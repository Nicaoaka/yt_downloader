from yt_types import *
import yt_types
from yt_wrapper import DL
import utils
from collections import defaultdict

# TODO: Add paths to config
# currently in `main.py` and `yt_wrapper.py`

# HOME = r'C:\Users\nicol\Videos\yt-dlp'
HOME = r'test'
PL_ID_OR_PATH = "test/The Verge of Impossibility [...3Cfmpjqm-Pa]/Infojson/2026-07-02 08-08-52.json"
# PL_ID_OR_PATH = "PLXOfMLBzXbbX0Gx-BJaE5t3Cfmpjqm-Pa"
REFRESH_AFTER = 86400 # in seconds
# COOKIE_FILE: str|None = r'secrets/cookie_file.txt'
COOKIE_FILE: str|None = None

DELETE_COOKIES: bool = False
WRITE_FLAT: bool = True
WRITE_PL_INFO: bool = True
WRITE_BEST: bool = True


merged_history: PL_DownloadInfo = {} # type: ignore - init inside of wrapper
def wrapper_match_filter(
        pl_v_info: PL_V_InfoDict,
        curr: PL_DownloadInfo,
        history: dict[int, PL_DownloadInfo],
        ytdlp: YT_DLP_DownloadArchive,
) -> DL:
    """ Custom Filter

    Args:
        pl_v_info (PL_V_InfoDict): Flat playlist video info (fairly limited)
        curr (DownloadInfo): Info about current run's downloads/extracts
        history (dict[EPOCH, DownloadInfo]): Info of all recorded downloads/extracts
        ytdlp (YT_DLP_DownloadArchive): yt-dlp's download archive format: list[ tuple[youtube|youtubewebarchive, v_id], ]

    Returns:
        DL (Download options):
            - SKIP
            - EXTRACT
            - DOWNLOAD
            - QUIT
            - USER: [prompt for one of the 4 other options]
    """

    global merged_history
    if not merged_history:
        merged_history = utils.merge_history(history)

    # when to stop?
    # after 1 download or 3 extracts.
    if len(curr['download']) >= 1 or len(curr['extract']) >= 3:
        return DL.QUIT
    
    # download? - only if under 1_000_000 views
    if pl_v_info['id'] in merged_history['download']:
        return DL.SKIP
    if (pl_v_info['view_count'] or 0) < 1_000_000: # probably safe
        return DL.DOWNLOAD
    
    # extract? - if not already extracted
    if pl_v_info['id'] not in merged_history['extract']:
        return DL.EXTRACT
    
    return DL.SKIP

def yt_dlp_match_filter(v_info: V_InfoDict, *, incomplete: bool) -> str|None:
    """
    - If it returns a message (`anything`), the video is ignored.
    - If it returns `None`, the video is downloaded.
    - If it returns `utils.NO_DEFAULT`, the user is interactively
        asked whether to download the video.
    - `Raise utils.DownloadCancelled(msg)` to abort remaining
        downloads when a video is rejected.
        > USE `DL.QUIT` in ``wrapper_match_filter`` instead !!!
    """
    
    return None


"""
If `outtmpl` or `download_archive` need to be changed,
do that in ``edit_final_opts()`` or ``edit_final_opts_in_place()``
because the generated `paths` overwrite those keys.
"""
OPTS: YT_DLP_Params = {
    'quiet': False,
    'verbose': False,
    'clean_infojson': False,
    'sleep_interval': 3,
    'max_sleep_interval': 10,
    'ratelimit': 3_000_000,
    'remote_components': {'ejs:npm'},


    # Embed metadata
    'postprocessors': [ {'already_have_subtitle': False,
                        'key': 'FFmpegEmbedSubtitle'},
                        {'add_chapters': True,
                        'add_infojson': 'if_exists',
                        'add_metadata': True,
                        'key': 'FFmpegMetadata'},
                        {'already_have_thumbnail': False, 'key': 'EmbedThumbnail'}
    ],

    'writeautomaticsub': False,
    'subtitleslangs': ['ja*', 'en*', '日本語', '英語', '-live_chat'],
    'writesubtitles': True,
    'writethumbnail': True,
    # 'merge_output_format': 'mp4',
}


# in-place occurs first
def edit_final_opts_in_place(opts: YT_DLP_Params) -> None:
    return None
def edit_final_opts(opts: YT_DLP_Params) -> YT_DLP_Params:
    return opts





# Only change the below if you know what you are doing
# (will require *manually* updating previously downloaded playlists)
INDIVIDUAL_VIDEO_FOLDERS = False
ARCHIVE_FN = '_ytlp_archive.txt'
METADATA_FN = '_metadata.json'
