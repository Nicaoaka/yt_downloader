__all__ = [
    'YT_Flat_V_InfoDict', 'YT_V_InfoDict', 'WA_V_InfoDict',
    'YT_Flat_PL_V_InfoDict', 'YT_PL_V_InfoDict', 'WA_PL_V_InfoDict',
    'YT_Flat_PL_InfoDict', 'YT_PL_InfoDict',
]

from typing import TypedDict, Literal, NotRequired, Required, Any, TYPE_CHECKING
from pldl.pldl_types import (
    _PL_V_RelInfo,
    _V_InfoDict_Addons,
    _PL_InfoDict_Addons,
)



# 
# V_InfoDict
# 

class _YT_Flat_V_Thumbnails(TypedDict):
    url: str
    height: int
    width: int
    # preference: int
    # id: str
    # resolution: str

class _YT_Flat_V_InfoDict(TypedDict, total=False):
    _type: str
    ie_key: str
    id: Required[str]
    url: str
    title: str

    description: str | None # None always
    duration: int | None
    channel_id: str | None
    channel: str | None
    channel_url: str | None
    uploader: str | None
    uploader_id: str | None
    uploader_url: str | None
    thumbnails: list[_YT_Flat_V_Thumbnails]
    timestamp: int | None
    release_timestamp: int | None
    availability: str | None
    view_count: int | None
    live_status: str | None
    channel_is_verified: bool | None
    __x_forwarded_for_ip: Any


class _fragment(TypedDict, total=False):
    url: str
    duration: int | float

class _YT_Formats(TypedDict):
    asr: NotRequired[int | float | None]
    format_id: str
    format_index: NotRequired[int | None]
    manifest_url: NotRequired[str]
    language: NotRequired[str | None]
    language_preference: NotRequired[int]
    filesize: NotRequired[int | None]
    format_note: NotRequired[str]
    ext: str
    protocol: str
    preference: NotRequired[int | None]
    quality: NotRequired[int | float]
    has_drm: NotRequired[bool]
    acodec: NotRequired[str | Literal['none']]
    vcodec: str | Literal['none']
    dynamic_range: NotRequired[str | None]
    container: NotRequired[str]
    downloader_options: NotRequired[dict[str, int]]
    source_preference: NotRequired[int]
    url: str
    width: NotRequired[int | None]
    height: NotRequired[int | None]
    fps: NotRequired[int | float | None]
    audio_channels: NotRequired[int | None]
    rows: NotRequired[int]
    columns: NotRequired[int]
    fragments: NotRequired[list[_fragment]]
    audio_ext: str | Literal['none']
    video_ext: str | Literal['none']
    vbr: int | float | None
    abr: int | float | None
    tbr: int | float | None
    resolution: str
    aspect_ratio: int | float | None
    filesize_approx: NotRequired[int | None]
    http_headers: dict[str, str] # idrc about the stuff in here
        # User-Agent: str
        # Accept: str
        # Accept-Language: str
        # Sec-Fetch-Mode: str
    format: str # '{format_id} - {resolution} {format_note}'
    filepath: NotRequired[str] # in requested_downloads

class _YT_Thumbnails(TypedDict):
    url: str
    height: NotRequired[int]
    width: NotRequired[int]
    preference: int
    id: str
    resolution: NotRequired[str]

class _YT_Subtitle(TypedDict):
    ext: str
    url: str # to download
    name: NotRequired[str] # language spelt out
    video_id: NotRequired[str] # in 'live_chat'
    protocol: NotRequired[Literal['m3u8_native', 'youtube_live_chat_replay'] | str]
    __yt_dlp_client: NotRequired[Literal['tv', 'ios'] | str]

class _YT_RequestedSubtitles(_YT_Subtitle, total=False):
    filepath: str

class _YT_Heatmap(TypedDict):
    start_time: float
    end_time: float
    value: float

class __YT_Format_Compact(TypedDict, total=False): 
    format: str
    format_id: str
    ext: str
    protocol: str
    language: NotRequired[str | None]
    format_note: str
    filesize_approx: int
    tbr: int | float | None
    width: int | None
    height: int | None
    resolution: str | None
    fps: int | float | None
    dynamic_range: str | None
    vcodec: str | None
    vbr: int | float | None
    aspect_ratio: int | float | None
    acodec: str | None
    abr: int | float | None
    asr: int | float | None
    audio_channels: int | None

