from __future__ import annotations

__all__ = [
    'PlaylistDL_Config', 'Config_IdentType',
]

import os
import dataclasses
from typing import Callable, Literal, Any
from enum import StrEnum, auto

from .utils import utils
from ._types import *
from . import yt_utils
from .post_processing import filters

class Config_IdentType(StrEnum):
    """
    On the first run you must use `PL_ID_OR_URL`

    Otherwise, the preferred type is
    1. METADATA_PATH
    2. PL_INFO_PATH
    3. PL_ID_OR_URL
    """
    PL_ID_OR_URL  = auto()
    PL_INFO_PATH  = auto() # abs/rel path, is not effected by home
    METADATA_PATH = auto() # abs/rel path, is not effected by home 


def default_wrapper_match_filter(
    pl_v_info: V_InfoDict|dict,
    curr_dl_info: PL_DownloadInfo,
    history: PL_DownloadHistory,
    history_ids: ID_DownloadInfo,
    ytdlp: YT_DLP_DownloadArchive,
    ytdlp_ids: YT_DLP_DownloadArchive_IDs,
) -> DL_Action:
    """
    Per run
    QUIT: After 5 downloads OR 20 extracts
    DOWNLOAD: If <1,000,000 or unknown views
    EXTRACT: If not extracted yet
    SKIP: Otherwise
    """
    
    curr_dl_ids = yt_utils.ids_from_pl_download_info(curr_dl_info)
    if len(curr_dl_ids['download']) >= 5 or len(curr_dl_ids['extract']) >= 20:
        return DL_Action.QUIT

    # already downloaded - would be skipped by yt-dlp anyway from download_archive
    if pl_v_info['id'] in history_ids['download'] or pl_v_info['id'] in ytdlp_ids:
        return DL_Action.SKIP
    
    if pl_v_info['id'] in history_ids['fail']:
        for epoch in history:
            # ignore dl_info older than a week
            if int(epoch) < utils.epoch_now() - 7*24*3600:
                continue
            # skip if failed in the last week
            for dl_info in history[str(epoch)]:
                if dl_info['result'] in (DL_Result.FAIL) and dl_info['id'] == pl_v_info['id']:
                    return DL_Action.SKIP
    
    if (pl_v_info.get('view_count') or 0) < 1_000_000:
        return DL_Action.DOWNLOAD
    
    if pl_v_info['id'] not in history_ids['extract']:
        return DL_Action.EXTRACT
    
    return DL_Action.SKIP


def default_yt_dlp_match_filter(v_info: V_InfoDict, *, incomplete: bool) -> str | None:
    """
    `Prefer using wrapper_match_filter when possible`

    May be called multiple times for the same video.
    Extraction occurs before this is called, so it can only effect downloads.

    - Return a message to skip.
    - Return `None` to downloaded.
    - Return `yt_dlp.utils.NO_DEFAULT` to prompt user.
    (quitting the playlist can only occur in `wrapper_match_filter`)
    """
    return None



def default_opts() -> YT_DLP_Params:
    return {
        'quiet': False,
        'verbose': False,
        'sleep_interval': 3,
        'max_sleep_interval': 10,
        'ratelimit': 3_000_000,
        'remote_components': {'ejs:npm'},

        'format': 'ba+bv/b',
        'format_sort': ['abr', 'res:1080', 'vbr', '+size', ],
        # default: lang,quality,res,fps,hdr:12,vcodec,channels,acodec,size,br,asr,proto,ext,hasaud,source,id

        'postprocessors': [
            {'already_have_subtitle': False, 'key': 'FFmpegEmbedSubtitle'},
            {'add_chapters': True, 'add_infojson': 'if_exists',
             'add_metadata': True, 'key': 'FFmpegMetadata'},
            {'already_have_thumbnail': False, 'key': 'EmbedThumbnail'},
        ],

        'clean_infojson': False,
        'writeautomaticsub': False,
        'subtitleslangs': ['ja*', 'en*', '日本語', '英語', '-live_chat'],
        'writesubtitles': True,
        'writethumbnail': True,
    }


