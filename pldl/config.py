from __future__ import annotations

__all__ = [
    'Config_IdentType',
    'PlaylistDL_Config',
]

import dataclasses
import os
import random
from collections.abc import Callable, Iterable
from enum import StrEnum, auto
from typing import Any

from pldl import yt_utils
from pldl.pldl_types import *
from pldl.post_processing import filters
from pldl.utils import utils


class Config_IdentType(StrEnum):
    """
    On the first run you must use `PL_ID_OR_URL`

    Otherwise, `METADATA_PATH` should be used when possible
    """
    PL_ID_OR_URL  = auto()
    METADATA_PATH = auto() # abs/rel path, is not effected by home 
    PL_INFO_PATH  = auto() # abs/rel path, is not effected by home

type V_DL_OrderManip = Callable[[
    list[tuple[int, V_InfoDict]]
], Iterable[tuple[int, V_InfoDict]]]
type WrapperMatchFilter = Callable[[
    V_InfoDict,
    PL_DownloadInfo,
    PL_DownloadHistory,     ID_DownloadInfo,
    YT_DLP_DownloadArchive, YT_DLP_DownloadArchive_IDs,
], DL_Action]


def default_yt_dlp_match_filter(v_info: V_InfoDict, *, incomplete: bool) -> str | None:
    """
    `Prefer using wrapper_match_filter when possible`, this should be set in opts

    May be called multiple times for the same video.
    Extraction occurs before this is called, so it can only effect downloads.

    - Return a message to skip.
    - Return `None` to downloaded.
    - Return `yt_dlp.utils.NO_DEFAULT` to prompt user.
    (quitting the playlist can only occur in `wrapper_match_filter`)
    """
    return None

def default_opts() -> YT_DLP_Params:
    def retry_sleep_func(n: int) -> int:
        return min((1+random.random()) * 2 ** n, 120) # wait exponentially longer, capped at 120x
    
    return {
        'quiet': False,
        'verbose': False,

        'sleep_interval': 5,
        'max_sleep_interval': 30,
        'sleep_interval_requests': 1,

        'retries': 3,
        'retry_sleep_functions': {
            'http': retry_sleep_func,      # type: ignore (default?)
            'fragment': retry_sleep_func,
            'extractor': retry_sleep_func, # type: ignore (file_access?)
        },

        'ratelimit': 5_000_000, # is this necessary?
        # 'max_downloads': 10,  # use wrapper_match_filter_builder

        'remote_components': {'ejs:npm'},

        # Prefer non-HLS (DASH) streams to avoid PTS/merge issues with itag 232 etc.
        'format': 'ba+bv[protocol!*=m3u8]/b[protocol!*=m3u8]/ba+bv/b',
        'format_sort': ['abr', 'res:1080', 'vbr', '+size'],

        'postprocessors': [
            {'already_have_subtitle': False, 'key': 'FFmpegEmbedSubtitle'},
            {'add_chapters': True, 'add_infojson': 'if_exists',
             'add_metadata': True, 'key': 'FFmpegMetadata'},
            {'already_have_thumbnail': False, 'key': 'EmbedThumbnail'},
        ],

        # Fallback safety net: if an HLS stream is unavoidable (no DASH equivalent),
        # regenerate missing presentation timestamps so the merger doesn't choke.
        'postprocessor_args': {
            'ffmpeg': ['-fflags', '+genpts'],
        },

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
    filters.filter_pl_info(info, set(), {'automatic_captions', 'formats'})


def default_dl_info_filter(dl_info: DownloadInfo) -> bool:
    """
    Return True to add to history

    The default will return False for operations that were cancelled.
    """
    return dl_info['result'] != DL_Result.CANCELLED

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
    
    # --- cookies ---
    cookie_file: str | None = None
    cookies_for_pl:    bool = True
    cookies_for_vids:  bool = False
    empty_cookies:     bool = True

    # --- what to persist ---
    write_raw_flat:    bool = False
    write_raw_v_infos: bool = False
    
    # filters
    filter_flat_info:   Callable[[PL_InfoDict], None] = dataclasses.field(default=default_filter_flat_info)
    filter_pl_info:     Callable[[PL_InfoDict], None] = dataclasses.field(default=default_filter_pl_info)
    filter_merge_info:  Callable[[PL_InfoDict], None] = dataclasses.field(default=default_filter_merge_info)

    # used after filter_flat, filter_normal, and filter_merge
    filter_all_info:    Callable[[PL_InfoDict|Any], None] = dataclasses.field(default=default_filter_all_info)

    meta_dl_history_filter: Callable[[DownloadInfo], bool] = dataclasses.field(default=default_dl_info_filter)
    
    # --- yt-dlp params ---
    opts: YT_DLP_Params = dataclasses.field(default_factory=default_opts)

    # --- path templates ---
    path_tmpls: CustomOuttmpl = dataclasses.field(default_factory=default_path_tmpls)

    # --- dev ---
    _no_yt_dlp_downloads: bool = False # like a testing mode

    def __post_init__(self):
        """
        Validate inputs as much as possible.

        Cannot validate `paths_tmpls` here.
        If the playlist identifier is an ID, the Playlist folder can't be resolved,
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
                from pldl.playlist_dl import PlaylistDL
                PlaylistDL._validate_metadata_config_sync(utils.json_load(self.ident), self)

        # cookies
        utils.assert_file(self.cookie_file, 'cookie_file', min_size=1, None_is_ok=True)

        # opts
        if 'cookiefile' in self.opts:
            raise ValueError(
                "'cookiefile' can not be set in `config.opts`.\n"
                "Set `config.cookie_file` or set the cookiefile in API args instead.")
        for k in ('outtmpl', 'download_archive'):
            if k in self.opts:
                raise ValueError(
                    f"'{k}' can not be set in `config.opts`.\n"
                    f"Set `config.path_tmpls` instead.")
        if 'paths' in self.opts and self.opts['paths'] and 'home' in self.opts['paths']:
            raise ValueError(
                "'home' can not be set in `config.opts['paths']`.\n"
                "Set `config.home` instead.")

def main():
    
    import pprint  # noqa: I001
    from pldl.utils.utils import hex

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

