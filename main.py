import copy
import os
from pathlib import Path
import time
import random
import pprint

from yt_dlp import YoutubeDL

from config import *
from yt_types import *
from yt_types import empty_Metadata
import utils
import display
import yt_wrapper
import post_processing

def _validate_cookies():
    if COOKIE_FILE is not None:
        if not os.path.exists(COOKIE_FILE):
            raise ValueError("COOKIE_FILE does not exist")
        with open(COOKIE_FILE, 'r') as f:
            if len(f.read()) == 0:
                raise ValueError("COOKIE_FILE is empty")

def __pl_input_is_path():
    return os.path.exists(PL_ID_OR_PATH)

def _get_flat_info():
    # get flat playlist info - new or existing
    if __pl_input_is_path():
        pl_info: PL_InfoDict = utils.json_load(PL_ID_OR_PATH)
        if (utils.now_as_epoch() - (pl_info.get('epoch') or 0)) > REFRESH_AFTER:
            pl_info = yt_wrapper.extract_flat_info(PL_ID_OR_PATH, opts={'cookiefile': COOKIE_FILE})
    elif utils.is_id_like(PL_ID_OR_PATH, False) or 'list=' in PL_ID_OR_PATH:
        pl_info = yt_wrapper.extract_flat_info(PL_ID_OR_PATH, opts={'cookiefile': COOKIE_FILE})
    else:
        raise ValueError(f'{PL_ID_OR_PATH} does not resemble a valid id or path!')
    
    return pl_info

def make_pl_info_path(tmpl, info, pre_suffix=''):
    p = Path(HOME) / YoutubeDL().evaluate_outtmpl(tmpl, info, True)
    if not pre_suffix:
        return str(p)
    return str(p.with_suffix(f'.{pre_suffix}.json'))


# TODO Refactor to lower complexity
def download_pl():

    _validate_cookies()

    pl_info = _get_flat_info()
    if DELETE_COOKIES and COOKIE_FILE:
        with open(COOKIE_FILE, 'w') as f: ...

    # Get outtmpl paths
    paths, pl_path, v_path = yt_wrapper.make_paths(
        Home               = HOME,
        # \/\/\/ for more flexibility the pl dirname is here instead of in config \/\/\/
        Playlist           = f'{pl_info['title'] or '[no title]'} [{utils.truncate(pl_info['id'], 11, end_in_max=False, trunc_start=True)}]',
        indiv_video_folders = INDIVIDUAL_VIDEO_FOLDERS,
        pl_archive          = ARCHIVE_FN)
    
    best_info_path = None
    if not __pl_input_is_path() and WRITE_FLAT and not os.path.exists(PL_ID_OR_PATH):
        best_info_path = make_pl_info_path(paths['outtmpl']['pl_infojson'], pl_info, 'flat') # type: ignore
        utils.json_dump( pl_info, best_info_path )

    # Load archives
    metadata_path = os.path.join(pl_path, METADATA_FN)
    metadata: Metadata = utils.json_load(metadata_path, empty_Metadata())

    # Validate state
    if metadata['paths'] and metadata['paths'] != paths:
        raise ValueError("Detected changed path settings!")
    metadata['paths'] = copy.deepcopy(paths)
    
    # Load yt_dlp archive for match filter
    yt_dlp_archive = yt_wrapper.load_yt_archive(paths.get('download_archive'))
    __dl_ytdlp = set(utils.ids_from_ytdlp(yt_dlp_archive))
    __dl_hist = set(utils.merge_history(metadata['history'])['download'])
    if __dl_ytdlp != __dl_hist:
        raise ValueError(f"Detected download state mismatch:\nytdlp-only: {__dl_ytdlp - __dl_hist}\nhist-only: {__dl_hist - __dl_ytdlp}")
    del __dl_ytdlp, __dl_hist
    
    opts: YT_DLP_Params = {
        **OPTS,
        **paths,
        'match_filter': yt_dlp_match_filter, # type: ignore
    }

    edit_final_opts_in_place(opts)
    opts = edit_final_opts(opts)

    # download playlist videos and data based on opts
    download_info = yt_wrapper.download_pl_videos(
        pl_info              = pl_info,
        wrapper_match_filter = lambda v_info, curr: wrapper_match_filter(v_info, curr, metadata['history'], yt_dlp_archive),
        opts                 = opts)
    
    if not download_info['extract'] and not download_info['download']:
        print("No new info")
        input("Continue anyway?")
        # TODO
    
    if pl_info.get('epoch') is None:
        pl_info['epoch'] = -utils.now_as_epoch()
        print(utils.rgb(" WARNING ", bg_rgb=(200,200,0)), f"pl_info epoch not found or is None, setting to negative of current time: {pl_info['epoch']}")
    if str(pl_info['epoch']) not in metadata['history']: # type: ignore - epoch is an int
        metadata['history'][pl_info['epoch']] = download_info # type: ignore - epoch is an int
    else:
        # set as current time
        metadata['history'][utils.now_as_epoch()] = download_info

    # write raw extract info, act as fallback if no or bad 'best_info_path'
    if WRITE_PL_INFO:
        best_info_path = make_pl_info_path(paths['outtmpl']['pl_infojson'], pl_info) # type: ignore
        utils.json_dump(pl_info, best_info_path)

    # write info combined with the previous best info
    def get_merge_info():
        # TODO: Make merge epoch `now`
        # support using the flat playlist over and over, building the merge

        old_best_info_path = metadata['best_info_path']
        if old_best_info_path is None or not os.path.exists(old_best_info_path):
            return None
        
        old_pl_info: PL_InfoDict = utils.json_load(old_best_info_path, default=None)
        if not isinstance(old_pl_info, dict):
            print(f"{metadata['best_info_path']} is a malformed json")
            return None
        
        print("Found old_best_info")
        return post_processing.merge_pl_infos([pl_info, old_pl_info])

    merge_info = None
    metadata['epoch'] = utils.now_as_epoch()
    if WRITE_BEST:
        merge_info = get_merge_info()
        if merge_info:
            print("Wrote merge info")
            __pl_info_epoch = merge_info['epoch'] # type: ignore
            merge_info['epoch'] = metadata['epoch']
            best_info_path = make_pl_info_path(paths['outtmpl']['pl_infojson'], merge_info, 'merge') # type: ignore
            merge_info['epoch'] = __pl_info_epoch
            utils.json_dump(merge_info, best_info_path)
        elif not WRITE_PL_INFO:
            print("Failed to find old best info, writing pl_info instead")
            best_info_path = make_pl_info_path(paths['outtmpl']['pl_infojson'], pl_info) # type: ignore
            utils.json_dump(pl_info, best_info_path)
        else:
            print('No')
            # write nothing if no merge_info and WRITE_PL_INFO already wrote pl_info

    metadata['best_info_path'] = best_info_path # type: ignore
    utils.json_dump(metadata, metadata_path, 'rm old')
    display.download_results(download_info)

def rebuild_merge():
    pl_infos = []
    for p in os.listdir('test/The Verge of Impossibility [...3Cfmpjqm-Pa]/Infojson'):
        for 
    post_processing.merge_pl_infos()


def main():
    # download_pl()

if __name__ == "__main__":
    main()