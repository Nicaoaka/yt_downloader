__all__ = [
    'YT_DLP_Params', 'InfoDict', 'V_InfoDict', 'PL_V_InfoDict', 'PL_InfoDict',
    'YT_DLP_DownloadArchive',
    'Metadata',
    'CustomOuttmpl', 'PL_ResolvedPaths',
    'DL_Action', 'DL_Result',
    'PL_DownloadInfo', 'DownloadInfo', 'ID_DownloadInfo',
]

from enum import StrEnum, auto
from typing import Literal, TypedDict, NotRequired, Required, Any, Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from yt_dlp import _Params

type V_ID = str
type PL_ID = str
type EPOCH_STR = str
type YT_DLP_Params = _Params
class NO_DEFAULT: ...

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
    like_count: int | None
    # tags: list[str] | None
    thumbnail: str | None
    # timestamp: int | float | None 
    title: str | None
    uploader: str | None
    url: str | None

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


type YT_DLP_DownloadArchive = list[tuple[str, str]]


# custom
class CustomOuttmpl(TypedDict):
    # Folders
    Home: str
    Playlist: str|Callable[[PL_InfoDict], str]

    # Video Files
    video_file: str # for `default`
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

class PL_ResolvedPaths(TypedDict):
    Home: str
    Playlist: str
    video_file: str
    flat_infojson: str
    pl_infojson: str
    merge_infojson: str
    ytdlp_archive: str
    metadata: str

    chapter:     NotRequired[str]
    subtitle:    NotRequired[str]
    thumbnail:   NotRequired[str]
    description: NotRequired[str]
    annotation:  NotRequired[str]
    link:        NotRequired[str]

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
    DOWNLOAD   = auto()

class DownloadInfo(TypedDict):
    id: str
    action: DL_Action
    result: DL_Result
    errors: list[Exception]

class ID_DownloadInfo(TypedDict):
    # skip: list[str]
    fail: list[str]
    no_info: list[str]
    extract: list[str]
    download: list[str]
    error: list[str]

type PL_DownloadInfo = list[DownloadInfo]


class _MetadataFiles(TypedDict):
    latest_flat_info:  str|None
    latest_pl_info:    str|None
    latest_merge_info: str|None

class Metadata(_MetadataFiles):
    history:    dict[EPOCH_STR, PL_DownloadInfo]
    path_tmpls: CustomOuttmpl
    pl_epoch:   int
    epoch:      int

def empty_Metadata() -> Metadata:
    return {
        'history':    {},
        'path_tmpls': {},
        'latest_flat_info':  None,
        'latest_pl_info':    None,
        'latest_merge_info': None,
        'pl_epoch':   NO_DEFAULT,
        'epoch':      NO_DEFAULT,
    } # type: ignore - epochs must be set manually

def main():
    print(_MetadataFiles.__required_keys__)

if __name__ == "__main__":
    main()
