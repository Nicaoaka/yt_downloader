"""
The yt-dlp payload shape, as TypedDicts, plus the download-control vocabulary.

TypedDict is right here and a dataclass is not: this is foreign data with ~140 of optional keys
whose shape changes between yt-dlp releases. It types the keys we care about, costs nothing
at runtime, copies and validates nothing, and keys yt-dlp adds tomorrow are ignored.

- `id` is ReadOnly: nothing may reassign a video's identity in place.

v1-compat: the pldl-side addon keys (`info_level`, `unavailable_msgs`, `playlist_epoch`) are
still declared here because stored v1 files carry them inline and the migrator has to read
them. **New code must not write them into a payload** -- they are envelope fields; see
envelope.py.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'V_ID', 'PL_ID',

    'YT_DLP_InfoDict', 'V_InfoDict', 'PL_InfoDict', 'ANY_InfoDict',

    'ExtractorKey', 'YT_DLP_DownloadArchive', 'YT_DLP_DownloadArchive_IDs',

    'DL_Action', 'DL_Result',
    'NO_VALUE',

    # v1-compat
    '_v1_DownloadInfo', '_v1_Session_DownloadInfo',
]

from collections.abc import Iterable
from enum import StrEnum, auto
from typing import Any, Literal, NotRequired, ReadOnly, Required, TypedDict

type V_ID = str
type PL_ID = str

# yt-dlp's own stubs type these as `_typeshed.Incomplete`, i.e. "not pinned down yet".
# Kept as a distinct alias so the unfinished ones stay visibly unfinished.
type Incomplete = Any


# YT_DLP_InfoDict is `_InfoDict` copied from
# .../ms-python.vscode-pylance-*/dist/typeshed-fallback/stubs/yt-dlp/yt_dlp/extractor/common.pyi
# yt_dlp version 2026.07.01.235203
class YT_DLP_InfoDict[ENTRY=YT_DLP_InfoDict](TypedDict, total=False):
    id: ReadOnly[Required[str]]
    title: str | None
    formats: list[dict[str, Any]] | None
    available_at: int
    url: str | None
    ext: str | None
    format: str | None
    player_url: str | None
    direct: bool | None
    alt_title: str | None
    display_id: Incomplete
    thumbnails: list[dict[str, Incomplete]] | None
    thumbnail: str | None
    description: str | None
    uploader: str | None
    license: str | None
    creators: list[str] | None
    timestamp: int | float | None
    upload_date: Incomplete
    release_timestamp: Incomplete
    release_date: Incomplete
    release_year: Incomplete
    modified_timestamp: Incomplete
    modified_date: Incomplete
    uploader_id: Incomplete
    uploader_url: str | None
    channel: str | None
    channel_id: Incomplete
    channel_url: str | None
    channel_follower_count: int | None
    channel_is_verified: Incomplete
    location: Incomplete
    subtitles: Incomplete
    automatic_captions: Incomplete
    duration: int | None
    view_count: int | None
    concurrent_view_count: int | None
    save_count: int | None
    like_count: int | None
    dislike_count: int | None
    repost_count: int | None
    average_rating: Incomplete
    comment_count: int | None
    comments: Incomplete
    age_limit: int
    webpage_url: str | None
    categories: list[str] | None
    tags: list[str] | None
    cast: list[Incomplete] | None
    is_live: bool | None
    was_live: bool | None
    live_status: Literal['is_live', 'is_upcoming', 'was_live', 'not_live', 'post_live'] | None
    start_time: Incomplete
    end_time: Incomplete
    chapters: Incomplete
    heatmap: Incomplete
    playable_in_embed: bool | str | None
    availability: Literal['private', 'premium_only', 'subscriber_only', 'needs_auth',
                          'unlisted', 'public'] | None
    media_type: str | None
    _old_archive_ids: Incomplete
    _format_sort_fields: Incomplete
    chapter: str | None
    chapter_number: int | None
    chapter_id: str | None
    series: str | None
    series_id: str | None
    season: str | None
    season_number: int | None
    season_id: str | None
    episode: Incomplete
    episode_number: int | None
    episode_id: str | None
    track: str | None
    track_number: int | None
    track_id: str | None
    artists: list[str] | None
    composers: list[str] | None
    genres: list[str] | None
    album: str | None
    album_type: str | None
    album_artists: list[str] | None
    disc_number: int | None
    section_start: Incomplete
    section_end: Incomplete
    rows: int | None
    columns: int | None
    playlist_count: int | None
    entries: list[ENTRY]  # changed from Iterable[_InfoDict] | PagedList
    requested_formats: Iterable[YT_DLP_InfoDict]
    requested_downloads: Iterable[YT_DLP_InfoDict]  # presence of this means DOWNLOAD level

    # deprecated fields
    composer: Incomplete
    artist: Incomplete
    genre: Incomplete
    album_artist: Incomplete
    creator: str | None

    # yt-dlp writes this on every extraction
    epoch: int

    # yt-dlp's own extractor bookkeeping, load-bearing for level derivation
    extractor: NotRequired[str]
    extractor_key: NotRequired[str]
    ie_key: NotRequired[str]


class _PL_V_RelInfo(TypedDict, total=False):
    """Playlist-relative fields yt-dlp adds to a video that was reached through a playlist.

    `playlist` and `playlist_index` appear on every YT/WA video info, playlist or not, which
    is why they are `| None` rather than absent.
    """
    playlist_count: int | None      # same as 'n_entries'
    playlist: str | None
    playlist_id: str
    playlist_title: str             # same as 'playlist'
    playlist_uploader: str
    playlist_uploader_id: str       # @handle
    playlist_channel: str           # same as 'playlist_uploader'
    playlist_channel_id: str        # YT id
    playlist_webpage_url: str
    n_entries: int
    playlist_index: int | None
    __last_playlist_index: int      # same as 'n_entries'
    playlist_autonumber: int        # same as 'playlist_index'


class _v1_V_InfoDict_Addons(TypedDict, total=False):
    """DEPRECATED! Fields that v1 wrote *into* the payload.

    v1-compat: Declared so the migrator can read v1 files. New code puts these on the top layer
    instead (see envelope.py).
    """
    info_level: str
    unavailable_msgs: list[dict[str, Any]]  # v1 wrote plain dicts
    playlist_epoch: int


class _v1_PL_InfoDict_Addons(TypedDict, total=False):
    """DEPRECATED! Fields that v1 wrote into a generated playlist infodict.

    v1-compat: generated playlist documents carry these on an envelope now, so they cannot
    collide with yt-dlp's namespace. Declared so the migrator can read v1 files.
    """

    info_level: str
    merge_timeline: dict[str, dict[str, Any]]


class V_InfoDict(YT_DLP_InfoDict, _PL_V_RelInfo, _v1_V_InfoDict_Addons): ...


class PL_InfoDict[ENTRY=V_InfoDict](YT_DLP_InfoDict[ENTRY], _v1_PL_InfoDict_Addons):
    entries: list[ENTRY]  # type: ignore[misc] - deliberate override


type ANY_InfoDict = V_InfoDict | PL_InfoDict | dict


# ---- archive ----

type ExtractorKey = str
type YT_DLP_DownloadArchive = list[tuple[ExtractorKey, V_ID]]
type YT_DLP_DownloadArchive_IDs = list[V_ID]


# ---- download control ----

class DL_Action(StrEnum):
    """What to do with a video.

    Declaration order used to be load-bearing for override tie-breaks, documented only in a
    comment. policy/ gives rules an explicit `priority` instead, so nothing here depends on
    the order any more.
    """
    USER     = auto()
    QUIT     = auto()
    SKIP     = auto()
    EXTRACT  = auto()
    DOWNLOAD = auto()


class DL_Result(StrEnum):
    """What actually happened.

    CANCELLED and CACHED are separate: "already in the archive" and "the user stopped it" lead
    to different decisions on the next run, so collapsing them loses the distinction that
    matters.
    """
    CANCELLED    = auto()
    FAIL         = auto()
    UNRECOGNIZED = auto()
    CACHED       = auto()
    EXTRACT      = auto()
    DOWNLOAD     = auto()


# ---- v1-compat ----

class _v1_DownloadInfo(TypedDict):
    """DEPRECATED! One video's outcome, as v1 wrote it into `history`.

    v1-compat: `metadata.VideoLog` is the v2 shape. Kept so the migrator can read v1 history.
    """

    id: str
    title: str | None
    action: DL_Action
    result: DL_Result
    errors: NotRequired[list[str]]


type _v1_Session_DownloadInfo = list[_v1_DownloadInfo]
"""DEPRECATED! v1-compat: `metadata.SessionLog` is the v2 shape."""


# ---- sentinels ----

class _FalsySentinelMeta(type):
    def __repr__(cls) -> str:
        return f'<{cls.__name__}>'

    def __bool__(cls) -> Literal[False]:
        return False


class NO_VALUE(metaclass=_FalsySentinelMeta):
    """Differentiate absent from `None`/default value.

    Falsy and never instantiated -- it is used as the class itself, so `is NO_VALUE` is the
    identity check and `if value:` treats it like any other empty value.
    """
