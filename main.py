from yt_types import *
from config import Config_IdentType, PlaylistDL_Config
from playlist_downloader import PlaylistDL
import utils
import yt_utils
import post_processing

def wrapper_match_filter(
    pl_v_info: PL_V_InfoDict,
    curr_dl_info: PL_DownloadInfo,
    history: PL_DownloadHistory,
    history_ids: ID_DownloadInfo,
    ytdlp: YT_DLP_DownloadArchive,
    ytdlp_ids: YT_DLP_DownloadArchive_IDs,
) -> DL_Action:
    """
    1 download OR 3 extracts per run,
    skip if already downloaded,
    download if under 1,000,000 views,
    else extract once.
    """
    return DL_Action.USER
    curr_dl_ids = yt_utils.ids_from_pl_download_info(curr_dl_info)

    if len(curr_dl_ids['download']) >= 1 or len(curr_dl_ids['extract']) >= 3:
        return DL_Action.QUIT

    if pl_v_info['id'] in history_ids['download']:
        return DL_Action.SKIP
    if (pl_v_info['view_count'] or 0) < 1_000_000:
        return DL_Action.EXTRACT

    if pl_v_info['id'] not in history_ids['extract']:
        return DL_Action.EXTRACT

    return DL_Action.SKIP

config = PlaylistDL_Config(
    ident='test/Night drive [...RFS3QSOhDMk]/_metadata.json',
    ident_type=Config_IdentType.METADATA_PATH,

    # cookie_file='secrets/cookie_file.txt',
    # cookies_for_pl=True,
    # cookies_for_v=False,
    # empty_cookies=True,
    
    write_flat=False,
    write_pl_info=True,
    write_merge=True,

    wrapper_match_filter=wrapper_match_filter,
)
PlaylistDL(config)
