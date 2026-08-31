__all__ = [  # noqa: RUF022
    'DEFAULT_EPOCH', 'READABLE_EPOCH_FMT', 'MALFORMED_EPOCH_FMT',
    
    'get_v_id_from_yt_url', 'get_pl_id_from_yt_url', 'is_id_like',
    'get_yt_video_url', 'get_yt_playlist_url',
    'get_archiveorg_url_for_yt_dlp', 'get_archiveorg_url', 'get_archiveorg_video_url', 
    'get_v_display',

    'extract_flat_info', 'download_video', 'download_video_generic',
    'derive_v_info_level', 'derive_pl_info_level',

    'ytdlp_eval_tmpl',

    'copy_and_sanitize_info',
    'ids_from_yt_dlp_archive', 'ids_from_pl_download_info', 'ids_from_history',
    'get_pl_v_info', 'fixup_pl_info', 'interpret_error_msg',

    'get_epoch', 'get_latest_epoch', 'to_readable_epoch', 'from_readable_epoch',
]

import datetime
import re
from collections.abc import Callable
from typing import Any

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from pldl import pldl_types
from pldl.pldl_types import *
from pldl.utils import utils

# YouTube and InternetWebArchive id/url

def get_v_id_from_yt_url(url_or_id: str) -> str|None:
    from yt_dlp.extractor.youtube import YoutubeIE
    try:
        return YoutubeIE._match_id(url_or_id)
    except:  # noqa: E722 - do not error
        return None

def get_pl_id_from_yt_url(url_or_id: str) -> str|None:
    from yt_dlp.extractor.youtube import YoutubePlaylistIE
    try:
        return YoutubePlaylistIE._match_id(url_or_id)
    except:  # noqa: E722 - do not error
        return None

def is_id_like(id: str, is_video=False) -> bool:
    if not id:
        return False
    if is_video and len(id) != 11: # video ids are always 11 chars long
        return False
    
    # playlist id lengths can vary dramatically
    VALID_CHARS = ( # [a-zA-Z0-9-_]
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '1234567890'
        '-_'
    )
    return all(c in VALID_CHARS for c in id)

def get_v_display(v_info: V_InfoDict|dict) -> str:
    # some titles and channel names are empty strings
    title = utils.first_non_default(v_info, ['title', 'alt_title'], default_values=[None], default_return='???')
    creator = utils.first_non_default(v_info, ['channel', 'uploader_id', 'uploader', 'artist', 'creator'], default_values=['', None], default_return='???')
    return f"[{v_info['id']}] {title} by {creator}"

def get_yt_video_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"

def get_yt_playlist_url(playlist_id: str, video_id: str = '') -> str:
    if not video_id:
        return f"https://www.youtube.com/playlist?list={playlist_id}"
    return f"https://www.youtube.com/watch?v={video_id}&list={playlist_id}"

def get_yt_thumbnail_url(video_id: str) -> str:
    return f"https://i.ytimg.com/vi_webp/{video_id}/maxresdefault.webp"


# `date` is archiveorg format, so YYYYmmddHHMMSS
# For example, "20261225090125" is 2026/12/25 9:01:25.
# This can be input as an int: 2026_12_25__09_01_25.
def get_archiveorg_url_for_yt_dlp(v_id_or_url: str, date: int|str|None = None) -> str:
    if not date:
        return f"ytarchive:{v_id_or_url}"
    return f"ytarchive:{v_id_or_url}:{date}"

def get_archiveorg_url(v_id: str, date: int|str|None = None) -> str:
    if not date:
        return f"https://web.archive.org/https://www.youtube.com/watch?v={v_id}"
    return f"https://web.archive.org/web/{date}/https://www.youtube.com/watch?v={v_id}"

def get_archiveorg_video_url(video_id: str) -> str:
    return f"https://web.archive.org/web/2oe_/http://wayback-fakeurl.archive.org/yt/{video_id}"


# Extractors

