__all__ = ['DownloadPlaylist']

import os

from config import DownloaderConfig
from yt_types import *
import yt_types
import utils
import yt_utils
import yt_wrapper
import post_processing

import display



class DownloadPlaylist:
    def __init__(self, config: DownloaderConfig) -> None:
        self.config = config

        self.pl_info, self.is_new_pl_info = self.get_init_info()
        if self.config.empty_cookies:
            with open(self.config.cookie_file, 'r'): ... # type: ignore
        
        opt_outpaths, self.pl_outtmpls = self.generate_paths()
        
        yt_utils.get_v_info_level(self.pl_info)
        if config.write_flat and self.is_new_pl_info:
            # will be at least flat_info, may be better.
            utils.json_dump(
                obj = self.pl_info,
                dst = yt_utils.ytdlp_eval_tmpl(self.pl_outtmpls['flat_infojson'], self.pl_info),
                on_collision = 'mov new', auto_rename=True)




    def get_init_info(self) -> tuple[PL_InfoDict, bool]:
        """
        Based on the config playlist identifier, do one of:
        - Extract flat info from id
        - Load past playlist info, extract if old
        - Load lastest_flat_path from metadata, extract if old

        Something is old if more than `refresh_after` time has passed since the stored epoch.
            (if no epoch, assume old)
        """

        __extract_flat_info = lambda id: yt_wrapper.extract_flat_info(id, opts={'cookiefile': self.config.cookie_file})

        if self.config.playlist_id:
            return __extract_flat_info(self.config.playlist_id), True
        
        elif self.config.info_path:
            info = utils.json_load(self.config.info_path)
            _time_passed = utils.epoch_now() - info.get('epoch', 0)
            if isinstance(info, dict) and _time_passed <= self.config.refresh_after:
                return info, False
            if isinstance(info, dict):
                return info, False
            raise ValueError("Info json is malformed")
        
        elif self.config.metadata_path:
            old_metadata: Metadata = utils.json_load(self.config.metadata_path)
            
            # don't validate yet, not all branches got metadata yet
            _time_passed = utils.epoch_now() - old_metadata['pl_epoch']
            if _time_passed <= self.config.refresh_after:
                return __extract_flat_info(old_metadata['id']), True
            
            # try paths
            for k in ['latest_flat_info', 'latest_pl_info', 'latest_merge_info']:
                p = old_metadata.get(k)
                if p is None:
                    continue
                info: PL_InfoDict = utils.json_load(p, default=None)
                _time_passed = utils.epoch_now() - info.get('epoch', 0)
                if isinstance(info, dict) and _time_passed <= self.config.refresh_after:
                    return info, False
                utils.WARNING(f'In Metadata, malformed {k} info json at {p}')
            return __extract_flat_info(old_metadata['id']), True
        
        else:
            raise ValueError("No playlist identificaiton found !!!\nCheck config.py validations")

    def generate_paths(self) -> tuple[YT_DLP_Params, PL_Outtmpl]:
        """ make `paths`, `outtmpl`, `download_archive` opts

        Returns:
            tuple[YT_DLP_Params, RequiredPaths]:
            - `paths`, `outtmpl`, and `download_path` Params
            - `RequiredPaths` are all absolute paths
        
        Defaults from `DEFAULT_OUTTMPL`, `OUTTMPL_TYPES` (in yt_dlp/utils/_utils.py)    
        field_reference: https://github.com/yt-dlp/yt-dlp#output-template
        """

        PATH_TMPLS = self.config.path_tmpls
        Home = self.config.home
        
        if callable(PATH_TMPLS['Playlist']):
            Playlist = PATH_TMPLS['Playlist'](self.pl_info)
        else:
            Playlist = yt_utils.ytdlp_eval_tmpl(PATH_TMPLS['Playlist'], self.pl_info)

        pl_outtmpls: PL_Outtmpl = {
            'Playlist':         os.path.join(Home, Playlist),

            'video_file':       os.path.join(Home, Playlist, PATH_TMPLS['video_file']),

            'flat_infojson':    os.path.join(Home, Playlist, PATH_TMPLS['flat_infojson']),
            'pl_infojson':      os.path.join(Home, Playlist, PATH_TMPLS['pl_infojson']),
            'merge_infojson':   os.path.join(Home, Playlist, PATH_TMPLS['merge_infojson']),

            'ytdlp_archive':    os.path.join(Home, Playlist, PATH_TMPLS['ytdlp_archive']),
            'metadata':         os.path.join(Home, Playlist, PATH_TMPLS['metadata']),
        }

        opt_outpaths: YT_DLP_Params = {
            'paths': {'home': Home}, # type: ignore - Home directory of all outtmpl (there's also `temp`)
            'outtmpl': {
                'default':  pl_outtmpls['video_file'],
                # infojsons and metadata are custom
            },
            'download_archive': pl_outtmpls['ytdlp_archive'],
        }
        for k in ConfigOuttmpl.__optional_keys__:
            if k in PATH_TMPLS:
                p = os.path.join(Playlist, PATH_TMPLS[k])
                pl_outtmpls[k] = p
                opt_outpaths['outtmpl'][k] = p # type: ignore - 'outtmpl' is defined, keys are hardcoded in to be valid

        return opt_outpaths, pl_outtmpls



    


