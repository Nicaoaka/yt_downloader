from __future__ import annotations

__all__ = [
    'PlaylistDL_Config', 'Config_IdentType',
    'wrapper_match_filter_builder',
]

import os
import dataclasses
from typing import Callable, Literal, Any, Iterable
from enum import StrEnum, auto

from pldl.utils import utils
from pldl.pldl_types import *
from pldl import yt_utils
from pldl.post_processing import filters

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


def wrapper_match_filter_builder(
    # these should never be 0, besides when quit_when_maxed is False 
    max_extracts: float = float('inf'),
    max_downloads: float = float('inf'),
    max_fails: float = float('inf'),

    # if True, not all unavailable vids will be seen and some overrides will not be reached
    quit_when_maxed: bool = False,

    extract_match: Callable[[V_InfoDict], bool]|None = None,
    download_match: Callable[[V_InfoDict], bool] = lambda v: (
               ((v.get('view_count') or 0) < 100_000) \
            and (v.get('duration') or 0) <=  5 * 60),

    overrides: dict[DL_Action, Iterable[V_ID]] = {},

    fail_backoff_time = 7 * 24 * 3600,

    yt_unavailable_action: DL_Action | None = DL_Action.DOWNLOAD,

    debug: bool = False,
):
    """ If `extract_match` is None (default), then it is the opposite of `download_match` """

    if extract_match is None:
        extract_match = lambda pl_v_info: not download_match(pl_v_info)

    if max_extracts < 0: raise ValueError("max_extracts must be >= 0")
    if max_downloads < 0: raise ValueError("max_downloads must be >= 0")
    
    _print = lambda s: print(utils.hex('>', fg="#FF9F21"), utils.hex(s, fg="#FFC478")) if debug else \
             lambda *args, **kwargs: None

    def wrapper_match_filter(
        pl_v_info: V_InfoDict,
        curr_dl_info: PL_DownloadInfo,
        history: PL_DownloadHistory,
        history_ids: ID_DownloadInfo,
        ytdlp: YT_DLP_DownloadArchive,
        ytdlp_ids: YT_DLP_DownloadArchive_IDs,
    ) -> DL_Action:

        # basic derived values
        v_id = pl_v_info['id']
        curr_dl_ids = yt_utils.ids_from_pl_download_info(curr_dl_info)
        likely_unavailable = pl_v_info.get('view_count') in (0, None)

        EXT_IS_MAXED = len(curr_dl_ids['extract']) >= max_extracts
        DL_IS_MAXED = len(curr_dl_ids['download']) >= max_downloads
        FAIL_IS_MAXED = len(curr_dl_ids['fail']) >= max_fails

        if quit_when_maxed:
            if EXT_IS_MAXED:
                _print("Maxed extract")
                return DL_Action.QUIT
            if DL_IS_MAXED:
                _print("Maxed downloads")
                return DL_Action.QUIT
            if FAIL_IS_MAXED:
                _print("Maxed fails")
                return DL_Action.QUIT


        
        # See DL_Action definition for order (order is top to bottom)
        # A v_id should only appear in one dl_action in the override anyway
        for action in DL_Action:
            if v_id in overrides.get(action, []):
                _print(f"{action} override")
                return action

        # Skip if failed and still in the backoff time
        # Applies to both download and extract
        for epoch in history:
            if yt_utils.from_readable_epoch(epoch) < (utils.epoch_now() - fail_backoff_time):
                continue
            for dl_info in history[str(epoch)]:
                if dl_info['id'] == v_id and dl_info['result'] == DL_Result.FAIL:
                    _print(f"Previous fail at {epoch}\n\t{dl_info.get('errors')}")
                    return DL_Action.SKIP

        # if a v_info could be downloaded or extracted,
        # download takes priority
        # unavailable ignores maxes
        if v_id not in history_ids['download'] or v_id not in ytdlp_ids:
            # not affected by download max
            if yt_unavailable_action == DL_Action.DOWNLOAD and likely_unavailable:
                _print("likely unavailable is DOWNLOAD")
                return DL_Action.DOWNLOAD
            if not DL_IS_MAXED and download_match(pl_v_info):
                _print("download match")
                return DL_Action.DOWNLOAD

        if v_id not in history_ids['extract']:
            # not affected by extract max
            if yt_unavailable_action == DL_Action.EXTRACT and likely_unavailable:
                _print("likely unavailable is EXTRACT")
                return DL_Action.EXTRACT
            if not EXT_IS_MAXED and extract_match(pl_v_info):
                _print("extract match")
                return DL_Action.EXTRACT

        return DL_Action.SKIP

    return wrapper_match_filter



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

        # Adjust epoch to local timezone (this is utc-7)
        # This will need adjusting if you have daylight savings
        # raw_video_infojson uses session start time for epoch
        # pl_infojson and merge_infojson use latest playlist/video epoch for epoch
        'raw_flat_infojson': "_flat\\%(epoch-25200>%Y-%m-%d %H-%M-%S)s.flat.json",
        'raw_video_infojson': "_v_infos\\%(epoch-25200>%Y-%m-%d %H-%M-%S)s.v_infos.json",
        '_merged_flat_infojson': "%(epoch-25200>%Y-%m-%d %H-%M-%S)s.merge.flat.json",
        'pl_infojson': "playlist\\%(epoch-25200>%Y-%m-%d %H-%M-%S)s.info.json",
        'merge_infojson': "%(epoch-25200>%Y-%m-%d %H-%M-%S)s.merge.json",

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

    The default will return False for operations that were cancelled.
    """
    return not dl_info['result'] == DL_Result.CANCELLED

def default_field_updater(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    from pldl.post_processing import merge_updaters
    return merge_updaters.COMMON_UPDATER(info, k, v, is_latest)

def default_update_filter(k: str) -> bool:
    return k in {
        'title',
        'description', 'categories', 'tags',
        'uploader', 'uploader_id', 'channel', 'creators', 'creator',
        'release_year', 'modified_date', 'availability',
        'extractor',
    }


@dataclasses.dataclass
class PlaylistDL_Config:

    
    # --- playlist identity / location (PICK ONLY ONE) ---
    ident: str
    ident_type: Config_IdentType
    home: str

    # --- refresh ---
    refresh_after: float = 7 * 24 * 3600  # seconds; if ident_type is Playlist_ID, it will extract
    force_flat_extract: bool = False
    base_info_type: Literal['any', 'latest_flat', 'merge_flat'] = 'merge_flat'
    
    # --- cookies ---
    cookie_file: str | None = None
    cookies_for_pl:    bool = True
    cookies_for_vids:  bool = False
    empty_cookies:     bool = True

    # --- what to persist ---
    write_flat:        bool = False
    write_raw_v_infos: bool = False
    write_pl_info:     bool = False
    write_merge:       bool = True
    
    # filters
    filter_flat_info:   Callable[[PL_InfoDict], None] = dataclasses.field(default=default_filter_flat_info)
    filter_pl_info:     Callable[[PL_InfoDict], None] = dataclasses.field(default=default_filter_pl_info)
    filter_merge_info:  Callable[[PL_InfoDict], None] = dataclasses.field(default=default_filter_merge_info)
    filter_all_info:    Callable[[PL_InfoDict|Any], None] = dataclasses.field(default=default_filter_all_info) # used after filter_flat, filter_normal, and filter_merge

    meta_dl_history_filter: Callable[[DownloadInfo], bool] = dataclasses.field(default=default_dl_info_filter)

    field_updater: Callable[[V_InfoDict | dict, str, Any | type[NO_VALUE], bool], bool] = default_field_updater
    update_filter: Callable[[str], bool] = default_update_filter

    # --- control hooks (override per-instance as needed) ---
    wrapper_match_filter: Callable[[
            V_InfoDict,
            PL_DownloadInfo,
            PL_DownloadHistory,     ID_DownloadInfo,
            YT_DLP_DownloadArchive, YT_DLP_DownloadArchive_IDs,
        ], DL_Action,
    ] = wrapper_match_filter_builder()
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