def extract_flat_info(pl_url_or_id: str, opts: YT_DLP_Params|None = None) -> PL_InfoDict[V_InfoDict]:
    """ Get basic info from a youtube playlist, it must be available on youtube.

    Args:
        pl_url_or_id (str): Playlist url or id to extract
        opts (YT_DLP_Params, optional): Options to pass into YoutubeDL. Defaults to {}.
            Note 'skip_download', 'extract_flat' are forced.
    
    Returns:
        PL_InfoDict: Flat playlist info
    """
    if opts is None:
        opts = {}
    with YoutubeDL(opts | {
        'skip_download': 'True',
        'extract_flat': 'in_playlist',
        'writethumbnail': False, # playlist thumbnail
    }) as ydl:
        flat_info: PL_InfoDict[V_InfoDict] = ydl.extract_info(pl_url_or_id, download=False) # type: ignore

    if not flat_info:
        raise RuntimeError(f"Failed to extract flat playlist for {pl_url_or_id}. Check terminal for errors.")

    flat_info['info_level'] = PL_InfoLevel.FLAT.name
    
    now = utils.epoch_now()
    for entry in flat_info['entries']:
        entry.setdefault('epoch', flat_info.get('epoch', now))
        entry.setdefault('playlist_epoch', flat_info.get('epoch', now))
        entry['info_level'] = derive_v_info_level(entry).name
    return flat_info

def download_video(
        v_id: str,
        opts: YT_DLP_Params | None = None,
        yt: bool = True,
        wa: bool = True,
        download: bool = True,
) -> tuple[V_InfoDict|None, list[Exception], bool]:
    """ Downloads a video, using Youtube and/or WebArchive extractors

    Args:
        v_id (str): the id of the video
        opts (YT_DLP_Params, optional): any additional opts for the download. Defaults to {}.
        yt (bool, optional): Use `YoutubeIE`. Should be False if it is known to be unavailable. Defaults to True.
        wa (bool, optional): Use `YoutubeWebArchiveIE` fallback. Defaults to True.
        download (bool, optional): Whether to download the video. Defaults to True.

    Returns:
        tuple[V_InfoDict | dict | None, list[Exception], bool]:
        - video info, `None` if the vid is already in the archive
        - list of Exception objects
        - if extraction was successful
    """
    if opts is None:
        opts = {}
    if not is_id_like(v_id, is_video=True):
        raise ValueError(f"{v_id} does not resemble a video id")
    
    info: V_InfoDict = {} # type: ignore - init
    errors: list[Exception] = []
    if yt:
        try:
            with YoutubeDL(opts) as ydl:
                _info = ydl.extract_info(get_yt_video_url(v_id), download=download)
                if _info is None:
                    return None, errors, True # already downloaded
                info.update(_info) # type: ignore
                info['info_level'] = derive_v_info_level(info, check=False).name
                return info, errors, True
        except DownloadError as yt_err:
            # info['yt_unavailable_msg'] = yt_err.msg
            info.setdefault('unavailable_msgs', []).append({
                'epoch': utils.epoch_now(),
                'msg': yt_err.msg,
                'type': 'youtube',
            })
            errors.append(yt_err)
        except Exception as e:  # noqa: BLE001 - catch any yt_dlp exception
            errors.append(e)
    if wa:
        try:
            with YoutubeDL(opts) as ydl:
                _info = ydl.extract_info(get_archiveorg_url(v_id), download=download)
                if _info is None:
                    return None, errors, True # already downloaded
                info.update(_info) # type: ignore
                info['info_level'] = derive_v_info_level(info, check=False).name
                return info, errors, True
        except DownloadError as wa_err:
            # info['wa_unavailable_msg'] = wa_err.msg
            info.setdefault('unavailable_msgs', []).append({
                'epoch': utils.epoch_now(),
                'msg': wa_err.msg,
                'type': 'web.archive:youtube',
            })
            errors.append(wa_err)
        except Exception as e:  # noqa: BLE001 - catch any yt_dlp exception
            errors.append(e)
    info['info_level'] = derive_v_info_level(info, check=False).name
    return info, errors, False

