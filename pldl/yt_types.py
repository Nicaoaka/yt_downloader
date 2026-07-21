__all__ = [
    'YT_DLP_Params',
    'V_ID', 'PL_ID', 'EPOCH_STR',
    'InfoDict', 'V_InfoDict', 'PL_V_InfoDict', 'PL_InfoDict',
    'YT_DLP_DownloadArchive', 'YT_DLP_DownloadArchive_IDs',

    'Config_IdentType',
    'CustomOuttmpl', 'PL_Resolved_CustomOuttmpl',
    
    'UnavailableMsg',
    'V_MergeTimeline', 'PL_MergeTimeline',
    'DL_Action', 'DL_Result',
    'DownloadInfo', 'PL_DownloadInfo', 'PL_DownloadHistory',
    'ID_DownloadInfo',
    'Metadata',
    '_V_InfoLevel', '_PL_InfoLevel',
]

from enum import StrEnum, auto, IntEnum
from typing import get_args, TypedDict, Literal, NotRequired, Required, Any, Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from yt_dlp import _Params

type V_ID = str
type PL_ID = str
type EPOCH_STR = str
type YT_DLP_Params = _Params

# copied from yt_dlp, slightly editted
class InfoDict(TypedDict):
    # age_limit: int
    availability: Literal["private", "premium_only", "subscriber_only", "needs_auth", "unlisted", "public"] | None
    # available_at: int
    # creator: str | None
    # comment_count: int | None
    # duration: int | None
    # formats: list[dict[str, Any]]
    id: Required[str]
    like_count: NotRequired[int | None]
    # tags: list[str] | None
    thumbnail: NotRequired[str | None]
    # timestamp: int | float | None 
    title: str | None
    uploader: str | None
    url: NotRequired[str | None]

    view_count: int | None
    channel: str | None
    channel_id: str | None
    uploader_id: str | None
    uploader: str | None
    channel_url: str | None
    uploader_url: str | None
    epoch: NotRequired[int]
    channel_follower_count: NotRequired[int | None]

    extractor_key: NotRequired[str]
    extractor: NotRequired[str]
    webpage_url: NotRequired[str]
    original_url: NotRequired[str]
    webpage_url_basename: NotRequired[str]
    webpage_url_domain: NotRequired[str]

class V_InfoDict(InfoDict):
    # age_limit: int
    # available_at: int
    comment_count: int | None
    duration: int | None
    formats: list[dict[str, Any]]
    tags: NotRequired[list[str] | None]

    # custom
    yt_unavailable_msg: NotRequired[str|None]
    wa_unavailable_msg: NotRequired[str|None]
    unavailable_msgs: NotRequired[list[UnavailableMsg]]


class __PL_V_InfoDict(TypedDict):
    playlist: str | None
    playlist_id: str
    playlist_index: int
    playlist_uploader: str | None
    playlist_uploader_id: str | None
    playlist_channel: str | None

    # custom
    playlist_epoch: NotRequired[int]

class PL_V_InfoDict(V_InfoDict, __PL_V_InfoDict):
    ...


class PL_InfoDict(InfoDict):
    playlist_count: int
    modified_date: str
    entries: list[PL_V_InfoDict]
    tags: list[str] | None

    # Custom
    merge_timeline: NotRequired[PL_MergeTimeline]


# class Flat_PL_V_InfoDict(TypedDict):
#     _type: str
#     ie_key: str
#     id: str
#     url: str
#     title: str
#     description:  None
#     duration: int | None
#     channel_id: str | None
#     channel: str | None
#     channel_url: str | None
#     uploader: str | None
#     uploader_id: None
#     uploader_url: None
#     thumbnails: list
#     timestamp: None
#     release_timestamp: None
#     availability: None
#     view_count: int | None
#     live_status: None
#     channel_is_verified: None
#     __x_forwarded_for_ip: None
#     playlist: str
#     playlist_id: str
#     playlist_index: int
#     playlist_uploader: str
#     playlist_uploader_id: str
#     playlist_channel: str


type YT_DLP_DownloadArchive = tuple[tuple[str, str], ...]
type YT_DLP_DownloadArchive_IDs = list[V_ID]


# custom

class Config_IdentType(StrEnum):
    """
    On the first run you must use `PL_ID_OR_URL`

    Otherwise, the preferred type is
    1. METADATA_PATH
    2. PL_INFO_PATH
    3. PL_ID_OR_URL
    """
    PL_ID_OR_URL   = auto()
    PL_INFO_PATH  = auto()
    METADATA_PATH = auto()

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

class UnavailableMsg(TypedDict):
    epoch: int|None
    msg:   str|None
    type:  str

class _V_MergeTimeline(TypedDict):
    better_info: NotRequired[str] # "{merge_V_InfoLevel.name} -> {new_V_InfoLevel.name}"
    unavailable: NotRequired[list[str]]
type V_MergeTimeline = dict[EPOCH_STR, _V_MergeTimeline]
type PL_MergeTimeline = dict[V_ID, V_MergeTimeline]

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
type PL_DownloadHistory = dict[EPOCH_STR, PL_DownloadInfo]

class ID_DownloadInfo(TypedDict):
    # skip: list[str]
    fail: list[str]
    extract: list[str]
    download: list[str]
    error: list[str]


_MetadataFiles_Lit = Literal['latest_flat_info', 'latest_pl_info', 'latest_merge_info', '_merge_flat']
class _MetadataPointers(TypedDict):
    """
    ### will be lists instead of tuples!
    Tuples are used for better type checking, and values should be handled *immutably* anyway.
    """
    latest_flat_info:  tuple[str, int]|None
    latest_pl_info:    tuple[str, int]|None
    latest_merge_info: tuple[str, int]|None
    _merge_flat: tuple[str, int]|None
assert set(get_args(_MetadataFiles_Lit)) == set(_MetadataPointers.__required_keys__), "Must have same key names"

class Metadata(TypedDict):
    id: str
    path_tmpls: PL_Resolved_CustomOuttmpl
    history: PL_DownloadHistory

    pointers: _MetadataPointers



class _V_InfoLevel(IntEnum):
    NONE = 0
    UNAVAIL_YT = 1
    FLAT = 2
    EXTRACT = 3
    DOWNLOAD = 4

class _PL_InfoLevel(IntEnum):
    NONE = 0
    FLAT = 1
    MERGE_FLAT = 2
    NORMAL = 3
    MERGE = 4
