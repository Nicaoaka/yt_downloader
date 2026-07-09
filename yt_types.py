__all__ = [
    'YT_DLP_Params',
    'V_ID', 'PL_ID', 'EPOCH_STR',
    'InfoDict', 'V_InfoDict', 'PL_V_InfoDict', 'PL_InfoDict',
    'YT_DLP_DownloadArchive', 'YT_DLP_DownloadArchive_IDs',

    'Config_IdentType',
    'CustomOuttmpl', 'PL_Resolved_CustomOuttmpl',
    
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
    unavailable_msgs: NotRequired[list[dict]]


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
    merge_info: NotRequired[dict[str, dict[str, Any]]]


class Flat_PL_V_InfoDict(TypedDict):
    _type: str
    ie_key: str
    id: str
    url: str
    title: str
    description:  None
    duration: int | None
    channel_id: str | None
    channel: str | None
    channel_url: str | None
    uploader: str | None
    uploader_id: None
    uploader_url: None
    thumbnails: list
    timestamp: None
    release_timestamp: None
    availability: None
    view_count: int | None
    live_status: None
    channel_is_verified: None
    __x_forwarded_for_ip: None
    playlist: str
    playlist_id: str
    playlist_index: int
    playlist_uploader: str
    playlist_uploader_id: str
    playlist_channel: str


type YT_DLP_DownloadArchive = tuple[tuple[str, str], ...]
type YT_DLP_DownloadArchive_IDs = list[V_ID]


# custom

class Config_IdentType(StrEnum):
    """
    On the first run you must use `PLAYLIST_ID`

    Otherwise, the preferred type is
    1. METADATA_PATH
    2. PL_INFO_PATH
    3. PLAYLIST_ID
    """
    PLAYLIST_ID   = auto()
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
    flat_infojson: str
    pl_infojson: str
    merge_infojson: str
    
    # Meta
    metadata: str
    ytdlp_archive: str

class CustomOuttmpl(_CustomOuttmpl):
    Playlist: str|Callable[[PL_InfoDict], str]

class PL_Resolved_CustomOuttmpl(_CustomOuttmpl):
    Playlist: str



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
    NO_INFO      = auto()
    EXTRACT      = auto()
    DOWNLOAD     = auto()


class DownloadInfo(TypedDict):
    id: str
    action: DL_Action
    result: DL_Result
    errors: list[Exception]

type PL_DownloadInfo = list[DownloadInfo]
type PL_DownloadHistory = dict[EPOCH_STR, PL_DownloadInfo]

class ID_DownloadInfo(TypedDict):
    # skip: list[str]
    fail: list[str]
    no_info: list[str]
    extract: list[str]
    download: list[str]
    error: list[str]


_MetadataFiles_Lit = Literal['latest_flat_info', 'latest_pl_info', 'latest_merge_info']
class _MetadataFiles(TypedDict):
    latest_flat_info:  str|None
    latest_pl_info:    str|None
    latest_merge_info: str|None
assert set(get_args(_MetadataFiles_Lit)) == set(_MetadataFiles.__required_keys__), "Must have same key names"

class Metadata(_MetadataFiles):
    id: str
    path_tmpls: PL_Resolved_CustomOuttmpl
    history: PL_DownloadHistory
    pl_epoch: int # for latest pl extraction
    v_epoch:  int # for latest video extraction

def empty_Metadata() -> Metadata:
    """ `id`, `path_tmpls`, `pl_epoch`, and `v_epoch` must be set """
    return {
        'id': '',
        'history':    {},
        'path_tmpls': {},
        'pl_epoch':   -1,
        'v_epoch':    -1,
        
        'latest_flat_info':  None,
        'latest_pl_info':    None,
        'latest_merge_info': None,
    } # type: ignore



class _V_InfoLevel(IntEnum):
    NONE = 0
    CHECK_WA = 1
    CHECK_YT = 2
    EXTRACT = 3
    DOWNLOAD = 4

class _PL_InfoLevel(IntEnum):
    NONE = 0
    FLAT = 1
    NORMAL = 2
    MERGED = 3



def main():
    pass

if __name__ == "__main__":
    main()