def download_video_generic(url: str, opts: YT_DLP_Params, download: bool) -> tuple[V_InfoDict|None, Exception|DownloadError|None, bool]:
    """
    Tries to download the video given the url using yt_dlp
    Returns the resulting infodict and the download info
    """
    info: V_InfoDict = {'info_level': V_InfoLevel.NONE} # type: ignore - init
    now = utils.epoch_now()

    try:
        with YoutubeDL(opts) as ydl:
            info: V_InfoDict = ydl.extract_info(url, download=download) # type: ignore
    except DownloadError as dl_err:
        info['unavailable_msgs'] = [{
            'epoch': now,
            'msg': dl_err.msg,
            'type': utils.get_domain(url) or url,
        }]
        return (info, dl_err, False)
    except Exception as e:  # noqa: BLE001 - catch any yt_dlp exception
        info['unavailable_msgs'] = [{
            'epoch': now,
            'msg': repr(e),
            'type': utils.get_domain(url) or url,
        }]
        return (None, e, False)
    
    if not info:
        return (None, None, True)
    info['info_level'] = derive_v_info_level(info, check=False).name
    return (info, None, True)



# Extraction Availability

def _maybe_available_on_yt(info: V_InfoDict | dict) -> bool:
    """ Returns True if unsure """
    # 'ie_key' occurs in flat info, but flat will only use youtube - OK.
    if info.get('extractor_key') == 'YoutubeWebArchive':
        return True
    # incomplete extract (many other stats could be used like `duration`)
    return info.get('channel') is not None

def _has_extracted_info(info: V_InfoDict | dict) -> bool:
    return bool(info.get('extractor'))

def _has_download_info(info: V_InfoDict | dict) -> bool:
    return bool(info.get("requested_downloads"))

def derive_v_info_level(v_info: V_InfoDict|dict|None, check: bool = True) -> V_InfoLevel:
    if not v_info:
        return V_InfoLevel.NONE

    expected = v_info.get('info_level', None)
    res = None

    if _has_download_info(v_info):       res = V_InfoLevel.DOWNLOAD
    elif _has_extracted_info(v_info):    res = V_InfoLevel.EXTRACT
    elif _maybe_available_on_yt(v_info): res = V_InfoLevel.FLAT
    else: res = V_InfoLevel.NONE

    if expected is not None and res.name != expected and check:
        if res == V_InfoLevel.NONE and expected == 'FLAT':
            utils.WARNING(f"[from {utils.get_caller_function()}] Mismatching V_InfoLevel: {expected = } != {res.name} = got (possibly old unavail flat detected hardcoded to FlAT)")
        else:
            utils.WARNING(f"[from {utils.get_caller_function()}] Mismatching V_InfoLevel: {expected = } != {res.name} = got")

    return res

def derive_pl_info_level(pl_info: PL_InfoDict|dict|None, check: bool = True) -> PL_InfoLevel:
    if not pl_info:
        return PL_InfoLevel.NONE

    expected = pl_info.get('info_level', None)
    has_extracts = any(derive_v_info_level(entry) >= V_InfoLevel.EXTRACT for entry in pl_info.get('entries', []))
    has_merge_timeline = 'merge_timeline' in pl_info
    res = None
    match has_extracts, has_merge_timeline:
        case False, False: res = PL_InfoLevel.FLAT
        case False,  True: res = PL_InfoLevel.MERGE_FLAT
        case  True, False: res = PL_InfoLevel.NORMAL
        case  True,  True: res = PL_InfoLevel.MERGE

    if expected is not None and res.name != expected and check:
        utils.WARNING(f"[from {utils.get_caller_function()}] Mismatching PL_InfoLevel: {expected = } != {res.name} = got")

    return res



# Path helpers

def ytdlp_eval_tmpl(tmpl: str, info: ANY_InfoDict, alt_info: ANY_InfoDict|None = None) -> str:
    """ Creates a deepcopy with `alt_info` overriding `info` to call yt_dlp's ``evaluate_outtmpl()`` """
    if alt_info is None:
        alt_info = {}
    return YoutubeDL().evaluate_outtmpl(
        tmpl,
        copy_and_sanitize_info(info | alt_info, wrap=True), # type: ignore
        sanitize=True)



# Processing archives

def copy_and_sanitize_info[T](_info_dict: T, remove_private_keys=False, wrap: bool = True) -> T|Any:
    """
    Creates a json-dumpable deepcopy of the info_dict.
    
    Keeps: `dict, list, str, int, float, bool`
    (`tuple, set, LazyList`) -> `list`
    non-basic types use `repr()`

    Never removes 'entries' kval.
    """
    KEY = None
    if wrap or not isinstance(_info_dict, dict):
        KEY = '__copy_and_sanitize_info__'
        info_dict = {KEY: _info_dict}
    else:
        info_dict = _info_dict
    
    info_dict = YoutubeDL.sanitize_info(info_dict, False) # type: ignore
    if KEY:
        info_dict = info_dict[KEY] # type: ignore

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



