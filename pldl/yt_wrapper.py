__all__ = [
    'extract_flat_info',
    'download_video',
    'download_video_alt',
    'load_yt_archive',
    'sanitize_info',
]

import os
from typing import Any

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from .utils import utils
from .yt_types import *
from . import yt_utils


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
    
    now = utils.epoch_now()
    for entry in flat_info['entries']:
        entry.setdefault('epoch', flat_info.get('epoch', now))
        entry.setdefault('playlist_epoch', flat_info.get('epoch', now))
    return flat_info



def download_video(
        v_url_or_id: str,
        opts: YT_DLP_Params = {},
        yt: bool = True,
        wa: bool = True,
        _download: bool = True,
) -> tuple[V_InfoDict|None, list[Exception], bool]:
    """ Downloads a video, using Youtube and/or WebArchive extractors

    Args:
        v_url_or_id (str): the url or id of the video
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
    info: V_InfoDict = {} # type: ignore - init
    errors: list[Exception] = []
    if yt:
        try:
            with YoutubeDL(opts) as ydl:
                _info = ydl.extract_info(v_url_or_id, download=_download)
                if _info is None:
                    return None, errors, True # already downloaded
                info.update(_info) # type: ignore
                return info, errors, True
        except DownloadError as yt_err:
            info['yt_unavailable_msg'] = yt_err.msg
        except Exception as e:
            errors.append(e)
    if wa:
        try:
            with YoutubeDL(opts) as ydl:
                _info = ydl.extract_info(yt_utils.get_archiveorg_url(v_url_or_id, for_yt_dlp=True), download=_download)
                if _info is None:
                    return None, errors, True # already downloaded
                info.update(_info) # type: ignore
                return info, errors, True
        except DownloadError as wa_err:
            info['wa_unavailable_msg'] = wa_err.msg
        except Exception as e:
            errors.append(e)
    return info, errors, False



def load_yt_archive(p: str|None) -> YT_DLP_DownloadArchive:
    if not p or not os.path.exists(p):
        return ()
    res = []
    with open(p, 'r', encoding='utf-8') as f:
        for line_no, line in enumerate(f, start=1):
            if not line:
                continue
            items = line.split()
            if len(items) != 2:
                utils.WARNING(f"[yt_dlp archive] Unrecognized @ L{line_no}: {line}")
                continue
            ie_key, v_id = items
            if yt_utils.is_id_like(v_id, is_video=True):
                utils.WARNING(f"[yt_dlp archive] Bad video id @ L{line_no}: {line}")
                continue
            res.append( (ie_key, v_id) )
    return tuple(res)



def download_video_alt(url: str, opts: YT_DLP_Params) -> InfoDict | str|None | Exception:
    """
    Tries to downlaod the video given the url using yt_dlp
    Returns the resulting data
    """
    try:
        with YoutubeDL(opts) as ydl:
            return ydl.extract_info(url) # type: ignore
    except DownloadError as dl_err:
        return dl_err.msg
    except Exception as e:
        return e


def sanitize_info[T](info_dict: T, remove_private_keys=False) -> T|Any:
    """
    Creates a json-dumpable deepcopy of the info_dict.
    
    Keeps: dict, list, tuple, set, LazyList, str, int, float, bool.
    Everything else is turned to str using repr().

    Never removes 'entries' kval.
    """

    info_dict = YoutubeDL.sanitize_info(info_dict, False) # type: ignore

    if remove_private_keys is False:
        return info_dict
    
    reject = lambda k, v: v is None or k.startswith('__') or k in {
        'requested_downloads', 'requested_formats', 'requested_subtitles', 'requested_entries',
        'filepath', '_filename', 'filename', 'infojson_filename', 'original_url',
        'playlist_autonumber',
    }
    
    def filter_fn(obj):
        if isinstance(obj, dict):
            return {k: filter_fn(v) for k, v in obj.items() if not reject(k, v)}
        elif isinstance(obj, list):
            return [filter_fn(x) for x in obj] # get entries
        # other cases are handled in YoutubeDL
        return obj

    return filter_fn(info_dict)

