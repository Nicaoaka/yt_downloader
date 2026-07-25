from pldl import *

# add ability to change id of certain video
#   dvyG8KWrB_E -> 62RUkX4AqyM
# test extraction/download from other sources
# test manipulations

def wrapper_match_filter(
    pl_v_info: V_InfoDict,
    curr_dl_info: PL_DownloadInfo,
    history: PL_DownloadHistory,
    history_ids: ID_DownloadInfo,
    ytdlp: YT_DLP_DownloadArchive,
    ytdlp_ids: YT_DLP_DownloadArchive_IDs,
) -> DL_Action:
    
    __V_ID__ = pl_v_info['id']
    
    if __V_ID__ in DOWNLOAD_OVERRIDE:
        return DL_Action.DOWNLOAD
    
    if __V_ID__ in EXTRACT_OVERRIDE:
        return DL_Action.EXTRACT


    curr_dl_ids = yt_utils.ids_from_pl_download_info(curr_dl_info)
    if QUIT_WHEN_MAXED and (len(curr_dl_ids['download']) >= MAX_DOWNLOADS or len(curr_dl_ids['extract'])  >= MAX_EXTRACTS):
        return DL_Action.QUIT
    
    # check for old failures
    if __V_ID__ in history_ids['fail']:
        for epoch in history:
            # ignore dl_info older than a week
            if int(epoch) < utils.epoch_now() - 7*24*3600:
                continue
            # skip if failed in that time
            for dl_info in history[str(epoch)]:
                if dl_info['result'] in (DL_Result.FAIL) and dl_info['id'] == __V_ID__:
                    return DL_Action.SKIP

    # already downloaded - would be skipped by yt-dlp anyway from download_archive
    if __V_ID__ in history_ids['download'] or __V_ID__ in ytdlp_ids:
        return DL_Action.SKIP

    likely_unavailable = (pl_v_info.get('view_count') or 0) == 0
    if YT_UNAVAILABLE_DL_ACTION is not None and likely_unavailable:
        return YT_UNAVAILABLE_DL_ACTION


    if len(curr_dl_ids['download']) < MAX_DOWNLOADS and \
       (pl_v_info.get('view_count') or 0) < 100_000 and \
       (pl_v_info.get('duration') or 0) <= 5*60:
        return DL_Action.DOWNLOAD
    
    if __V_ID__ in history_ids['extract']: return DL_Action.SKIP
    
    if len(curr_dl_ids['extract']) < MAX_EXTRACTS:
        return DL_Action.EXTRACT
    
    return DL_Action.SKIP

def yt_dlp_match_filter(v_info: V_InfoDict, *, incomplete: bool) -> str | None:
    """
    `Prefer using wrapper_match_filter when possible`

    May be called multiple times for the same video.
    Extraction occurs before this is called, so it can only effect downloads.

    - Return a message to skip.
    - Return `None` to downloaded.
    - Return `yt_dlp.utils.NO_DEFAULT` to prompt user.
    (quitting the playlist can only occur in `wrapper_match_filter`)
    """
    if (v_info.get('channel_follower_count') or 0) >= 1_000_000:
        return 'high sub count, likely archived'
    return None

EXTRACT_OVERRIDE: list[V_ID]  = []
DOWNLOAD_OVERRIDE: list[V_ID] = []
YT_UNAVAILABLE_DL_ACTION: DL_Action|None = DL_Action.DOWNLOAD # ignores MAXs

QUIT_WHEN_MAXED: bool = False # when either max is hit
MAX_EXTRACTS = 25
MAX_DOWNLOADS = 5

_config = PlaylistDL_Config(
    ident=r'c:\Users\nicol\Videos\yt-dlp\Watch later [...GmwOeRLrSVz]\_metadata.json',
    ident_type=Config_IdentType.METADATA_PATH,
    home='C:\\Users\\nicol\\Videos\\yt-dlp',

    # cookie_file='secrets/cookie_file.txt',
    # cookies_for_pl=True,
    # cookies_for_vids=False,
    # empty_cookies=True,
    
    write_flat=True,
    write_raw_v_infos=True,
    write_pl_info=True,
    write_merge=True,

    wrapper_match_filter=wrapper_match_filter,
    yt_dlp_match_filter=yt_dlp_match_filter,
)

with PlaylistDL(_config) as pl_dl:
    pl_dl.download_v_infos()
    pl_dl.make_pl_info()
    pl_dl.make_merge_info(delete_prev=True)
    pass