def ids_from_yt_dlp_archive(l: YT_DLP_DownloadArchive) -> list[V_ID]:
    EXTRACTORS_WITH_YT_IDS = {'youtube', 'youtubewebarchive', '__pldl_yt_dlp_generic__'}
    return [tup[1] for tup in l if tup[0] in EXTRACTORS_WITH_YT_IDS]

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
    for epoch in sorted(history.keys(), key=from_readable_epoch): # oldest -> newest
        for k, ids in ids_from_pl_download_info(history[str(epoch)]).items():
            merged[k].extend(ids)
    return merged


def get_pl_v_info(pl_info: PL_InfoDict, v_idx: int):
    return {
        'playlist_id':                  pl_info['id'],
        'playlist':                     pl_info.get('title') or pl_info['id'],
        'playlist_count':               pl_info.get('playlist_count'),
        'n_entries':                    pl_info.get('playlist_count'),
        'playlist_index':               v_idx,
        'playlist_autonumber':          v_idx,
        'playlist_title':               pl_info.get('title'),
        'playlist_channel':             pl_info.get('channel'),
        'playlist_channel_id':          pl_info.get('channel_id'),
        'playlist_uploader':            pl_info.get('uploader'),
        'playlist_uploader_id':         pl_info.get('uploader_id'),
        'playlist_webpage_url':         pl_info.get('webpage_url') or pl_info.get('original_url') or pl_info.get('url'),

        # custom
        'playlist_epoch': get_epoch(pl_info)
    }

def fixup_v_info(v_info: V_InfoDict):
    v_info['info_level'] = derive_v_info_level(v_info, check=False).name

def _fixup_pl_v_infos(pl_info: PL_InfoDict):
    for i, entry in enumerate(pl_info['entries']):
        entry.update(get_pl_v_info(pl_info, i)) # type: ignore
        fixup_v_info(entry)

def fixup_pl_info(pl_info: PL_InfoDict, fixup_entries: bool = True):
    pl_info['playlist_count'] = len(pl_info['entries'])
    if fixup_entries:
        _fixup_pl_v_infos(pl_info)
    pl_info['info_level'] = derive_pl_info_level(pl_info, check=False).name


# Technical/transient errors that don't confirm if the video is unavailable.
MISC_ERRORS = {
    r'.*Read timed out.*timeout=[\d\.]+': 'timed_out',
    r'^Postprocessing.*': 'postprocessing',
    r'.*HTTP Error 403: Forbidden': 'http_403',
}

# Errors that confirm that the video is actually unavailable on that platform.
UNAVAILABLE_PATTERNS = (
    r'.*[Vv]ideo unavailable.*',                                # yt: unavailable / takedown / terminated
    r'.*has been removed for violating.*Terms of Service.*',    # yt: ToS removal (doesn't say "unavailable")
    r'.*[Pp]rivate video.*',                                    # yt: private
    r'.*[Pp]lease sign in.*',                                   # yt: private video
    r'.*not archived or indexed.*',                             # wa: not indexed
)


def interpret_error_msg(yt_dlp_error_msg: str) -> tuple[str, bool]:
    """ returns (reason, is_unavailable) """

    tag = ""
    body = yt_dlp_error_msg

    if match := re.match(r".*\[([^\[]+?)\].*", yt_dlp_error_msg):
        tag = match.group(1)

    if match := re.match(r"(?:\u001b\[0;31mERROR:\u001b\[0m )(.+)", yt_dlp_error_msg):
        body = match.group(1)
    else:
        utils.WARNING(f"Unexpected yt_dlp error msg without ANSI prefix:\n{yt_dlp_error_msg!r}")

    if known_err := utils.regex_map(MISC_ERRORS, body, None):
        return known_err, False

    if any(re.match(p, body) for p in UNAVAILABLE_PATTERNS):
        return tag or body, True

    formatted_err = utils.hex(repr(yt_dlp_error_msg)[1:-1], fg="#E02B2B")
    utils.WARNING(f"Unrecognized yt_dlp error msg, treating as NOT confirmed-unavailable:\n'''{formatted_err}'''")
    return tag or body, False



