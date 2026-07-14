__all__ = [
    'download_video',
    'extract_flat_info', 'download_pl_videos',
    'load_yt_archive',
    'download_video_alt',
]

import os
import pprint
from typing import Callable

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from yt_types import *
import utils
import yt_utils
import pp_utils
import display



def download_video(
        v_url_or_id: str,
        opts: YT_DLP_Params = {},
        yt: bool = True,
        wa: bool = True,
        _download: bool = True,
) -> tuple[V_InfoDict|dict|None, list[Exception], bool]:
    """ Downloads a video, using Youtube and/or WebArchive extractors

    Args:
        id (str): the id of the video
        opts (YT_DLP_Params, optional): any additional opts for the download. Defaults to {}.
        yt (bool, optional): Use `YoutubeIE`. Should be False if it is known to be unavailable. Defaults to True.
        wa (bool, optional): Use `YoutubeWebArchiveIE` fallback. Defaults to True.
        _download (bool, optional): Whether to download the video. Defaults to True.

    Returns:
        tuple[V_InfoDict | dict | None, list[Exception], bool]:
        - video info, `None` if the vid is already in the archive
        - list of Exception objects
        - if extraction was successful
    """
    info = {}
    errors: list[Exception] = []
    if yt:
        try:
            with YoutubeDL(opts) as ydl:
                _info = ydl.extract_info(v_url_or_id, download=_download)
                if _info is None:
                    return None, errors, True # already downloaded
                info.update(_info)
                return info, errors, True
        except Exception as yt_err:
            if isinstance(yt_err, DownloadError):
                info['yt_unavailable_msg'] = yt_err.msg
            else: # unexpected
                errors.append(yt_err)
    if wa:
        try:
            with YoutubeDL(opts) as ydl:
                _info = ydl.extract_info(yt_utils.get_archiveorg_url(v_url_or_id, for_yt_dlp=True), download=_download)
                if _info is None:
                    return None, errors, True # already downloaded
                info.update(_info)
                return info, errors, True
        except Exception as wa_err:
            if isinstance(wa_err, DownloadError):
                info['wa_unavailable_msg'] = wa_err.msg
            else:# unexpected
                errors.append(wa_err)
    return info, errors, False



def extract_flat_info(pl_url_or_id: str, opts: YT_DLP_Params = {}) -> PL_InfoDict:
    """ Get basic info from a youtube playlist, it must be available on youtube.

    Args:
        pl_url_or_id (str): Playlist url or id to extract
        opts (YT_DLP_Params, optional): Options to pass into YoutubeDL. Defaults to {}.
            Note 'skip_download', 'extract_flat', 'ignoreerrors' are forced.

    Returns:
        PL_InfoDict: Flat playlist info
    """
    with YoutubeDL(opts | {
        'skip_download': 'True',
        'extract_flat': 'in_playlist',
        'ignoreerrors': True,
    }) as ydl:
        flat_info: PL_InfoDict = ydl.extract_info(pl_url_or_id, download=False) # type: ignore
    
    pp_utils.add_pl_info_to_entries(flat_info)
    now = utils.epoch_now()
    for entry in flat_info['entries']:
        entry['epoch'] = flat_info.get('epoch', -now)
    return flat_info



def get_result(v_info, success: bool) -> DL_Result:
    if not success:
        return DL_Result.FAIL
    if v_info is None:
        # None is returned if download cache or cancelled.
        return DL_Result.CACHED
    if yt_utils.has_download_info(v_info):
        return DL_Result.DOWNLOAD
    if yt_utils.has_extracted_info(v_info):
        return DL_Result.EXTRACT
    return DL_Result.UNRECOGNIZED

