__all__ = [
    'download_video',
    'extract_flat_info', 'download_pl_videos',
    'load_yt_archive',
]

import os
from typing import Callable
import traceback

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from yt_types import *
import utils
import yt_utils
import post_processing
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
                    return None, errors, True
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
                    return None, errors, True
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
    post_processing.add_pl_info_to_entries(flat_info)
    return flat_info



def get_result(v_info, success: bool) -> DL_Result:
    if not success:
        return DL_Result.FAIL
    if v_info is None:
        return DL_Result.NO_INFO
    if not yt_utils.has_extracted_info(v_info):
        return DL_Result.UNRECOGNIZED
    if not yt_utils.has_download_info(v_info):
        return DL_Result.EXTRACT
    return DL_Result.DOWNLOAD

def download_pl_videos(
        pl_info: PL_InfoDict,
        wrapper_match_filter: Callable[[PL_V_InfoDict, PL_DownloadInfo], DL_Action]|None = None,
        opts: YT_DLP_Params = {},
        yt: bool = False,
        wa: bool = True,
) -> PL_DownloadInfo:
    """ Extract and download videos in videos_to_download. Return the extracted info, download results, and errors

    Args:
        opts (YT_DLP_Params, optional): Extra opts. Defaults to {}.
        wa_fallback (bool, optional): Use archive.org fallback. Defaults to True.
        try_unavailable (bool, optional): Try youtube even if marked as unavailable in flat_info. Defaults to False.

    Returns:
        
    """
    pl_dl_info: PL_DownloadInfo = []

    N = len(pl_info['entries'])
    DL_MAP = {
        str(action).lower(): action
        for action in DL_Action
        if action not in (DL_Action.USER)
    }
    try:
        for i, entry in enumerate(pl_info['entries']):
            action = DL_Action.DOWNLOAD
            if wrapper_match_filter is not None:
                action = wrapper_match_filter(entry, pl_dl_info)
            
            if action == DL_Action.USER:
                choice = utils.input_string(
                    list(DL_MAP.keys()),
                    f'Pick a Download Option: ',
                    prefix_options=True,
                )
                action = DL_MAP[choice]
            
            i_of_N = f"{i+1:{len(str(N))}}/{N}"
            pl_v_display = f'[{i_of_N}] [{entry['id']}] {entry.get('title') or "???"} - {entry.get('channel') or '???'}'
            print(utils.hex(pl_v_display, '#78dcb4'))
            print(display.DL_ACTION_STR_MAP[action])
            input()

            pl_dl_info.append({
                'id': entry['id'],
                'action': action,
                'result': DL_Result.CANCELLED,
                'errors': [],
            })
            if action == DL_Action.QUIT:
                break
            elif action == DL_Action.SKIP:
                continue

            # v_info, errors, success = {}, [], True
            v_info, errors, success = download_video(
                entry['id'],
                opts=opts,
                yt = yt or yt_utils.maybe_available_on_yt(entry),
                wa = wa,
                _download = (action == DL_Action.DOWNLOAD)
            )

            pl_dl_info[-1] = {
                'id': entry['id'], 'action': action, 'errors': errors,
                'result': get_result(v_info, success),
            }
            display.download_result(pl_dl_info[-1])
            entry.update(v_info) # type: ignore
    except KeyboardInterrupt:
        print(utils.hex("    KEYBOARD INTERRUPT    ", bg='#ffffff'))
    except Exception as e:
        print(utils.hex(''.join(traceback.format_exception(e)), fg='#c83232'))
    
    # may be redundent, but can't hurt
    post_processing.add_pl_info_to_entries(pl_info)
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
