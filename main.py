from yt_types import *
from config import Config_IdentType, PlaylistDL_Config
from playlist_downloader import PlaylistDL
import utils
import yt_utils
import post_processing

# TODO:
# Remove yt_dlp archive - already have custom archiving
# Add post processing for filtering pl_info (eg especially `heatmap` and `automatic_captions`)

def wrapper_match_filter(
    pl_v_info: PL_V_InfoDict,
    curr_dl_info: PL_DownloadInfo,
    history: PL_DownloadHistory,
    history_ids: ID_DownloadInfo,
    ytdlp: YT_DLP_DownloadArchive,
    ytdlp_ids: YT_DLP_DownloadArchive_IDs,
) -> DL_Action:

    if pl_v_info['id'] in DOWNLOAD_OVERIDE:
        return DL_Action.DOWNLOAD
    if pl_v_info['id'] in EXTRACT_OVERIDE:
        return DL_Action.EXTRACT

    curr_dl_ids = yt_utils.ids_from_pl_download_info(curr_dl_info)
    
    if len(curr_dl_ids['download']) >= 1 or len(curr_dl_ids['extract']) >= 3:
        return DL_Action.QUIT
    
    if pl_v_info['id'] in history_ids['download']:
        return DL_Action.SKIP

    # only skip if the fail was in the last week
    if pl_v_info['id'] in history_ids['fail']:
        for epoch in history:
            if int(epoch) < utils.epoch_now() - 7*24*3600:
                continue
            for dl_info in history[str(epoch)]:
                if dl_info['id'] == pl_v_info['id']:
                    return DL_Action.SKIP
    
    if (pl_v_info.get('view_count') or 0) < 1_000_000:
        return DL_Action.DOWNLOAD

    if pl_v_info['id'] in history_ids['extract']:
        return DL_Action.SKIP

    return DL_Action.EXTRACT



EXTRACT_OVERIDE = ['']
DOWNLOAD_OVERIDE = ['']

config = PlaylistDL_Config(
    ident='test/jyes [...A-E9x23WGD3]/_metadata.json',
    ident_type=Config_IdentType.METADATA_PATH,
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
PlaylistDL(config)
