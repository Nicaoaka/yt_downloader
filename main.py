from pldl import *

def wrapper_match_filter(
    pl_v_info: V_InfoDict,
    curr_dl_info: PL_DownloadInfo,
    history: PL_DownloadHistory,
    history_ids: ID_DownloadInfo,
    ytdlp: YT_DLP_DownloadArchive,
    ytdlp_ids: YT_DLP_DownloadArchive_IDs,
) -> DL_Action:
        
    
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
    
    # already downloaded - would be skipped by yt-dlp anyway from download_archive
    if pl_v_info['id'] in history_ids['download'] or pl_v_info['id'] in ytdlp_ids:
        return DL_Action.SKIP
    
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
DOWNLOAD_OVERRIDE = ['KfEEm4Zx-EU']
EXTRACT_OVERRIDE  = []
MAX_DOWNLOADS = 1
MAX_EXTRACTS = 3

_config = PlaylistDL_Config(
    ident=r'Lists 4/Night drive [...RFS3QSOhDMk]/_metadata.json',
    ident_type=Config_IdentType.METADATA_PATH,
    home='Lists 4',

    # cookie_file='secrets/cookie_file.txt',
    # cookies_for_pl=True,
    # cookies_for_v=False,
    # empty_cookies=True,
    
    write_flat=True,
    write_raw_v_infos=True,
    write_pl_info=True,
    write_merge=True,

    wrapper_match_filter=wrapper_match_filter,
)

with PlaylistDL(_config) as pl_dl:
    pl_dl.download_v_infos()
    pl_dl.make_pl_info(delete_prev=True)
    pl_dl.make_merge_info(delete_prev=True)
