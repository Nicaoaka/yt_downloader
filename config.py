from __future__ import annotations

__all__ = [
    'PlaylistDL_Config'
]

from dataclasses import dataclass, field
from typing import Callable, Literal

from yt_types import *
import yt_types
import utils
import yt_utils


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
    ytdlp_ids: list[V_ID],
) -> DL_Action:
    """
    1 download OR 3 extracts per run,
    skip if already downloaded,
    download if under 1,000,000 views,
    else extract once.
    """

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


def default_yt_dlp_match_filter(v_info: V_InfoDict, *, incomplete: bool) -> str | None:
    """
    May be called multiple times for during the same video.
    Only effects download, will extract no matter what! `(use wrapper_match_filter instead)`

    - Return a message to skip.
    - Return None to downloaded.
    - Return `utils.NO_DEFAULT` to prompt user.
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
        'match_filter': default_yt_dlp_match_filter,  # type: ignore

        'postprocessors': [
            {'already_have_subtitle': False, 'key': 'FFmpegEmbedSubtitle'},
            {'add_chapters': True, 'add_infojson': 'if_exists',
             'add_metadata': True, 'key': 'FFmpegMetadata'},
            {'already_have_thumbnail': False, 'key': 'EmbedThumbnail'},
        ],

        'writeautomaticsub': False,
        'subtitleslangs': ['ja*', 'en*', '日本語', '英語', '-live_chat'],
        'writesubtitles': True,
        'writethumbnail': True,
    }


def default_path_tmpls() -> CustomOuttmpl:
    """
    reference: https://github.com/yt-dlp/yt-dlp#output-template
    
    Defaults for outtmpl can be found in yt_dlp/utils/_utils.py in the symbol `OUTTMPL_TYPES`.
    """
    return {
        'Playlist': lambda pl_info: (
            f"{pl_info['title'] or '[no title]'} "
            f"[{utils.truncate(pl_info['id'], 11, end_in_max=False, trunc_start=True)}]"
        ),

        'video_file': 'Videos/%(title)s [%(id)s].%(ext)s',

        'flat_infojson': 'flat/%(epoch>%Y-%m-%d %H-%M-%S)s.flat.json',
        'pl_infojson': 'playlist/%(epoch>%Y-%m-%d %H-%M-%S)s.info.json',
        'merge_infojson': '%(epoch>%Y-%m-%d %H-%M-%S)s.json',

        'ytdlp_archive': '_ytlp_archive.txt',
        'metadata': '_metadata.json',
    }


@dataclass
class PlaylistDL_Config:
    # --- playlist identity / location (PICK ONLY ONE) ---
    ident: str
    ident_type: ConfigID_Type

    # --- refresh ---
    refresh_after: int = 7 * 24*3600  # seconds; only used if the playlist identifier is a path
    
    # --- cookies ---
    cookie_file: str | None = None
    cookies_for_pl:    bool = True
    cookies_for_vids:  bool = False
    empty_cookies:     bool = False

    # --- what to persist ---
    write_flat:    bool = True
    write_pl_info: bool = True
    write_merge:   bool = True
    
    # merge options
    merge_keep_one: bool = True # removes old merges - one json
    merge_fallback_order: list[yt_types._MetadataFiles_Lit] = field(default_factory=default_merge_fallbacks)

    # --- control hooks (override per-instance as needed) ---
    wrapper_match_filter: Callable[
        [
            PL_V_InfoDict,
            PL_DownloadInfo,
            PL_DownloadHistory,
            ID_DownloadInfo,
            YT_DLP_DownloadArchive,
            list[V_ID],
        ],
        DL_Action,
    ] = default_wrapper_match_filter
    yt_dlp_match_filter: Callable[..., str | None] = default_yt_dlp_match_filter
    edit_final_opts_in_place: Callable[[YT_DLP_Params], None] = default_edit_final_opts_in_place

    # --- yt-dlp params / path templates ---
    home: str = 'test'
    path_tmpls: CustomOuttmpl = field(default_factory=default_path_tmpls)
    opts: YT_DLP_Params = field(default_factory=default_opts)

    def __post_init__(self):
        """
        Validate inputs as much as possible.

        Cannot validate `paths_tmpls` here.
        If the playist identifier is an ID, the Playlist folder can't be resolved,
        so any existing metadata file can't be loaded.
        So the 
        """

        utils.assert_file(self.cookie_file, 'cookie_file', min_size=1, or_None=True)

        # opts
        if 'cookiefile' in self.opts:
            raise ValueError(
                f"cookiefile can not be set in `config.opts`. Use `config.cookie_file` instead.")
        for k in ('outtmpl', 'paths', 'download_archive'):
            if k in self.opts:
                raise ValueError(
                    f"{k} can not be set in `config.opts`. Use `config.path_tmpls` instead.\n"
                    "(`config.path_tmpls` will create 'outtmpl', 'paths', and 'download_archive')")

def main():
    print("Default config:")
    import pprint
    pprint.pprint(PlaylistDL_Config(ident='exampleid', ident_type=ConfigID_Type.PLAYLIST_ID))

if __name__ == "__main__":
    main()
