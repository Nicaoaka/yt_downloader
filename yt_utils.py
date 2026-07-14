from yt_dlp import YoutubeDL
from yt_dlp.extractor.youtube import YoutubePlaylistIE

from yt_types import *

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
    return f'https://www.youtube.com/watch?v={video_id}'

def get_yt_playlist_url(playlist_id: str, video_id: str = '') -> str:
    if not video_id:
        return f'https://www.youtube.com/playlist?list={playlist_id}'
    return f'https://www.youtube.com/watch?v={video_id}&list={playlist_id}'

def get_archiveorg_url(v_id: str, date: int|str|None = None, for_yt_dlp: bool = False) -> str:
    if not date:
        if for_yt_dlp:
            return 'ytarchive:' + v_id
        return f"https://web.archive.org/https://www.youtube.com/watch?v={v_id}"
    if for_yt_dlp:
        return f'ytarchive:{v_id}:{date}'
    return f'https://web.archive.org/web/{date}/https://www.youtube.com/watch?v={v_id}'

def get_archiveorg_video_url(video_id: str) -> str:
    return f"https://web.archive.org/web/2oe_/http://wayback-fakeurl.archive.org/yt/{video_id}"



# Path helpers

def ytdlp_eval_tmpl(tmpl: str, info: InfoDict):
    return YoutubeDL().evaluate_outtmpl(tmpl, info, True) # type: ignore

def eval_with_dif_epoch(info: InfoDict, repl_epoch: int, tmpl: str):
    """ Temporarily swaps 'epoch' for outtmpl eval """
    __temp = info.get('epoch')
    info['epoch'] = repl_epoch
    path = ytdlp_eval_tmpl(tmpl, info)
    if __temp:
        info['epoch'] = __temp
    else:
        info.pop('epoch')
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



def get_v_info_level(v_info: V_InfoDict|None) -> _V_InfoLevel:
    """ Webarchive could appear at Download or Extract """
    if not v_info:                    return _V_InfoLevel.NONE
    if has_download_info(v_info):     return _V_InfoLevel.DOWNLOAD
    if has_extracted_info(v_info):    return _V_InfoLevel.EXTRACT
    if maybe_available_on_yt(v_info): return _V_InfoLevel.FLAT
    return _V_InfoLevel.UNAVAIL_YT

def get_pl_info_level(pl_info: PL_InfoDict|None) -> _PL_InfoLevel:
    if not pl_info or not pl_info.get('entries'): return _PL_InfoLevel.NONE
    if pl_info.get('merge_timeline'):             return _PL_InfoLevel.MERGED
    if any(get_v_info_level(entry) >= _V_InfoLevel.EXTRACT for entry in pl_info['entries']):
        return _PL_InfoLevel.NORMAL
    return _PL_InfoLevel.FLAT

# Processing archives

def ids_from_ytdlp_archive(l: YT_DLP_DownloadArchive) -> list[V_ID]:
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

