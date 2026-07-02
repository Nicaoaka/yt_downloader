__all__ = [
    'extract_flat_info', 'download_pl_videos'
]

import copy
from collections import defaultdict
import os
import enum
from typing import Callable
import traceback

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

import utils 
from yt_types import *
import yt_types
import post_processing

def _download_video(
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
                _info = ydl.extract_info(utils.get_archiveorg_url(v_url_or_id, for_yt_dlp=True), download=_download)
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

class DL(enum.IntEnum):
    USER = -1
    QUIT = 0
    SKIP = 1
    EXTRACT = 2
    DOWNLOAD = 3

DL_STR_MAP = {
    DL.QUIT:    utils.rgb(" QUIT ", bg_rgb=(255,   0,   0)),
    DL.SKIP:    utils.rgb(" SKIP ", bg_rgb=(255, 255,   0)),
    DL.EXTRACT: utils.rgb(" EXTR ", bg_rgb=(  0, 200, 200)),
    DL.DOWNLOAD:utils.rgb(" DWLD ", bg_rgb=(  0, 255,   0)),
}

def download_pl_videos(
        pl_info: PL_InfoDict,
        wrapper_match_filter: Callable[[PL_V_InfoDict, PL_DownloadInfo], DL]|None = None,
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
        (DownloadInfo)
    """
    dl_info: PL_DownloadInfo = yt_types.empty_DownloadInfo()

    N = len(pl_info['entries'])
    try:
        for i, entry in enumerate(pl_info['entries']):
            action = DL.DOWNLOAD
            if wrapper_match_filter is not None:
                action = wrapper_match_filter(entry, dl_info)
            
            if action == DL.USER:
                # TODO
                print(utils.rgb(" <USER> - Not implemented ", bg_rgb=(0,0,200)))
                action = DL.EXTRACT
                pass
            
            print(DL_STR_MAP[action], utils.rgb(f'[{i+1:{len(str(N))}}/{N}] [{entry['id']}] {entry['title'] or "???"} - {entry.get('channel') or '???'}', (120, 220, 180)))

            if action == DL.QUIT:
                break
            elif action == DL.SKIP:
                dl_info['skip'].append(entry['id'])
                continue

            # v_info, errors, success = {}, [], True
            v_info, errors, success = _download_video(
                entry['id'],
                opts=opts,
                yt = yt or utils.maybe_available_on_yt(entry),
                wa = wa,
                _download = (action==DL.DOWNLOAD)
            )
            if not success:
                dl_info['fail'].append(entry['id'])
            else:
                if v_info is None:
                    dl_info['no_info'].append(entry['id'])
                elif utils.has_extracted_info(v_info):
                    dl_info['extract'].append(entry['id'])
                    if utils.has_download_info(v_info):
                        dl_info['download'].append(entry['id'])

            if errors:
                dl_info['error'].append( (entry['id'], errors) )

            entry.update(v_info) # type: ignore
    except KeyboardInterrupt:
        print(utils.rgb("    USER INTERRUPT    ", bg_rgb=(255,255,255)))
    except Exception as e:
        print(utils.rgb(''.join(traceback.format_exception(e)), (200,50,50)))
    
    # may be redundent, but can't hurt
    post_processing.add_pl_info_to_entries(pl_info)
    return dl_info


def make_paths(
        Home: str,
        Playlist: str,
        indiv_video_folders: bool,
        pl_archive: str|None,
        Videos: str = 'Videos',
        _Video: str = '%(title)s [%(id)s]',
) -> tuple[YT_DLP_Params, str, str]:
    """ make `outtmpl` and `download_archive` param

    Args:
        Home (str): The home folder (e.g. r'C:/users/yomama/Videos')
        Playlist (str): Playlist folder name
        indiv_video_folders (bool): Adds more paths to video outtmpl. Set True for thorough downloading.
        pl_archive (str|None): yt-dlp download archive filename.
        Videos (str, optional): Name of the folder that will contains all playlist videos. Defaults to `Videos`.
        _Video (str, optional): Name of individiual video folders (unused if `individual_video_folders = False`). Defaults to `%(title)s [%(id)s]`.

    Returns:
        tuple[YT_DLP_Params, str, str]:
        - `paths`, `outtmpl`, and `download_path` Params
        - `Playlist` Absolute Path
        - `Videos` Absolute Path

    File Structures:
    ```
        _Home
            PL_TITLE_ID
                archive
                Info
                    pl_infojson
                Videos
                    infojson
                    default : (playlist videos)
    ```
    
    With `indiv_video_folder = True`
    ```
        _Home
            _Playlist
                archive
                Info
                    pl_infojson
                Videos
                    _Video
                        default
                        pl_video : (same as default)
                        chapter
                        subtitle
                        thumbnail
                        description
                        annotation
                        infojson
                        link
    ```
    
    Defaults from `DEFAULT_OUTTMPL`, `OUTTMPL_TYPES` (in yt_dlp/utils/_utils.py)    
    field_reference: https://github.com/yt-dlp/yt-dlp#output-template
    """
    
    paths: YT_DLP_Params = {
        'paths': {'home': Home}, # type: ignore - Home directory
        'outtmpl': {
            'default':           os.path.join(Playlist, Videos, '%(title)s [%(id)s].%(ext)s'),
            'pl_video':          os.path.join(Playlist, Videos, '%(title)s [%(id)s].%(ext)s'),
            'pl_thumbnail':      os.path.join(Playlist, 'thumbnail.%(ext)s'),
            'pl_description':    os.path.join(Playlist, 'description'),
            'pl_infojson':       os.path.join(Playlist, 'Infojson', '%(epoch>%Y-%m-%d %H-%M-%S)s.json'),
            'chapter':           os.path.join(Playlist, Videos, 'chapters', '%(section_number)03d %(section_title)s [%(id)s].%(ext)s'), # gets added by default
        },
        'download_archive': None if pl_archive is None else os.path.join(Home, Playlist, pl_archive),
    }
    if indiv_video_folders:
        indiv = {
            'default':           os.path.join(Playlist, Videos, _Video, '%(title)s.%(ext)s'),
            'pl_video':          os.path.join(Playlist, Videos, _Video, '%(title)s.%(ext)s'),
            'subtitle':          os.path.join(Playlist, Videos, _Video, 'subtitles'),
            'thumbnail':         os.path.join(Playlist, Videos, _Video, 'thumbnail.%(ext)s'),
            'description':       os.path.join(Playlist, Videos, _Video, 'description'),
            'annotation':        os.path.join(Playlist, Videos, _Video, 'annotations.xml'),
            'infojson':          os.path.join(Playlist, Videos, _Video, 'Infojson', '%(epoch>%Y-%m-%d %H-%M-%S)s.json'),
            'link':              os.path.join(Playlist, Videos, _Video, 'link.%(ext)s'),
        }
        paths['outtmpl'].update(indiv) # type: ignore
    return paths, os.path.join(Home, Playlist), os.path.join(Home, Playlist, Videos)

def load_yt_archive(p: str|None) -> YT_DLP_DownloadArchive:
    if not p or not os.path.exists(p):
        return []
    res = []
    with open(p, 'r', encoding='utf-8') as f:
        for line in f:
            if line:
                ie_key, v_id = line.split()
                res.append( (ie_key, v_id) )
    return res
