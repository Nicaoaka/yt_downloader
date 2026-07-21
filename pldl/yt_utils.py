import re
import datetime
import os
from typing import TYPE_CHECKING

from yt_dlp import YoutubeDL
from yt_dlp.extractor.youtube import YoutubePlaylistIE

from .utils import utils
from .yt_types import *
from . import yt_types
if TYPE_CHECKING:
    from .config import PlaylistDL_Config



# YouTube and InternetWebArchive id/url

def get_pl_id(url_or_id: str) -> str|None:
    try:
        return YoutubePlaylistIE._match_id(url_or_id)
    except:
        return None

def is_id_like(id: str, is_video=False) -> bool:
    if not id:
        return False
    if is_video and len(id) != 11: # video ids are always 11 chars long
        return False
    
    # playlist id lengths can vary dramatically

    VALID_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_"
    # [a-zA-Z0-9-_]
    return all(c in VALID_CHARS for c in id)

def get_yt_video_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"

def get_yt_playlist_url(playlist_id: str, video_id: str = '') -> str:
    if not video_id:
        return f"https://www.youtube.com/playlist?list={playlist_id}"
    return f"https://www.youtube.com/watch?v={video_id}&list={playlist_id}"

def get_archiveorg_url(v_id: str, date: int|str|None = None, for_yt_dlp: bool = False) -> str:
    if not date:
        if for_yt_dlp:
            return 'ytarchive:' + v_id
        return f"https://web.archive.org/https://www.youtube.com/watch?v={v_id}"
    if for_yt_dlp:
        return f"ytarchive:{v_id}:{date}"
    return f"https://web.archive.org/web/{date}/https://www.youtube.com/watch?v={v_id}"

def get_archiveorg_video_url(video_id: str) -> str:
    return f"https://web.archive.org/web/2oe_/http://wayback-fakeurl.archive.org/yt/{video_id}"

def get_v_display(v_info: V_InfoDict|dict) -> str:
    res = ""

    if 'id' in v_info:
        res += f'[{v_info['id']}] '
    if 'title' in v_info and v_info['title']:
        res += f'{v_info['title']} '
    if 'channel' in v_info and v_info['channel']:
        res += f'by {v_info['channel']} '
    
    res = res.strip()

    if not res:
        return "< No Video display >"
    return res



# Path helpers

def ytdlp_eval_tmpl(tmpl: str, info: InfoDict|dict):
    return YoutubeDL().evaluate_outtmpl(tmpl, info, True) # type: ignore

def eval_tmpl_with_alt_data(tmpl: str, info: InfoDict|dict, alt_data: InfoDict|dict):
    """ Temporarily swap keys of `info` to `alt_data` to call ``ytdlp_eval_tmpl`` """
    original = {k: info.get(k, utils.__NO_DEFAULT) for k in alt_data}
    info |= alt_data

    path = ytdlp_eval_tmpl(tmpl, info)

    for k, v in original:
        if v is utils.__NO_DEFAULT:
            info.pop(k)
        else:
            info[k] = v
    return path



# Availability

def maybe_available_on_yt(info: V_InfoDict | dict) -> bool:
    """ Returns True if unsure """
    # 'ie_key' occurs in flat info, but flat will only use youtube - OK.
    if info.get('extractor_key') == 'YoutubeWebArchive':
        return True
    # incomplete extract (many other stats could be used like `duration`)
    return info.get('channel') is not None

def has_extracted_info(info: V_InfoDict | dict) -> bool:
    return bool(info.get('extractor'))

def has_download_info(info: V_InfoDict | dict) -> bool:
    return bool(info.get("requested_downloads"))



def get_v_info_level(v_info: V_InfoDict|dict|None) -> _V_InfoLevel:
    """ Webarchive could appear at Download or Extract """
    if not v_info:                    return _V_InfoLevel.NONE
    if has_download_info(v_info):     return _V_InfoLevel.DOWNLOAD
    if has_extracted_info(v_info):    return _V_InfoLevel.EXTRACT
    if maybe_available_on_yt(v_info): return _V_InfoLevel.FLAT
    return _V_InfoLevel.UNAVAIL_YT

