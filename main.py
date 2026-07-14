from yt_types import *
from config import Config_IdentType, PlaylistDL_Config
from playlist_downloader import PlaylistDL
import utils
import yt_utils
import pp_utils
"""
TODO:
- Update `post_processing` merge functions

- Add post processing for filtering pl_info (eg especially `heatmap` and `automatic_captions`)
- Change ``yt_wrapper.download_pl_videos()`` to try download if there hasn't been a previous download fail (get yt_unavailabe_reason)
- Figure out what `DL_Result.NO_INFO` really means. Does it just represent hitting yt_dlp download_archive (cache)?

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
    
    if pl_v_info['id'] in history_ids['fail'] or pl_v_info['id'] in history_ids['no_info']:
        for epoch in history:
            # ignore dl_info older than a week
            if int(epoch) < utils.epoch_now() - 7*24*3600:
                continue
            # skip if failed in the last week
            for dl_info in history[str(epoch)]:
                if dl_info['result'] in (DL_Result.FAIL, DL_Result.NO_INFO) and dl_info['id'] == pl_v_info['id']:
                    return DL_Action.SKIP
    
    if pl_v_info['id'] in EXTRACT_OVERRIDE:
        return DL_Action.EXTRACT
    
    curr_dl_ids = yt_utils.ids_from_pl_download_info(curr_dl_info)
    if len(curr_dl_ids['download']) >= MAX_DOWNLOADS or len(curr_dl_ids['extract']) >= MAX_EXTRACTS:
        return DL_Action.SKIP
        
    if (pl_v_info.get('view_count') or 0) < 1_000_000:
        return DL_Action.DOWNLOAD
    
    if pl_v_info['id'] not in history_ids['extract']:
        return DL_Action.EXTRACT
    
    return DL_Action.SKIP

# `DOWNLOAD_OVERRIDE` does not override yt_dlp download archive
DOWNLOAD_OVERRIDE = []
EXTRACT_OVERRIDE  = []
MAX_DOWNLOADS = 1
MAX_EXTRACTS = 3

config = PlaylistDL_Config(
    ident='https://www.youtube.com/watch?v=UKXDb0INlCc&list=PLVw6cgrOWNXsFnOc3zpRqrQcfHZFo6S5U',
    ident_type=Config_IdentType.PL_ID_OR_URL,
    home='test',

    # cookie_file='secrets/cookie_file.txt',
    # cookies_for_pl=True,
    # cookies_for_v=False,
    # empty_cookies=True,
    
    write_flat=True,
    write_pl_info=True,
    write_merge=True,

    wrapper_match_filter=wrapper_match_filter,
)

# PlaylistDL(config)
