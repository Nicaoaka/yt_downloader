from pldl import *

"""
TODO:
- Ability to mixin downloads from other sources, eg vimeo (see ``yt_wrapper.download_video_alt()``)
"""

def wrapper_match_filter(
    pl_v_info: PL_V_InfoDict,
    curr_dl_info: PL_DownloadInfo,
    history: PL_DownloadHistory,
    history_ids: ID_DownloadInfo,
    ytdlp: YT_DLP_DownloadArchive,
    ytdlp_ids: YT_DLP_DownloadArchive_IDs,
) -> DL_Action:
        
    # already downloaded - would be skipped by yt-dlp anyway from download_archive
    if pl_v_info['id'] in history_ids['download'] or pl_v_info['id'] in ytdlp_ids:
        return DL_Action.SKIP
    
    if pl_v_info['id'] in DOWNLOAD_OVERRIDE:
        return DL_Action.DOWNLOAD
    
    if pl_v_info['id'] in history_ids['fail']:
        for epoch in history:
            # ignore dl_info older than a week
            if int(epoch) < utils.epoch_now() - 7*24*3600:
                continue
            # skip if failed in that time
            for dl_info in history[str(epoch)]:
                if dl_info['result'] in (DL_Result.FAIL) and dl_info['id'] == pl_v_info['id']:
                    return DL_Action.SKIP
    
    if pl_v_info['id'] in EXTRACT_OVERRIDE:
        return DL_Action.EXTRACT
    
    curr_dl_ids = yt_utils.ids_from_pl_download_info(curr_dl_info)
    if len(curr_dl_ids['download']) >= MAX_DOWNLOADS or len(curr_dl_ids['extract']) >= MAX_EXTRACTS:
        return DL_Action.SKIP
        
    if (pl_v_info.get('view_count') or 0) < 100_000:
        return DL_Action.DOWNLOAD
    
    if pl_v_info['id'] not in history_ids['extract']:
        return DL_Action.EXTRACT
    
    return DL_Action.SKIP

# OVERRIDEs take presedence over ALL, but yt_dlp download archive
# An attempt will be made every run, regardless of the MAXs.
DOWNLOAD_OVERRIDE = []
EXTRACT_OVERRIDE  = []
MAX_DOWNLOADS = 1
MAX_EXTRACTS = 3

config = PlaylistDL_Config(
    ident=r'Lists 3/Weird chill [...yvgAK80GYjv]/flat/2026-07-14 08-49-04.flat.json',
    ident_type=Config_IdentType.PL_INFO_PATH,
    home='Lists 3',

    # cookie_file='secrets/cookie_file.txt',
    # cookies_for_pl=True,
    # cookies_for_v=False,
    # empty_cookies=True,
    
    write_flat=True,
    write_pl_info=True,
    write_merge=True,

    wrapper_match_filter=wrapper_match_filter,
)

PlaylistDL(config)