def get_pl_info_level(pl_info: PL_InfoDict|dict|None) -> _PL_InfoLevel:
    if not pl_info or not pl_info.get('entries'): return _PL_InfoLevel.NONE
    has_extracts = any(get_v_info_level(entry) >= _V_InfoLevel.EXTRACT for entry in pl_info.get('entries', []))
    has_merge_timeline = 'merge_timeline' in pl_info
    match has_extracts, has_merge_timeline:
        case  True,  True: return _PL_InfoLevel.MERGE
        case  True, False: return _PL_InfoLevel.NORMAL
        case False,  True: return _PL_InfoLevel.MERGE_FLAT
        case False, False: return _PL_InfoLevel.FLAT


# Processing archives

def ids_from_yt_dlp_archive(l: YT_DLP_DownloadArchive) -> list[V_ID]:
    return [tup[1] for tup in l]

def ids_from_pl_download_info(pl_dl_info: PL_DownloadInfo) -> ID_DownloadInfo:
    res: ID_DownloadInfo = {
        'fail':     [],
        'extract':  [],
        'download': [],
        'error':    [],
    }
    for v in pl_dl_info:
        v_id = v['id']
        if v['result'] == DL_Result.FAIL: res['fail'].append(v_id)
        # if v['result'] == DL_Result.CANCELLED: res['skip'].append(v_id)
        # if v['result'] == DL_Result.CACHED: res['cached'].append(v_id)
        if v['result'] in (DL_Result.EXTRACT, DL_Result.DOWNLOAD): res['extract'].append(v_id)
        if v['result'] == DL_Result.DOWNLOAD: res['download'].append(v_id)
        if v.get('errors'):
            res['error'].append(v_id)
    return res

def ids_from_history(history: PL_DownloadHistory) -> ID_DownloadInfo:
    merged: ID_DownloadInfo = {
        'fail':     [],
        'extract':  [],
        'download': [],
        'error':    [],
    }
    for epoch in sorted(map(int, history.keys())): # oldest -> newest
        for k, ids in ids_from_pl_download_info(history[str(epoch)]).items():
            merged[k].extend(ids)
    return merged


def get_pl_v_info(pl_info: PL_InfoDict, v_idx: int):
    return {
        'playlist_id':                  pl_info['id'],
        'playlist':                     pl_info['title'] or pl_info['id'],
        'playlist_count':               pl_info['playlist_count'],
        'n_entries':                    pl_info['playlist_count'],
        'playlist_index':               v_idx,
        'playlist_autonumber':          v_idx,
        'playlist_title':               pl_info['title'],
        'playlist_channel':             pl_info['channel'],
        'playlist_channel_id':          pl_info.get('channel_id'),
        'playlist_uploader':            pl_info['uploader'],
        'playlist_uploader_id':         pl_info['uploader_id'],
        'playlist_webpage_url':         pl_info.get('webpage_url') or pl_info.get('original_url') or pl_info.get('url'),

        # custom
        'playlist_epoch': get_epoch(pl_info)
    }

def add_pl_info_to_entries(pl_info: PL_InfoDict):
    for i, entry in enumerate(pl_info['entries']):
        entry.update(get_pl_v_info(pl_info, i)) # type: ignore



# epoch stuff

def get_epoch(info: InfoDict|dict) -> int:
    from .config import DEFAULT_EPOCH
    return info.get('epoch', DEFAULT_EPOCH())

def get_latest_epoch(pl_info: PL_InfoDict) -> int:
    """ Max 'epoch' in pl_info and its entries.

    A negative epoch means the epoch wasn't found or all were malformed. """
    from .config import DEFAULT_EPOCH
    latest = max(
        get_epoch(pl_info),
        *(get_epoch(entry) for entry in pl_info['entries']))
    if latest <= DEFAULT_EPOCH():
        utils.WARNING(f"All epochs are malformed or missing: {latest}")
    return latest



