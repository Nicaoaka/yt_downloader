__all__ = [
    'V_ID', 'PL_ID', 'READABLE_EPOCH_STR', 'YT_DLP_Params',

    'YT_DLP_InfoDict', 'V_InfoDict', 'PL_InfoDict', 'ANY_InfoDict',

    'YT_DLP_DownloadArchive', 'YT_DLP_DownloadArchive_IDs',

    'CustomOuttmpl', 'PL_Resolved_CustomOuttmpl',
    'Metadata',
    
    'DL_Action', 'DL_Result',
    'DownloadInfo', 'PL_DownloadInfo', 'PL_DownloadHistory',
    'ID_DownloadInfo',

    'UnavailableMsg',
    'V_MergeTimeline', 'PL_MergeTimeline',
    'NO_VALUE',
]

from enum import StrEnum, auto
from typing import get_args, TypedDict, Literal, NotRequired, Required, Any, Callable, Iterable, TYPE_CHECKING
if TYPE_CHECKING:
    from _typeshed import Incomplete
    from yt_dlp import _Params
    # from yt_dlp.utils import PagedList

from pldl.utils.utils import FalsySentinel



type V_ID = str
type PL_ID = str
type READABLE_EPOCH_STR = str
type YT_DLP_Params = _Params



# YT_DLP_InfoDict is `_InfoDict` copied from
# .../.vscode/extensions/ms-python.vscode-pylance-XXXX.XX.XX/dist/typeshed-fallback/stubs/yt-dlp/yt_dlp/extractpr/common.pyi
# yt_dlp version 2026.07.01.235203
class YT_DLP_InfoDict[ENTRY=YT_DLP_InfoDict](TypedDict, total=False):
    id: Required[str]
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
    live_status: Literal["is_live", "is_upcoming", "was_live", "not_live", "post_live"] | None
    start_time: Incomplete
    end_time: Incomplete
    chapters: Incomplete
    heatmap: Incomplete
    playable_in_embed: bool | str | None
    availability: Literal["private", "premium_only", "subscriber_only", "needs_auth", "unlisted", "public"] | None
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
    entries: list[ENTRY] # changed from Iterable[_InfoDict] | PagedList
    requested_formats: Iterable[YT_DLP_InfoDict]
    # deprecated fields:
    composer: Incomplete
    artist: Incomplete
    genre: Incomplete
    album_artist: Incomplete
    creator: str | None

    # custom
    epoch: int


class _PL_V_RelInfo(TypedDict, total=False):
    # copied from full YT playlist info extraction
    # playlist and playlist_index are in all YT / WA VideoInfos playlist or not
    # that's why they have ' | None', they should be defined
    playlist_count: int | None # same as 'n_entries'
    playlist: str | None
    playlist_id: str
    playlist_title: str # same as 'playlist'
    playlist_uploader: str
    playlist_uploader_id: str # @handle
    playlist_channel: str # same as 'playlist_uploader'
    playlist_channel_id: str # YT id
    playlist_webpage_url: str
    n_entries: int
    playlist_index: int | None
    __last_playlist_index: int # same as 'n_entries'
    playlist_autonumber: int # same as 'playlist_index'

class _V_InfoDict_Addons(TypedDict, total=False):
    info_level: str
    yt_unavailable_msg: str|None
    wa_unavailable_msg: str|None
    unavailable_msgs: list[UnavailableMsg]
    playlist_epoch: int

class _PL_InfoDict_Addons(TypedDict, total=False):
    info_level: str
    merge_timeline: PL_MergeTimeline

class V_InfoDict(YT_DLP_InfoDict, _PL_V_RelInfo, _V_InfoDict_Addons): ...
class PL_InfoDict[ENTRY=V_InfoDict](YT_DLP_InfoDict[ENTRY], _PL_InfoDict_Addons):
    entries: list[ENTRY] # type: ignore - override

type ANY_InfoDict = V_InfoDict | PL_InfoDict | dict



# custom Types
type YT_DLP_DownloadArchive = tuple[tuple[str, str], ...]
type YT_DLP_DownloadArchive_IDs = list[V_ID]

# outtmpl doesn't include Home,
# so that the Home folder can be moved without edits
class _CustomOuttmpl(TypedDict):
    video_file: str # instead of `default`
    chapter:    NotRequired[str]
    subtitle:   NotRequired[str]
    thumbnail:  NotRequired[str]
    description:NotRequired[str]
    annotation: NotRequired[str]
    link:       NotRequired[str]

    # Custom names
    pl_infojson: str
    merge_infojson: str
    raw_flat_infojson: str
    raw_video_infojson: str
    _merged_flat_infojson: str
    
    # Meta
    metadata: str
    yt_dlp_archive: str

class CustomOuttmpl(_CustomOuttmpl):
    Playlist: str|Callable[[PL_InfoDict], str]

class PL_Resolved_CustomOuttmpl(_CustomOuttmpl):
    Playlist: str

_MetadataFiles_Lit = Literal['latest_flat_info', 'latest_pl_info', 'latest_merge_info', '_merge_flat']
class _MetadataPointers(TypedDict, total=False):
    """
    ### will be lists instead of tuples!
    Tuples are used for better type checking, and values should be handled *immutably* anyway.
    """
    latest_flat_info:  tuple[str, int]|None
    latest_pl_info:    tuple[str, int]|None
    latest_merge_info: tuple[str, int]|None
    _merge_flat:       tuple[str, int]|None
assert set(get_args(_MetadataFiles_Lit)) == set(_MetadataPointers.__optional_keys__), "Must have same key names"

class Metadata(TypedDict):
    id: str
    path_tmpls: PL_Resolved_CustomOuttmpl
    pointers: _MetadataPointers
    
    history: PL_DownloadHistory



# Download control types
class DL_Action(StrEnum):
    USER     = auto()
    QUIT     = auto()
    SKIP     = auto()
    EXTRACT  = auto()
    DOWNLOAD = auto()

class DL_Result(StrEnum):
    CANCELLED    = auto()
    FAIL         = auto()
    UNRECOGNIZED = auto()
    CACHED      = auto()
    EXTRACT      = auto()
    DOWNLOAD     = auto()

class DownloadInfo(TypedDict):
    id: str
    title: str | None
    action: DL_Action
    result: DL_Result
    errors: NotRequired[list[Exception]]

type PL_DownloadInfo = list[DownloadInfo]
type PL_DownloadHistory = dict[READABLE_EPOCH_STR, PL_DownloadInfo]

class ID_DownloadInfo(TypedDict):
    # skip: list[str]
    fail: list[str]
    extract: list[str]
    download: list[str]
    error: list[str]



# used by postprocessing.merge_infos
class UnavailableMsg(TypedDict):
    epoch: int|None
    msg:   str|None
    type:  str

class _V_MergeTimeline(TypedDict):
    better_info: NotRequired[list[str]] # "{merge_V_InfoLevel.name} -> {new_V_InfoLevel.name}"
    unavailable: NotRequired[list[str]]
    updates:     NotRequired[list[str]]
type V_MergeTimeline = dict[READABLE_EPOCH_STR, _V_MergeTimeline]
type PL_MergeTimeline = dict[V_ID, V_MergeTimeline]

class NO_VALUE(FalsySentinel): ...