class _YT_RequestedDownloads(__YT_Format_Compact, total=False):
    requested_formats: list[_YT_Formats]
    
    # almost _YT_Format()
        # format
        # format_id
        # ext
        # protocol
        # language
        # format_note
        # filesize_approx
        # tbr
        # width
        # height
        # resolution
        # fps
        # dynamic_range
        # vcodec
        # vbr
        # aspect_ratio
        # acodec
        # abr
        # asr
        # audio_channels
    
    _filename: str
    filename: str
    filepath: str
    __postprocessors: NotRequired[list[str]]
    __real_download: NotRequired[bool]
    __files_to_merge: NotRequired[list[str]]
    __finaldir: str
    __files_to_move: NotRequired[dict]
    __write_download_archive: NotRequired[bool]

class _YT_V_InfoDict(__YT_Format_Compact, total=False):
    id: Required[str]
    title: str
    formats: list[_YT_Formats]
    thumbnails: list[_YT_Thumbnails]
    thumbnail: str
    description: str
    channel_id: str
    channel_url: str
    duration: int
    view_count: int
    average_rating: Any
    age_limit: int
    webpage_url: str
    categories: list[str]
    tags: list[str]
    playable_in_embed: bool
    live_status: str
    media_type: str
    release_timestamp: int | None
    _format_sort_fields: list[str]
    automatic_captions: dict[str, list[_YT_Subtitle]] # str is the language name
    subtitles: dict[str, list[_YT_Subtitle]] # str is the caption name
    comment_count: int
    chapters: list | dict | None
    heatmap: list[_YT_Heatmap] | None
    like_count: int
    channel: str
    channel_follower_count: int # subscriber count
    channel_is_verified: NotRequired[bool]
    uploader: str
    uploader_id: str | None
    uploader_url: str | None
    upload_date: str
    timestamp: int
    availability: Literal['private', 'premium_only', 'subscriber_only', 'needs_auth', 'unlisted', 'public'] | None
    original_url: str
    webpage_url_basename: Literal['watch'] # videos are 'watch', playlists are 'playlist'
    webpage_url_domain: Literal['youtube.com']
    extractor: Literal['youtube']
    extractor_key: Literal['Youtube']

    playlist: str | None
    playlist_index: int | None

    display_id: str # same as id
    fulltitle: str # same as title
    duration_string: str # HH:MM:SS no lead 0s
    release_date: NotRequired[str] # YYYYMMDD
    release_year: int | None
    is_live: bool
    was_live: bool
    requested_subtitles: dict[str, _YT_RequestedSubtitles] | None
    _has_drm: Any | None
    epoch: int

    requested_downloads: list[_YT_RequestedDownloads]
    requested_formats: list[_YT_Formats]

    # almost the same as _YT_Formats (may change based on download)
        # format
        # format_id
        # ext
        # protocol
        # language
        # format_note
        # filesize_approx
        # tbr
        # width
        # height
        # resolution
        # fps: int
        # dynamic_range
        # vcodec
        # vbr
    stretched_ratio: int | float | None # not in _YT_Formats
        # aspect_ratio
        # acodec
        # abr
        # asr
        # audio_channels


class _WA_Thumbnails(TypedDict):
    url: str
    filesize: int
    preference: int # same as filesize
    id: str
    filepath: NotRequired[str]

class _WA_Formats(TypedDict):
    url: str # url to video (can manual download from there to)
    filesize: int 
    ext: str
    width: int
    height: int
    acodec: str
    abr: float | int | None
    vcodec: str
    format_id: str
    protocol: str
    video_ext: str | Literal['none']
    audio_ext: str | Literal['none']

    # requested_downloads doesn't have these for some reason
    vbr: NotRequired[float | int | None]
    tbr: NotRequired[float | int | None]
    resolution: str # '{widgth}x{height}'
    dynamic_range: str
    aspect_ratio: float | int
    cookies: str
    http_headers: dict[str, str] # idrc about the stuff in here
        # User-Agent: str
        # Accept: str
        # Accept-Language: str
        # Sec-Fetch-Mode: str
    format: str # '{format_id} - {resolution}'

class _WA_RequestedDownloads(_WA_Formats, total=False):

    # almost the same as _WA_Format
    # url: str
    # filesize: int 
    # ext: str
    # width: int
    # height: int
    # acodec: str
    # abr: float | int | None
    # vcodec: str
    # format_id: str
    # protocol: str
    # video_ext: str | Literal['none']
    # audio_ext: str | Literal['none']

    # # doesn't have these for some reason
    # vbr: float | int | None
    # tbr: float | int | None

    # resolution: str # '{widgth}x{height}'
    # dynamic_range: str
    # aspect_ratio: float | int
    # cookies: str
    # http_headers: Dict[str, str] # idrc about the stuff in here
    #     # User-Agent: str
    #     # Accept: str
    #     # Accept-Language: str
    #     # Sec-Fetch-Mode: str
    # format: str # '{format_id} - {resolution}'

    # added fields
    _filename: str
    filename: str
    __postprocessors: list # may contain objects like yt_dlp.postprocessor.ffmpeg.FFmpegMergerPP
    __real_download: bool
    __finaldir: str
    filepath: str
    __write_download_archive: bool