def to_readable_epoch(epoch: int) -> str:
    # low epochs can be invalid because of timezones.
    # So, exclue the first 24 hours from the start of the epoch
    from .config import READABLE_EPOCH_FMT, MALFORMED_EPOCH_FMT

    is_malformed = epoch < 0

    if abs(epoch) <= 3600 * 24:
        return MALFORMED_EPOCH_FMT.replace('{}', str(epoch))
    
    formatted = datetime.datetime.fromtimestamp(abs(epoch)).strftime(READABLE_EPOCH_FMT)
    if is_malformed:
        return MALFORMED_EPOCH_FMT.replace('{}', formatted)
    return formatted


def from_readable_epoch(readable: str) -> int:
    from .config import READABLE_EPOCH_FMT, MALFORMED_EPOCH_FMT

    # for simple regex matching (besides you only really need one)
    assert MALFORMED_EPOCH_FMT.count('{}') == 1, "MALFORMED_EPOCH_FMT must include ONE {} to sub for EPOCH_FMT"
    assert MALFORMED_EPOCH_FMT.count('__epoch_fmt_sub') == 0, "MALFORMED_EPOCH_FMT cannot include '__epoch_fmt_sub' for internal reasons"
    MALFORMED_EPOCH_RE = '^'+ re.escape(MALFORMED_EPOCH_FMT.replace('{}', '__epoch_fmt_sub')).replace('__epoch_fmt_sub', '(.+)') +'$'
    LOW_EPOCH_RE = '^'+ re.escape(MALFORMED_EPOCH_FMT.replace('{}', '__epoch_fmt_sub')).replace('__epoch_fmt_sub', r'(-?\d+)') +'$'

    match = re.match(LOW_EPOCH_RE, readable)
    if match:
        return int(match.groups()[0])
    match = re.match(MALFORMED_EPOCH_RE, readable)
    if match:
        readable = match.groups()[0]
    return int(datetime.datetime.strptime(readable, READABLE_EPOCH_FMT).timestamp())


# basic validations

def validate_pl_info(pl_info: PL_InfoDict):
    # TODO - is this necessary?
    if missing := utils.get_missing_typeddict_keys(pl_info, PL_InfoDict): # type: ignore - Metadata is a TypedDict
        raise KeyError(f"Missing kvals: {missing}")

def validate_metdata_config_sync(metadata: Metadata, config: PlaylistDL_Config):
    """ May raise KeyError, RuntimeError, or FileNotFoundError """

    if missing := utils.get_missing_typeddict_keys(metadata, Metadata): # type: ignore - Metadata is a TypedDict
        raise KeyError(f"Missing kvals: {missing}")

    for k in yt_types._MetadataPointers.__required_keys__:
        if metadata['pointers'][k] is None:
            continue

        rel_path, _epoch = metadata['pointers'][k]
        real_path = os.path.join(config.home, rel_path)
        utils.assert_file(real_path, f"{k} (metadata)", min_size=1)
    
    meta_path = os.path.join(config.home, metadata['path_tmpls'].get('Playlist', 'NA'), metadata['path_tmpls'].get('metadata', 'NA'))
    for k in metadata['path_tmpls'].keys() | config.path_tmpls.keys():
        if k == 'Playlist':
            continue # can't be checked without info
        if k not in metadata['path_tmpls']:
            raise KeyError(
                f"Missing key in metadata: {{{k!r}: {config.path_tmpls[k]!r}}}\n"
                f"Path: {meta_path}")
        if k not in config.path_tmpls:
            raise KeyError(
                f"Extra key in metdata: {{{k!r}: {metadata['path_tmpls'][k]!r}}}\n"
                f"Path: {meta_path}")
        if os.path.relpath(metadata['path_tmpls'][k], metadata['path_tmpls']['Playlist']) != config.path_tmpls[k]:
            raise KeyError(
                f"Changed `path_tmpls`: {repr(k)}:\n"
                f"metadata: {metadata['path_tmpls'][k]}\n"
                f"config:   {config.path_tmpls[k]}\n"
                f"Path: {meta_path}")