# TODO: Convert to class
# WHY:
# Data is being changed all over,
# This causes functional programming to get messy
# Not pure functions anyway

def _validate_metadata(old_metadata: Metadata, curr: Metadata):

    # keys
    if set(old_metadata.keys()) != set(Metadata.__required_keys__):
        extra, msissing = dif_sets(set(old_metadata.keys()), set(Metadata.__required_keys__))
        raise ValueError(
            f"Malformed metadata!\n"
            f"Extra keys: {extra}\n"
            f"Missing keys: {msissing}\n")
    
    # files
    for k in yt_types._MetadataFiles.__required_keys__:
        _validate_path(old_metadata['path_tmpls'][k], k)

    # path_tmpls
    if old_metadata['path_tmpls'] is not {} and old_metadata['path_tmpls'] != curr['path_tmpls']:
        raise ValueError("Malformed 'path_tmpls' in old metadata")

def _validate_dl_archive_sync(yt_dlp_archive, metadata):
    ytdlp_dl = set(utils.ids_from_ytdlp(yt_dlp_archive))
    hist_dl = set(utils.ids_from_history(metadata['history'])['download'])
    if ytdlp_dl != hist_dl:
        raise ValueError(f"Detected download state mismatch:\nytdlp-only: {ytdlp_dl - hist_dl}\nhist-only: {hist_dl - ytdlp_dl}")



def __pl_input_is_path():
    return os.path.exists(PLAYLIST_IDENTIFIER)

def _get_flat_info() -> tuple[PL_InfoDict, bool]:
    """ Get flat playlist info from existing file or extraction.
    If given a file and pl_info epoch is older than `REFRESH_AFTER`, extract again.
    Does not update `config.py` file to the new path!

    Raises:
        ValueError: If unrecognizedPlaylist input

    Returns:
        tuple[PL_InfoDict, bool]: Info and if it is new info (newly extracted)
    """
    # get flat playlist info - new or existing
    if __pl_input_is_path():
        pl_info: PL_InfoDict = utils.json_load(PLAYLIST_IDENTIFIER)
        is_new = False
        if (utils.epoch_now() - (pl_info.get('epoch') or 0)) > REFRESH_AFTER:
            pl_info = yt_wrapper.extract_flat_info(pl_info['id'], opts={'cookiefile': COOKIE_FILE})
            is_new = True
    elif utils.is_id_like(PLAYLIST_IDENTIFIER, False) or 'list=' in PLAYLIST_IDENTIFIER:
        pl_info = yt_wrapper.extract_flat_info(PLAYLIST_IDENTIFIER, opts={'cookiefile': COOKIE_FILE})
        is_new = True
    else:
        raise ValueError(f'{PLAYLIST_IDENTIFIER} does not resemble a valid id or path!')
    
    return pl_info, is_new



def add_metadata_history(pl_info: PL_InfoDict, metadata: Metadata, download_info: PL_DownloadInfo):
    __now = utils.epoch_now()
    if pl_info.get('epoch') is None:
        pl_info['epoch'] = __now
        utils.WARNING(f"pl_info epoch not found or is None, setting to current time: {__now}")
    
    if str(pl_info.get('epoch')) in metadata['history']:
        metadata['history'][str(__now)] = download_info
        utils.WARNING(f"pl_info epoch already exists in history, setting to current time: {__now}")
    else:
        metadata['history'][str(pl_info.get('epoch'))] = download_info



