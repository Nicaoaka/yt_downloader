from __future__ import annotations

__all__ = [
    'DownloaderConfig',
]

from dataclasses import dataclass, field
from typing import Callable

from yt_types import *
import utils
import yt_utils
import os


def default_wrapper_match_filter(
    pl_v_info: PL_V_InfoDict,
    curr: PL_DownloadInfo,
    history: PL_DownloadHistory,
    ytdlp: YT_DLP_DownloadArchive,
) -> DL_Action:
    """
    1 download OR 3 extracts per run,
    skip if already downloaded,
    download if under 1,000,000 views,
    else extract once.
    """

    id_curr = yt_utils.ids_from_download_info(curr)
    id_history = yt_utils.ids_from_history(history)
    id_ytdlp = yt_utils.ids_from_ytdlp(ytdlp)

    if len(id_curr['download']) >= 1 or len(id_curr['extract']) >= 3:
        return DL_Action.QUIT

    if pl_v_info['id'] in id_history['download']:
        return DL_Action.SKIP
    if (pl_v_info['view_count'] or 0) < 1_000_000:
        return DL_Action.EXTRACT

    if pl_v_info['id'] not in id_history['extract']:
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


def default_edit_final_opts(opts: YT_DLP_Params) -> YT_DLP_Params:
    return opts


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


def default_path_tmpls() -> ConfigOuttmpl:
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
        'merge_infojson': 'merge/%(epoch>%Y-%m-%d %H-%M-%S)s.merge.json',

        'ytdlp_archive': '_ytlp_archive.txt',
        'metadata': '_metadata.json',
    }



@dataclass
class DownloaderConfig:
    # --- playlist identity / location (PICK ONLY ONE) ---
    playlist_id:   str | None = "test/The Verge of Impossibility [...3Cfmpjqm-Pa]/flat/2026-07-03 07-43-12.flat.json"
    info_path:     str | None = None
    metadata_path: str | None = None

    # --- refresh ---
    refresh_after: int = 7 * 24*3600  # seconds; only used if the playlist identifier is a path
    
    # --- cookies ---
    cookie_file:   str | None = None
    empty_cookies: bool = False

    # --- what to persist ---
    write_flat:    bool = True
    write_pl_info: bool = True
    write_merge:   bool = True

    # --- control hooks (override per-instance as needed) ---
    wrapper_match_filter: Callable[
        [PL_V_InfoDict, PL_DownloadInfo, PL_DownloadHistory, YT_DLP_DownloadArchive],
        DL_Action,
    ] = default_wrapper_match_filter
    yt_dlp_match_filter: Callable[..., str | None] = default_yt_dlp_match_filter
    edit_final_opts_in_place: Callable[[YT_DLP_Params], None] = default_edit_final_opts_in_place
    edit_final_opts: Callable[[YT_DLP_Params], YT_DLP_Params] = default_edit_final_opts

    # --- yt-dlp params / path templates ---
    home: str = 'test'
    path_tmpls: ConfigOuttmpl = field(default_factory=default_path_tmpls)
    opts: YT_DLP_Params = field(default_factory=default_opts)

    def __post_init__(self):
        """
        Validate inputs as much as possible.

        Cannot validate `paths_tmpls` here.
        If the playist identifier is an ID, the Playlist folder can't be resolved,
        so any existing metadata file can't be loaded.
        So the 
        """

        # Identifiers
        playlist_identifiers = [x for x in [self.playlist_id, self.info_path, self.metadata_path] if x]
        if len(playlist_identifiers) == 0:
            raise ValueError("Give at least one playlist identifier.\nAny of: playlist_id, info_path, metadata_path")
        if len(playlist_identifiers) > 1:
            raise ValueError(f"Give only one playlist identifier. (Found {len(playlist_identifiers)})\nAny of: playlist_id, info_path, metadata_path")
        
        if self.playlist_id and not yt_utils.is_id_like(self.playlist_id, is_video=False):
            raise ValueError("playlist_id was not recognized as an id")
        
        utils.assert_file(self.info_path,     'info_path',     min_size=1, or_None=True)
        utils.assert_file(self.metadata_path, 'metadata_path', min_size=1, or_None=True)

        # Cookies
        if self.empty_cookies: utils.assert_file(self.cookie_file,   'cookie_path',   min_size=1, or_None=False)
        else:                  utils.assert_file(self.cookie_file,   'cookie_path',   min_size=1, or_None=True)

        # opts
        for k in ('outtmpl', 'paths', 'download_archive'):
            if k in self.opts:
                raise ValueError(
                    f"{k} can not be set in `config.opts`. Use `config.path_tmpls` instead.\n"
                    "(`config.path_tmpls` will create 'outtmpl', 'paths', and 'download_archive')")