# epoch stuff

# DO NOT CHANGE THESE!
DEFAULT_EPOCH: Callable[[],int] = lambda: -utils.epoch_now()
READABLE_EPOCH_FMT = '%Y-%m-%d__%H-%M-%S' # For formats, see datetime.strftime()
MALFORMED_EPOCH_FMT = '{} (malformed)'

assert MALFORMED_EPOCH_FMT.strip() != '{}', "MALFORMED_EPOCH_FMT must include non space characters eg '{}-bad'"
assert MALFORMED_EPOCH_FMT.count('{}') == 1, "MALFORMED_EPOCH_FMT must include ONE {} to sub for EPOCH_FMT"
assert MALFORMED_EPOCH_FMT.count('__epoch_fmt_sub') == 0, "MALFORMED_EPOCH_FMT cannot include '__epoch_fmt_sub' for internal reasons"

def get_epoch(info: V_InfoDict|PL_InfoDict|dict) -> int:
    return info.get('epoch', DEFAULT_EPOCH())

def get_latest_epoch(pl_info: PL_InfoDict) -> int:
    """
    Max 'epoch' in pl_info and its entries.

    A negative epoch means the epoch wasn't found or all were malformed.
    """
    latest = max(
        pl_info.get('epoch', float('-inf')),
        max((entry.get('epoch', float('-inf')) for entry in pl_info['entries']), default=float('-inf')))
    if latest == float('-inf'):
        latest = DEFAULT_EPOCH()
        utils.WARNING(f"All epochs are malformed or missing: {latest}")
    return int(latest)

# note: yt-dlp can handle 0 and negative epochs. It just keeps going into the past.
def to_readable_epoch(epoch: int) -> str:
    # low epochs can be invalid because of timezones.
    # So, exclude the first 24 hours from the start of the epoch

    is_negative = epoch < 0

    if abs(epoch) <= 3600 * 24:
        return MALFORMED_EPOCH_FMT.replace('{}', str(epoch))
    
    formatted = datetime.datetime.fromtimestamp(abs(epoch)).astimezone(None).strftime(READABLE_EPOCH_FMT)
    if is_negative:
        return MALFORMED_EPOCH_FMT.replace('{}', '-'+formatted)
    return formatted

def from_readable_epoch(readable: str) -> int:

    # make sure 
    MALFORMED_EPOCH_RE = '^'+ re.escape(MALFORMED_EPOCH_FMT.replace('{}', '__epoch_fmt_sub')).replace('__epoch_fmt_sub', '(-?)(.+)') +'$'
    LOW_EPOCH_RE = '^'+ re.escape(MALFORMED_EPOCH_FMT.replace('{}', '__epoch_fmt_sub')).replace('__epoch_fmt_sub', r'(-?\d+)') +'$'

    match = re.match(LOW_EPOCH_RE, readable)
    if match:
        return int(match.groups()[0])
    
    match = re.match(MALFORMED_EPOCH_RE, readable)
    is_negative = 1
    if match:
        readable = match.groups()[1]
        is_negative = -1 if bool(match.groups()[0]) else 1
    
    try:
        epoch = int(datetime.datetime.strptime(readable, READABLE_EPOCH_FMT).astimezone(None).timestamp())
        return is_negative * epoch
    except Exception:  # noqa: BLE001 - don't raise
        ...

    try:
        return int(readable)
    except ValueError:
        raise ValueError(f"{readable} is not a recognized readable epoch")



def min_v_info(id: str, info_level: V_InfoLevel, other_info: pldl_types._V_InfoDict_NoReqs|None = None) -> V_InfoDict:
    if other_info is None:
        other_info = {}
    return {
        **other_info,
        'id': id,
        'info_level': info_level.name,
    }

def min_pl_info(id: str, info_level: PL_InfoLevel, other_info: pldl_types._PL_InfoDict_NoReqs|None = None) -> PL_InfoDict:
    if other_info is None:
        other_info = {}
    return {
        **other_info,
        'id': id,
        'entries': [],
        'info_level': info_level.name
    }