def _write_pl_info(pl_info: PL_InfoDict, tmpl: str) -> str:
    """ Writes the raw pl_info, changes the file epoch to the latest epoch """
    
    # set epoch to most recent v_info epoch
    latest_epoch = get_latest_epoch(pl_info)
    path = eval_with_dif_epoch(pl_info, latest_epoch, tmpl)
    utils.json_dump(pl_info, path)
    return path

def _write_merge_info(pl_info: PL_InfoDict, old___________: str|None, tmpl: str) -> tuple[PL_InfoDict, str]:
    """ Writes merge_info, sets time to latest epoch """

    def _get_merge_info(curr: PL_InfoDict, p: str|None):
        # support using the flat playlist over and over, building the merge
        if p is None or not os.path.exists(p):
            return None
        old_pl_info: PL_InfoDict = utils.json_load(p, default=None)
        if not isinstance(old_pl_info, dict):
            return None
        return post_processing.merge_pl_infos([curr, old_pl_info])
    
    merge_info = _get_merge_info(pl_info, old___________)
    latest_epoch = get_latest_epoch(merge_info or pl_info)
    path = eval_with_dif_epoch(pl_info, latest_epoch, tmpl)
    utils.json_dump(merge_info, path)
    return merge_info or pl_info, path




# TODO: Allow metadata path as the Playlist Identifier
def download_playlist():

    pl_info, is_new_pl_info = _get_flat_info()

    metadata: Metadata = yt_types.empty_Metadata()
    # Delete cookies ASAP
    if DELETE_COOKIES and COOKIE_FILE:
        with open(COOKIE_FILE, 'w'):
            ... # clear contents of file

    # Get paths
    opt_paths, req_paths = yt_wrapper.make_paths(pl_info)
    metadata['path_tmpls'] = PATH_TMPLS
    metadata['path_tmpls']['Playlist'] = os.path.relpath(req_paths['Playlist'], req_paths['Home']) # must be resolved/stable

    # Write flat ASAP
    if WRITE_FLAT and is_new_pl_info:
        metadata['latest_flat_info'] = yt_wrapper.ytdlp_eval_tmpl(req_paths['flat_infojson'], pl_info) # type: ignore
        utils.json_dump(pl_info, metadata['latest_flat_info'])
    
    # Load metadata
    metadata_path = os.path.join(req_paths['metadata'])
    old_metadata: Metadata = utils.json_load(metadata_path, yt_types.empty_Metadata())
    _validate_metadata(old_metadata, metadata)


    
    # Load yt_dlp archive for match filter
    yt_dlp_archive = yt_wrapper.load_yt_archive(req_paths['ytdlp_archive'])
    _validate_dl_archive_sync(yt_dlp_archive, metadata)
    
    # Build and finalize yt_dlp options
    opts: YT_DLP_Params = {**OPTS, **opt_paths}
    config.edit_final_opts_in_place(opts)
    opts = config.edit_final_opts(opts)

    # Download playlist videos and data based on opts
    pl_dl_info = yt_wrapper.download_pl_videos(
        pl_info              = pl_info,
        wrapper_match_filter = lambda v_info, curr: wrapper_match_filter(v_info, curr, metadata['history'], yt_dlp_archive),
        opts                 = opts)
    metadata['epoch'] = utils.epoch_now()
    
    # Add download info to metadata history
    add_metadata_history(pl_info, metadata, pl_dl_info)

    # Write raw pl_info (may be the same as flat info)
    id_dl_info = utils.ids_from_download_info(pl_dl_info)
    has_new_v_info = id_dl_info['extract'] or id_dl_info['download']
    if WRITE_PL_INFO:
        if not has_new_v_info:
            utils.WARNING("pl_info will be the same as flat_info")
        metadata['latest_pl_info'] = _write_pl_info(pl_info, req_paths['pl_infojson'])

    # Write merge info with the previous best info
    if WRITE_MERGE:
        _merge_info, metadata['latest_merge_info'] = _write_merge_info(pl_info, old_metadata['latest_merge_info'] or old_metadata['latest_pl_info'] or old_metadata['latest_flat_info'], req_paths['merge_infojson'])
        if _merge_info:
            pl_info = _merge_info    

    # Write metadata
    utils.json_dump(metadata, metadata_path, 'rm old')

    # Display overall results
    display.pl_download_info(pl_dl_info, errors=True)

# def rebuild_merge(pl_dir, info_dir, out):
#     pl_infos = []
#     for p in os.listdir(pl_dir):
#         for 
#     post_processing.merge_pl_infos()



def main():
    download_playlist()
    pass

if __name__ == "__main__":
    main()