def download_pl_videos(
        pl_info: PL_InfoDict,
        wrapper_match_filter: Callable[[PL_V_InfoDict, PL_DownloadInfo], DL_Action]|None = None,
        opts: YT_DLP_Params = {},
        try_yt_if_unavailable: bool = True,
        wa: bool = True,
) -> PL_DownloadInfo:
    """ Extract and download videos in videos_to_download. Return the extracted info, download results, and errors

    Args:
        pl_info (PL_InfoDict): Info is changed in-place
        wrapper_match_filter (Callable[[PL_V_InfoDict, PL_DownloadInfo], DL_Action]|None, optional):
            Called before downloading the video. Is given current playlist download information.
            Returns a download action to control the current playlist download.
            Defaults to None; this will extract and download every video not in the yt-dlp download archive.
        opts (YT_DLP_Params, optional): Extra opts used by ``download_video()``. Defaults to {}.
        try_yt_if_unavailable (bool, optional): Try Youtube even if it seems unavailable. Defaults to True.
        wa (bool, optional): Use archive.org if YouTube failed (fallback). Defaults to True.

    Returns:
        
    """
    pl_dl_info: PL_DownloadInfo = []

    N = len(pl_info['entries'])
    DL_MAP_NO_USER = {
        str(action).lower(): action
        for action in DL_Action
        if action not in (DL_Action.USER)
    }
    try:
        for i, entry in enumerate(pl_info['entries']):
            action = DL_Action.DOWNLOAD
            if wrapper_match_filter is not None:
                action = wrapper_match_filter(entry, pl_dl_info)
            
            i_of_N = f"{i+1:{len(str(N))}}/{N}"
            pl_v_display = f'[{i_of_N}] [{entry['id']}] {entry.get('title') or "???"} - {entry.get('channel') or '???'}'
            

            if action == DL_Action.USER:

                # TODO: Display video details
                print(f"[TEMP]:\n{pprint.pformat(entry, indent=4)}")
                choice = utils.input_string(
                    list(DL_MAP_NO_USER.keys()),
                    f'Pick a Download Option: ',
                    prefix_options=True,
                )
                action = DL_MAP_NO_USER[choice]

            pl_dl_info.append({
                'id': entry['id'],
                'title': entry['title'],
                'action': action,
                'result': DL_Result.CANCELLED,
            })

            if action == DL_Action.QUIT:
                print(display.ACTION_TAG[DL_Action.QUIT].rendered)
                break
            elif action == DL_Action.SKIP:
                print(display.ACTION_TAG[action].rendered + ' ' + utils.hex(pl_v_display, display.ACTION_TAG[action].color))
                continue

            print()
            print(display.ACTION_TAG[action].rendered + ' ' + utils.hex(pl_v_display, display.ACTION_TAG[action].color))

            # v_info, errors, success = {}, [], True
            v_info, errors, success = download_video(
                entry['id'],
                opts=opts,
                yt = try_yt_if_unavailable or yt_utils.maybe_available_on_yt(entry),
                wa = wa,
                _download = (action == DL_Action.DOWNLOAD)
            )

            pl_dl_info[-1] = {
                'id': entry['id'],
                'title': (v_info or entry).get('title'),
                'action': action,
                'result': get_result(v_info, success),
            }
            if errors:
                pl_dl_info[-1]['errors'] = errors

            result_tag = display.download_result(pl_dl_info[-1])
            print(result_tag.rendered + ' ' + utils.hex(pl_v_display, result_tag.color))
            print()
            
            if v_info:
                entry.update(v_info) # type: ignore
    except KeyboardInterrupt:
        print(utils.hex("    KEYBOARD INTERRUPT    ", bg='#ffffff'))
    except Exception as e:
        print(display.exc(e))
    
    # may be redundent, but can't hurt
    pp_utils.add_pl_info_to_entries(pl_info)
    return pl_dl_info



def load_yt_archive(p: str|None) -> YT_DLP_DownloadArchive:
    if not p or not os.path.exists(p):
        return ()
    res = []
    with open(p, 'r', encoding='utf-8') as f:
        for line in f:
            if line:
                ie_key, v_id = line.split()
                res.append( (ie_key, v_id) )
    return tuple(res)


# TODO
def download_video_alt(url: str, opts: YT_DLP_Params) -> InfoDict|dict | Exception:
    """
    Tries to downlaod the video given the url using yt_dlp
    Returns the resulting data
    """
    try:
        with YoutubeDL(opts) as ydl:
            return ydl.extract_info(url) # type: ignore
    except Exception as e:
        return e