class _WA_V_InfoDict(_WA_Formats, total=False):
    id: Required[str]
    title: str
    description:str
    upload_date: str # YYYYMMDD
    uploader: str # display name
    channel_id: str
    channel_url: str
    duration: int # in seconds
    thumbnails: list[_WA_Thumbnails]
    formats: list[_WA_Formats]
    webpage_url: str
    original_url: str
    webpage_url_basename: str
    webpage_url_domain: str
    extractor: str
    extractor_key: str
    playlist: str | None
    playlist_index: int | None
    thumbnail: str
    display_id: str # same as id
    fulltitle: str # same as title
    duration_string: str # HH:MM:SS no lead 0s
    release_year: int | None
    requested_subtitles: Any
    _has_drm: Any
    epoch: int
    requested_downloads: list[_WA_RequestedDownloads]

    # # same as _WA_Format
    # url: str # url to video (can manual download from there to)
    # filesize: int 
    # ext: str
    # width: int
    # height: int
    # acodec: str
    # abr: float | int | None
    # vcodec: str
    # format_id: int
    # protocol: str
    # video_ext: str | Literal['none']
    # audio_ext: str | Literal['none']
    # vbr: float | int | None
    # tbr: float | int | None
    # resolution: str # '{widgth}x{height}'
    # dynamic_range: str
    # aspect_ratio: float | int
    # cookies: str
    # http_headers: Dict[str, str] # idrc about the stuff in here
    #     # User-Agent: str
    #     # Accept: str
    #     # Accept-Language: str
    #     # Sec-Fetch-Mode: str
    # format: str # '{format_id} - {resolution}'

class _YT_Flat_PL_V_InfoDict(_YT_Flat_V_InfoDict, _PL_V_RelInfo): ...

# will not appear because extractio is video by video instead of full playlist
class _YT_PL_V_InfoDict(_YT_V_InfoDict, _PL_V_RelInfo, total=False):
    album: str
    artists: list[str]
    track: str
    release_date: str # YYYYMMDD
    creators: list[str] # may be the same as artists
    alt_title: str
    artist: str
    creator: str  # may be the same as artist

class _WA_PL_V_InfoDict(_WA_V_InfoDict, _PL_V_RelInfo): ...

# 
# Playlists
# 

class _PL_Thumbnails(TypedDict):
    url: str
    height: int
    width: int
    id: str
    resolution: str # {width}x{height}
    filepath: NotRequired[str] # of the downloaded? thumbnail (probably the highest quality one)

class _YT_PL_InfoDict_Common[ENTRY](TypedDict, total=False):
    id: Required[str]
    title: str
    availability: str | None
    channel_follower_count: str | None
    description: str
    tags: list[str]
    thumbnails: list[_PL_Thumbnails]
    modified_date: str
    view_count: int
    playlist_count: int
    channel: str
    channel_id: str
    uploader_id: str
    uploader: str
    channel_url: str
    uploader_url: str
    _type: str
    entries: Required[list[ENTRY]] # changed from Required[Iterable[ENTRY] | PagedList]
    extractor_key: str
    extractor: str
    webpage_url: str
    original_url: str
    webpage_url_basename: str
    webpage_url_domain: str
    release_year: int | None
    epoch: int

class _YT_Flat_PL_InfoDict[ENTRY](_YT_PL_InfoDict_Common[ENTRY]): ...
class _YT_PL_InfoDict[ENTRY](_YT_PL_InfoDict_Common[ENTRY]): ...

# more concise but not used internally
class YT_Flat_V_InfoDict(_YT_Flat_V_InfoDict, _V_InfoDict_Addons): ...
class YT_V_InfoDict(_YT_V_InfoDict, _V_InfoDict_Addons): ...
class WA_V_InfoDict(_WA_V_InfoDict, _V_InfoDict_Addons): ...

class YT_Flat_PL_V_InfoDict(_YT_Flat_PL_V_InfoDict, _V_InfoDict_Addons): ...
class YT_PL_V_InfoDict(_YT_PL_V_InfoDict, _V_InfoDict_Addons): ...
class WA_PL_V_InfoDict(_WA_PL_V_InfoDict, _V_InfoDict_Addons): ...

class YT_Flat_PL_InfoDict[ENTRY](_YT_Flat_PL_InfoDict[ENTRY], _PL_InfoDict_Addons): ...
class YT_PL_InfoDict[ENTRY](_YT_PL_InfoDict[ENTRY], _PL_InfoDict_Addons): ...
# YT_Flat_PL_InfoDict and YT_PL_InfoDict they are the same
 