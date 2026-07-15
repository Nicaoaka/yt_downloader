from __future__ import annotations

__all__ = [
    'PlaylistDL_Config', 'Config_IdentType',
]

import os
import dataclasses
from typing import Callable

from .utils import utils
from .yt_types import *
from . import yt_types
from . import yt_utils

# Do these need to be configurable?
DEFAULT_EPOCH: Callable[[],int] = lambda: -1
TIMELINE_EPOCH_FMT = '%Y_%m_%d__%H_%M_%S' # For formats, see datetime.strftime()


def default_merge_fallbacks() -> list[yt_types._MetadataFiles_Lit]:
    return [
        'latest_merge_info', # checked/used first
        'latest_pl_info',    # second
        'latest_flat_info',  # last
    ]


def default_wrapper_match_filter(
    pl_v_info: PL_V_InfoDict,
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
    (quitting the playlist can onnly occur in `wrapper_match_filter`)
    """
    return None


def default_edit_final_opts_in_place(opts: YT_DLP_Params) -> None:
    return None


def default_opts() -> YT_DLP_Params:
    return {
        'quiet': False,
        'verbose': False,
        'sleep_interval': 3,
        'max_sleep_interval': 10,
        'ratelimit': 3_000_000,
        'remote_components': {'ejs:npm'},
        'match_filter': default_yt_dlp_match_filter, # type: ignore

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
            f"{pl_info['title'] or "[no title]"} "
            f"[{utils.truncate(pl_info['id'], 11, end_in_max=False, trunc_start=True)}]"
        ),

        'video_file': "Videos\\%(title)s [%(id)s].%(ext)s",

        'flat_infojson': "flat\\%(epoch>%Y-%m-%d %H-%M-%S)s.flat.json",   # uses latest   pl epoch
        'pl_infojson': "playlist\\%(epoch>%Y-%m-%d %H-%M-%S)s.info.json", # uses latest v/pl epoch
        'merge_infojson': "%(epoch>%Y-%m-%d %H-%M-%S)s.merge.json",       # uses latest v/pl epoch

        'ytdlp_archive': "_ytdlp_archive.txt",
        'metadata': "_metadata.json",
    }


# all filters are in-place
def default_filter_flat(pl_info: PL_InfoDict):
    pass
def default_filter_normal(pl_info: PL_InfoDict):
    pass
def default_filter_merge(pl_info: PL_InfoDict):
    pass
def default_filter_common(pl_info: PL_InfoDict):
    from . import post_processing
    post_processing.filter_pl_info(pl_info, set(), {'automatic_captions'})


def default_dl_info_filter(dl_info: DownloadInfo) -> bool:
    """
    Return True to keep, False to filter out

    These skip when nothing happens, while still being a successful operation
    
    DL_Result.CACHED being in this category is debatable because
    the user-defined match filter chose to download even though it was already
    downloaded in the metadata history.
    """
    return dl_info['action'] not in (DL_Action.SKIP, DL_Action.QUIT) and \
           dl_info['result'] not in (DL_Result.CANCELLED)


def validate_metdata(metadata: Metadata, config: PlaylistDL_Config):
    for k in yt_types._MetadataFiles.__required_keys__:
        if metadata[k]:
            utils.assert_file(os.path.join(config.home, metadata['path_tmpls']['Playlist'], metadata[k]), f"{k} (metadata)", min_size=1)
    
    meta_path = os.path.join(config.home, metadata['path_tmpls'].get('Playlist', 'NA'), metadata['path_tmpls'].get('metadata', 'NA'))
    for k in metadata['path_tmpls'].keys() | config.path_tmpls.keys():
        if k == 'Playlist':
            continue # can't be checked without info
        if k not in metadata['path_tmpls']:
            raise ValueError(
                f"Missing key in metadata: {{{k!r}: {config.path_tmpls[k]!r}}}\n"
                f"Path: {meta_path}")
        if k not in config.path_tmpls:
            raise ValueError(
                f"Extra key in metdata: {{{k!r}: {metadata['path_tmpls'][k]!r}}}\n"
                f"Path: {meta_path}")
        if metadata['path_tmpls'][k] != config.path_tmpls[k]:
            raise ValueError(
                f"Changed `path_tmpls`: {repr(k)}:\n"
                f"metadata: {metadata['path_tmpls'][k]}\n"
                f"config:   {config.path_tmpls[k]}\n"
                f"Path: {meta_path}")


@dataclasses.dataclass
class PlaylistDL_Config:
    # --- playlist identity / location (PICK ONLY ONE) ---
    ident: str
    ident_type: Config_IdentType
    home: str

    # --- refresh ---
    refresh_after: int = 7 * 24 * 3600  # seconds; if ident_type is Playlist_ID, it will extract
    
    # --- cookies ---
    cookie_file: str | None = None
    cookies_for_pl:    bool = True
    cookies_for_v:  bool = False
    empty_cookies:     bool = False


    # --- what to persist ---
    write_flat:    bool = False
    write_pl_info: bool = False
    write_merge:   bool = True
    
    # filters
    filter_flat:   Callable[[PL_InfoDict]] = default_filter_flat
    filter_normal: Callable[[PL_InfoDict]] = default_filter_normal
    filter_merge:  Callable[[PL_InfoDict]] = default_filter_merge
    filter_common: Callable[[PL_InfoDict]] = default_filter_common # used after filter_flat, filter_normal, and filter_merge

    meta_dl_history_filter: Callable[[DownloadInfo], bool] = default_dl_info_filter

    # merge options
    merge_keep_one: bool = True # removes old merges - one json
    merge_fallback_order: list[yt_types._MetadataFiles_Lit] = dataclasses.field(default_factory=default_merge_fallbacks)

    # --- control hooks (override per-instance as needed) ---
    wrapper_match_filter: Callable[[
            PL_V_InfoDict,
            PL_DownloadInfo,
            PL_DownloadHistory,     ID_DownloadInfo,
            YT_DLP_DownloadArchive, YT_DLP_DownloadArchive_IDs,
        ], DL_Action,
    ] = default_wrapper_match_filter
    yt_dlp_match_filter: Callable[..., str | None] = default_yt_dlp_match_filter

    # --- path templates ---
    path_tmpls: CustomOuttmpl = dataclasses.field(default_factory=default_path_tmpls)
    
    # --- yt-dlp params ---
    opts: YT_DLP_Params = dataclasses.field(default_factory=default_opts)
    edit_final_opts_in_place: Callable[[YT_DLP_Params], None] = default_edit_final_opts_in_place

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
                if not yt_utils.get_pl_id(self.ident):
                    raise ValueError(f"{self.ident} wasn't recognized as a playlist id or url")
            case Config_IdentType.PL_INFO_PATH:
                utils.assert_file(self.ident, "pl_info_path (ident)", min_size=1)
                utils.json_load_typeddict(self.ident, PL_InfoDict)
            case Config_IdentType.METADATA_PATH:
                utils.assert_file(self.ident, "metadata_path (ident)", min_size=1)
                validate_metdata(utils.json_load_typeddict(self.ident, Metadata), self)

        # cookies
        utils.assert_file(self.cookie_file, 'cookie_file', min_size=1, or_None=True)

        # opts
        if 'cookiefile' in self.opts:
            raise ValueError(
                f"'cookiefile' can not be set in `config.opts`.\n"
                f"Set `config.cookie_file` instead.")
        for k in ('outtmpl', 'download_archive'):
            if k in self.opts:
                raise ValueError(
                    f"'{k}' can not be set in `config.opts`.\n"
                    f"Set `config.path_tmpls` instead.")
        if 'paths' in self.opts:
            raise ValueError(
                f"'paths' can not be set in `config.opts`.\n"
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

