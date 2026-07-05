__all__ = [
    'HOME', 'PLAYLIST_IDENTIFIER', 'REFRESH_AFTER',
    'COOKIE_FILE', 'DELETE_COOKIES',
    'WRITE_FLAT', 'WRITE_PL_INFO', 'WRITE_MERGE',

    'wrapper_match_filter', 'yt_dlp_match_filter',

    'OPTS',
    'edit_final_opts_in_place', 'edit_final_opts',

    'PATH_TMPLS',
]

from yt_types import *
import yt_types
import utils
import pprint



HOME = r'test'
# playlist id or any info/metadata path
PLAYLIST_IDENTIFIER = "test/The Verge of Impossibility [...3Cfmpjqm-Pa]/flat/2026-07-03 07-43-12.flat.json"
# PL_ID_OR_PATH = "PLXOfMLBzXbbX0Gx-BJaE5t3Cfmpjqm-Pa"
REFRESH_AFTER = 86400 # in seconds, only used if a path is provided
# COOKIE_FILE: str|None = r'secrets/cookie_file.txt'
COOKIE_FILE: str|None = None

DELETE_COOKIES: bool = False
WRITE_FLAT: bool = True
WRITE_PL_INFO: bool = True
WRITE_MERGE: bool = True


id_history: ID_DownloadInfo = {} # type: ignore - init inside of wrapper
def wrapper_match_filter(
        pl_v_info: PL_V_InfoDict,
        curr: PL_DownloadInfo,
        history: dict[yt_types.EPOCH_STR, PL_DownloadInfo],
        ytdlp: YT_DLP_DownloadArchive,
) -> DL_Action:
    """ Custom Filter

    Args:
        pl_v_info (PL_V_InfoDict): Flat playlist video info (fairly limited)
        curr (DownloadInfo): Info about current run's downloads/extracts
        history (dict[EPOCH, DownloadInfo]): Info of all recorded downloads/extracts
        ytdlp (YT_DLP_DownloadArchive): yt-dlp's download archive format: list[ tuple[youtube|youtubewebarchive, v_id], ]

    Returns:
        DL_Action (Download options):
            - SKIP
            - EXTRACT
            - DOWNLOAD
            - QUIT
            - USER : [prompt for one of the 4 other options]
    """

    global id_history
    if not id_history:
        id_history = utils.ids_from_history(history)
    
    id_curr = utils.ids_from_download_info(curr)

    # when to stop?
    # after 1 download or 3 extracts.
    if len(id_curr['download']) >= 1 or len(id_curr['extract']) >= 3:
        return DL_Action.QUIT
    
    # download? - only if under 1_000_000 views
    if pl_v_info['id'] in id_history['download']:
        return DL_Action.SKIP
    if (pl_v_info['view_count'] or 0) < 1_000_000:
        return DL_Action.EXTRACT
    
    # extract? - if not already extracted
    if pl_v_info['id'] not in id_history['extract']:
        return DL_Action.EXTRACT
    
    return DL_Action.SKIP

def yt_dlp_match_filter(v_info: V_InfoDict, *, incomplete: bool) -> str|None:
    """
    - If it returns a message (`anything`), the video is ignored.
    - If it returns `None`, the video is downloaded.
    - If it returns `utils.NO_DEFAULT`, the user is interactively asked whether to download the video.
    - `Raise utils.DownloadCancelled(msg)` to abort remaining downloads when a video is rejected.
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
    'sleep_interval': 3,
    'max_sleep_interval': 10,
    'ratelimit': 3_000_000,
    'remote_components': {'ejs:npm'},
    'match_filter': yt_dlp_match_filter, # type: ignore

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

"""
Only change the below if:
    `Fresh` playlist download
        OR
    `You know what you are doing`. You may need to `manually` update some files (esp metadata).

`Home` and `Playlist` are folders. All other items are files.

"""
PATH_TMPLS: CustomOuttmpl = {
    'Home': HOME,
    'Playlist': lambda pl_info: f'{pl_info['title'] or '[no title]'} [{utils.truncate(pl_info['id'], 11, end_in_max=False, trunc_start=True)}]',

    # Below will be relative to `Playlist`
    'video_file':       'Videos/%(title)s [%(id)s].%(ext)s',
    # 'video_file':        '%(title)s [%(id)s]/%(title)s.%(ext)s',
    # 'chapter':           '%(title)s [%(id)s]/%(section_number)03d %(section_title)s [%(id)s].%(ext)s',
    # 'subtitle':          '%(title)s [%(id)s]/subtitles/.%(ext)s',
    # 'thumbnail':         '%(title)s [%(id)s]/thumbnail.%(ext)s',
    # 'description':       '%(title)s [%(id)s]/description',
    # 'annotation':        '%(title)s [%(id)s]/annotations.xml',
    # 'link':              '%(title)s [%(id)s]/link.%(ext)s',

    'flat_infojson':        'flat/%(epoch>%Y-%m-%d %H-%M-%S)s.flat.json',
    'pl_infojson':      'playlist/%(epoch>%Y-%m-%d %H-%M-%S)s.info.json',
    'merge_infojson':      'merge/%(epoch>%Y-%m-%d %H-%M-%S)s.merge.json',

    'ytdlp_archive':    '_ytlp_archive.txt',
    'metadata':         '_metadata.json',
}