def default_path_tmpls() -> CustomOuttmpl:
    """
    USE `\\` instead of `/`
    
    reference: https://github.com/yt-dlp/yt-dlp#output-template
    
    Defaults for outtmpl can be found in yt_dlp/utils/_utils.py in the symbol `OUTTMPL_TYPES`.
    """
    return {
        'Playlist': lambda pl_info: (
            f"{pl_info.get('title') or "[no title]"} "
            f"[{utils.truncate(pl_info['id'], 11, end_in_max=False, trunc_start=True)}]"
        ),

        'video_file': "Videos\\%(title)s [%(id)s].%(ext)s",

        'raw_flat_infojson': "_flat\\%(epoch>%Y-%m-%d %H-%M-%S)s.flat.json",
        'raw_video_infojson': "_v_infos\\%(epoch>%Y-%m-%d %H-%M-%S)s.v_infos.json", # uses latest v epoch within

        '_merged_flat_infojson': "%(epoch>%Y-%m-%d %H-%M-%S)s.merge.flat.json",
        'pl_infojson': "playlist\\%(epoch>%Y-%m-%d %H-%M-%S)s.info.json",
        'merge_infojson': "%(epoch>%Y-%m-%d %H-%M-%S)s.merge.json",

        'yt_dlp_archive': "_yt_dlp_archive.txt",
        'metadata': "_metadata.json",
    }


# all filters are in-place
def default_filter_flat_info(flat_info: PL_InfoDict) -> None:
    pass
def default_filter_pl_info(pl_info: PL_InfoDict) -> None:
    pass
def default_filter_merge_info(merge_info: PL_InfoDict) -> None:
    pass
def default_filter_all_info(info: PL_InfoDict|Any) -> None:
    """ Filter used by raw_flat, raw_v_infos, _merge_flat, pl_info, and merge_info """
    if not isinstance(info, dict):
        return
    filters.filter_pl_info(info, set(), {'automatic_captions'})


def default_dl_info_filter(dl_info: DownloadInfo) -> bool:
    """
    Return True to add to history

    The default will return False for operations that were intentionally skipped:
    - `SKIP -> CANCELLED`
    - `QUIT -> CANCELLED`
    """
    return not (
        dl_info['action'] in (DL_Action.SKIP, DL_Action.QUIT, ) and \
        dl_info['result'] in (DL_Result.CANCELLED, ))


@dataclasses.dataclass
class PlaylistDL_Config:

    
    # --- playlist identity / location (PICK ONLY ONE) ---
    ident: str
    ident_type: Config_IdentType
    home: str

    # --- refresh ---
    refresh_after: float = 7 * 24 * 3600  # seconds; if ident_type is Playlist_ID, it will extract
    base_info_type: Literal['any', 'latest_flat', 'merge_flat'] = 'merge_flat'
    
    # --- cookies ---
    cookie_file: str | None = None
    cookies_for_pl:    bool = True
    cookies_for_vids:  bool = False
    empty_cookies:     bool = False

    # --- what to persist ---
    write_flat:        bool = False
    write_raw_v_infos: bool = False
    write_pl_info:     bool = False
    write_merge:       bool = True
    
    # filters
    filter_flat_info:   Callable[[PL_InfoDict], None] = dataclasses.field(default=default_filter_flat_info)
    filter_pl_info: Callable[[PL_InfoDict], None] = dataclasses.field(default=default_filter_pl_info)
    filter_merge_info:  Callable[[PL_InfoDict], None] = dataclasses.field(default=default_filter_merge_info)
    filter_all_info: Callable[[PL_InfoDict|Any], None] = dataclasses.field(default=default_filter_all_info) # used after filter_flat, filter_normal, and filter_merge

    meta_dl_history_filter: Callable[[DownloadInfo], bool] = dataclasses.field(default=default_dl_info_filter)

    # --- control hooks (override per-instance as needed) ---
    wrapper_match_filter: Callable[[
            V_InfoDict,
            PL_DownloadInfo,
            PL_DownloadHistory,     ID_DownloadInfo,
            YT_DLP_DownloadArchive, YT_DLP_DownloadArchive_IDs,
        ], DL_Action,
    ] = default_wrapper_match_filter
    yt_dlp_match_filter: Callable[..., str | None] = dataclasses.field(default=default_yt_dlp_match_filter)
    
    # --- yt-dlp params ---
    opts: YT_DLP_Params = dataclasses.field(default_factory=default_opts)

    # --- path templates ---
    path_tmpls: CustomOuttmpl = dataclasses.field(default_factory=default_path_tmpls)

    # --- testing opts ---
    _use_as_merge_flat: bool = False

    def __post_init__(self):
        """
        Validate inputs as much as possible.

        Cannot validate `paths_tmpls` here.
        If the playist identifier is an ID, the Playlist folder can't be resolved,
        so any existing metadata file can't be loaded.
        So the 
        """

        # ident
        match self.ident_type:
            case Config_IdentType.PL_ID_OR_URL:
                if not yt_utils.get_pl_id_from_yt_url(self.ident):
                    raise ValueError(f"{self.ident} wasn't recognized as a youtube playlist id or url")
                
            case Config_IdentType.PL_INFO_PATH:
                utils.assert_file(self.ident, "Playlist info path (ident)", min_size=1)
                pl_info = utils.json_load(self.ident)
                if missing := utils.get_missing_typeddict_keys(pl_info, PL_InfoDict):
                    raise ValueError(f"Playlist info path (ident) leads to malformed PL_InfoDict.\nMissing kvals: {missing}")
                
            case Config_IdentType.METADATA_PATH:
                if not os.path.exists(self.ident):
                    raise FileNotFoundError("Metadata path (ident) not found")
                yt_utils.validate_metdata_config_sync(utils.json_load(self.ident), self)

        # cookies
        utils.assert_file(self.cookie_file, 'cookie_file', min_size=1, None_is_ok=True)

        # opts
        if 'match_filter' in self.opts:
            raise ValueError(
                f"'match_filter' can not be set in `config.opts`.\n"
                f"Set `config.yt_dlp_match_filter` instead.")
        if 'cookiefile' in self.opts:
            raise ValueError(
                f"'cookiefile' can not be set in `config.opts`.\n"
                f"Set `config.cookie_file` or set the cookiefile in API args instead.")
        for k in ('outtmpl', 'download_archive'):
            if k in self.opts:
                raise ValueError(
                    f"'{k}' can not be set in `config.opts`.\n"
                    f"Set `config.path_tmpls` instead.")
        if 'paths' in self.opts and self.opts['paths'] and 'home' in self.opts['paths']:
            raise ValueError(
                f"'home' can not be set in `config.opts['paths']`.\n"
                f"Set `config.home` instead.")

# Do these need to be configurable?
DEFAULT_EPOCH: Callable[[],int] = lambda: -utils.epoch_now()
READABLE_EPOCH_FMT = '%Y-%m-%d__%H-%M-%S' # For formats, see datetime.strftime()
MALFORMED_EPOCH_FMT = '{} (malformed)'

def main():

    from pldl.utils.utils import hex
    import pprint

    example = PlaylistDL_Config(
        ident='LL',
        ident_type=Config_IdentType.PL_ID_OR_URL,
        home="example_home",
    )
    pprint.pprint(example, indent=4, width=20)
    required_fields = [
        repr(f.name) for f in dataclasses.fields(example)
        if (f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING)]
    print(hex(
        f"Note:\n"
        f"1. Required fields: {', '.join(required_fields)}\n"
        f"2. Generated opts:  'cookiefile', outtmpl', 'paths', 'download_archive'",
        "#4AA5FF"))

if __name__ == "__main__":
    main()

