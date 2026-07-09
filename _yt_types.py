from typing import TypedDict, Any, NotRequired, Literal

__all__ = [
    'YT_VideoInfo',
    'WA_VideoInfo',
    'FlatPlaylistVideoInfo',
    'YT_PlaylistInfo',
]



# (YouTube) YT_VideoInfo
class _fragment(TypedDict):
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
    has_drm: NotRequired[bool|None]
    acodec: NotRequired[str | Literal['none']]
    vcodec: str | Literal['none']
    dynamic_range: NotRequired[str | None]
    available_at: NotRequired[int]
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
    filepath: NotRequired[str]

class _YT_Subtitle(TypedDict):
    ext: str
    url: str # to download
    name: NotRequired[str] # language spelt out
    impersonate: NotRequired[bool]
    video_id: NotRequired[str] # in 'live_chat'
    protocol: NotRequired[Literal['m3u8_native', 'youtube_live_chat_replay'] | str]
    __yt_dlp_client: NotRequired[Literal['tv', 'ios'] | str]

class _YT_RequestedSubtitles(_YT_Subtitle):
    filepath: str

class _YT_Heatmap(TypedDict):
    start_time: float
    end_time: float
    value: float

class __YT_Format_Compact(TypedDict): 
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

class _YT_RequestedDownloads(__YT_Format_Compact):
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

# see .venv\Lib\site-packages\~t_dlp\extractor\common.py
class YT_VideoInfo(__YT_Format_Compact):
    id: str
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
    channel_is_verified: NotRequired[bool | None]
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
    _has_drm: NotRequired[bool | None]
    epoch: int

    requested_downloads: list[_YT_RequestedDownloads]
    requested_formats: list[_YT_Formats]

    # almost the same as _YT_Format (may change based on download)
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
    stretched_ratio: int | float | None # not in _YT_Forma
        # aspect_ratio
        # acodec
        # abr
        # asr
        # audio_channels

    __x_forwarded_for_ip: NotRequired[None]
    ie_key: NotRequired[str]
    _type: NotRequired[str]
    url: NotRequired[str]
    __post_extractor: NotRequired[Any]



# (WebArchive) WA_VideoInfo

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

class _WA_RequestedDownloads(_WA_Formats):

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

class WA_VideoInfo(_WA_Formats):
    id: str
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
    _has_drm: NotRequired[bool | None]
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

    __post_extractor: NotRequired[Any]


""" YT_VideoInfo vs WA_VideoInfo
# Exclusive to YouTube / WebArchive is missing:
    # view_count: int               *****
    # average_rating: Any           
    # age_limit: int                **
    # categories: list              *
    # tags: list                    ****
    # playable_in_embed: bool       **
    # live_status: str              
    # media_type: str               
    # release_timestamp: int        
    # _format_sort_fields: list     
    # automatic_captions: dict      **
    # subtitles: dict               ***
    # comment_count: str            ****
    # chapters: Any                 
    # heatmap: list                 
    # like_count: int               *****
    # channel: str                          [same as uploader]
    # channel_follower_count: int   *****
    # uploader_id: str              ***
    # uploader_url: str             
    # timestamp: int                ****    [can somewhat be derived form upload_date]
    # availability: str             
    # is_live: bool                 
    # was_live: bool                
    # language: str                 
    # format_note: str              
    # filesize_approx: int          
    # fps: int | float              **
    # stretched_ratio: float        
    # asr: int                      
    # audio_channels: int           

# Exclusive to WebArchive / YouTube is missing:
    # url: str                      
    # filesize: int                 
    # video_ext: str                        [ext covers this]
    # audio_ext: str                        [ext covers this]
    # cookies: str                  
    # http_headers: Dict            
"""




# PlaylistVideoInfo Types

class _PL_Thumbnails(TypedDict):
    url: str
    height: int
    width: int
    id: str
    resolution: str # {width}x{height}
    filepath: NotRequired[str] # of the downloaded thumbnail (probably the highest quality one)

class _YT_Generic_PlaylistInfo(TypedDict):
    id: str
    title: str
    availability: str | None
    channel_follower_count: str | None
    description: str
    tags: list[str]
    thumbnails: list[_PL_Thumbnails | _FlatPL_V_Thumbnails]
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
    
    # add:
    # entries: list[...]

    extractor_key: str
    extractor: str
    webpage_url: str
    original_url: str
    webpage_url_basename: str
    webpage_url_domain: str
    release_year: int | None
    epoch: int


# FlatPlaylistInfo

class _FlatPL_V_Thumbnails(TypedDict):
    url: str
    height: int
    width: int
    preference: int
    filepath: NotRequired[str]
    # id: str
    # resolution: str

class FlatPlaylistVideoInfo(TypedDict):

    # d
    _type: str
    ie_key: str
    id: str
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
    thumbnails: list[_FlatPL_V_Thumbnails]
    timestamp: int | None
    release_timestamp: int | None
    availability: str | None
    view_count: int | None
    live_status: str | None
    channel_is_verified: bool | None
    __x_forwarded_for_ip: Any

class YT_FlatPlaylistInfo(_YT_Generic_PlaylistInfo):
    entries: list[FlatPlaylistVideoInfo]
    _version: NotRequired[dict] # contains stuff but idrc about it



# (Normal/default) PlaylistInfo

class _PL_V_RelInfo(TypedDict):
    # copied from full YT playlist info extraction
    # playlist and playlist_index are in all YT / WA VideoInfos playlist or not
    # that's why they have ' | None', they should be defined
    playlist_count: int # same as 'n_entries'
    playlist: str | None
    playlist_id: str
    playlist_title: str # same as 'playlist'
    playlist_uploader: str
    playlist_uploader_id: str # @handle
    playlist_channel: str
    playlist_channel_id: str # YT id
    playlist_webpage_url: str
    n_entries: int
    playlist_index: int | None
    __last_playlist_index: NotRequired[int] # same as 'n_entries'
    playlist_autonumber: NotRequired[int] # same as 'playlist_index'

class YT_PlaylistVideoInfo(YT_VideoInfo, _PL_V_RelInfo):
    album: NotRequired[str]
    artists: NotRequired[list[str]]
    track: NotRequired[str]
    release_date: NotRequired[str] # YYYYMMDD
    creators: NotRequired[list[str] | None] # may be the same as artists
    alt_title: NotRequired[str]
    artist: NotRequired[str]
    creator: NotRequired[str]  # may be the same as artist

class YT_PlaylistInfo(_YT_Generic_PlaylistInfo):
    entries: list[YT_PlaylistVideoInfo | None]



class WA_PlaylistVideoInfo(WA_VideoInfo, _PL_V_RelInfo): ...


class Playlist_Amalgamation(_YT_Generic_PlaylistInfo):
    entries: list[FlatPlaylistVideoInfo | YT_PlaylistVideoInfo | WA_PlaylistVideoInfo]

y: YT_PlaylistVideoInfo = {
    'playlist_count':               1,
    'playlist_title':               '',
    'playlist_channel_id':          '',
    'playlist_webpage_url':         '',
    'n_entries':                    1,
    'playlist_autonumber':          1,
    'playlist':                     '',
    'playlist_channel':             '',
    'playlist_id':                  '',
    'playlist_uploader':            '',
    'playlist_uploader_id':         '',
    'playlist_index':               1,
      "_type": "url",
      "ie_key": "Youtube",
      "id": "7lVS5Ugo47s",
      "url": "https://www.youtube.com/watch?v=7lVS5Ugo47s",
      "title": "When I'm Gone - Gura x Senzawa Cover Duet",
      "description": "Amazing how those two individual VTubers \"\ud83d\ude09\" are so on spot!\nSame voice, different body: @SamekoSaba You're welcome :3  \n\nSource clips:\nhttps://www.youtube.com/watch?v=cP3eChqUphA\nhttps://www.youtube.com/watch?v=EoA5PaApyC0\n\nOriginal song: Cups - Anna Kendrick\nCover by: Gawr Gura & Senzawa\n\nThumbnail:\nGura: https://www.reddit.com/r/Hololive/comments/j3hpo5/fanart_gawrgura_by_me/\n\n0:00 Gura talks\n0:34 Singing\n2:26 Senzawa talks",
      "duration": 155,
      "channel_id": "UCzBjh5e90GSIFxweeb85ddQ",
      "channel": "marsini",
      "channel_url": "https://www.youtube.com/channel/UCzBjh5e90GSIFxweeb85ddQ",
      "uploader": "marsini",
      "uploader_id": "@marsini",
      "uploader_url": "https://www.youtube.com/@marsini",
      "thumbnails": [
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/3.jpg",
          "preference": -37,
          "id": "0"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/3.webp",
          "preference": -36,
          "id": "1"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/2.jpg",
          "preference": -35,
          "id": "2"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/2.webp",
          "preference": -34,
          "id": "3"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/1.jpg",
          "preference": -33,
          "id": "4"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/1.webp",
          "preference": -32,
          "id": "5"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/mq3.jpg",
          "preference": -31,
          "id": "6"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/mq3.webp",
          "preference": -30,
          "id": "7"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/mq2.jpg",
          "preference": -29,
          "id": "8"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/mq2.webp",
          "preference": -28,
          "id": "9"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/mq1.jpg",
          "preference": -27,
          "id": "10"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/mq1.webp",
          "preference": -26,
          "id": "11"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hq3.jpg",
          "preference": -25,
          "id": "12"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/hq3.webp",
          "preference": -24,
          "id": "13"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hq2.jpg",
          "preference": -23,
          "id": "14"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/hq2.webp",
          "preference": -22,
          "id": "15"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hq1.jpg",
          "preference": -21,
          "id": "16"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/hq1.webp",
          "preference": -20,
          "id": "17"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/sd3.jpg",
          "preference": -19,
          "id": "18"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/sd3.webp",
          "preference": -18,
          "id": "19"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/sd2.jpg",
          "preference": -17,
          "id": "20"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/sd2.webp",
          "preference": -16,
          "id": "21"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/sd1.jpg",
          "preference": -15,
          "id": "22"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/sd1.webp",
          "preference": -14,
          "id": "23"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/default.jpg",
          "height": 90,
          "width": 120,
          "preference": -13,
          "id": "24",
          "resolution": "120x90"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/default.webp",
          "preference": -12,
          "id": "25"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/mqdefault.jpg",
          "height": 180,
          "width": 320,
          "preference": -11,
          "id": "26",
          "resolution": "320x180"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/mqdefault.webp",
          "preference": -10,
          "id": "27"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/0.jpg",
          "preference": -9,
          "id": "28"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/0.webp",
          "preference": -8,
          "id": "29"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hqdefault.jpg?sqp=-oaymwEiCKgBEF5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4CLCkzEAFvZHAl3rjk7Dw-6RdLrkhgA",
          "height": 94,
          "width": 168,
          "preference": -7,
          "id": "30",
          "resolution": "168x94"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hqdefault.jpg?sqp=-oaymwEiCMQBEG5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4CLAKqyCivFSl0WoHo708E6_kvS7b6w",
          "height": 110,
          "width": 196,
          "preference": -7,
          "id": "31",
          "resolution": "196x110"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hqdefault.jpg?sqp=-oaymwEjCPYBEIoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLDT-sChDUCnqFkw80S4GqLmARicEw",
          "height": 138,
          "width": 246,
          "preference": -7,
          "id": "32",
          "resolution": "246x138"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hqdefault.jpg?sqp=-oaymwEjCNACELwBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLA8uuhF8JVh3tACUk_DpqPdUla9DQ",
          "height": 188,
          "width": 336,
          "preference": -7,
          "id": "33",
          "resolution": "336x188"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hqdefault.jpg",
          "height": 360,
          "width": 480,
          "preference": -7,
          "id": "34",
          "resolution": "480x360"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/hqdefault.webp",
          "preference": -6,
          "id": "35"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/sddefault.jpg",
          "height": 480,
          "width": 640,
          "preference": -5,
          "id": "36",
          "resolution": "640x480"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/sddefault.webp",
          "preference": -4,
          "id": "37"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hq720.jpg",
          "preference": -3,
          "id": "38"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/hq720.webp",
          "preference": -2,
          "id": "39"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/maxresdefault.jpg",
          "height": 1080,
          "width": 1920,
          "preference": -1,
          "id": "40",
          "resolution": "1920x1080"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/maxresdefault.webp",
          "preference": 0,
          "id": "41"
        }
      ],
      "timestamp": 1618720941,
      "release_timestamp": None,
      "availability": "public",
      "view_count": 1821516,
      "live_status": "not_live",
      "channel_is_verified": None,
      "__x_forwarded_for_ip": None,
      "playlist": None,
      "playlist_id": "PLXOfMLBzXbbVV8P-wQyZ9MAKxFsGy5v0b",
      "playlist_index": None,
      "playlist_uploader": "Some Random User",
      "playlist_uploader_id": "@somerandomuser8005",
      "playlist_channel": "Some Random User",
      "formats": [
        {
          "format_id": "sb2",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L0/default.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLDfjLTwZbhYgE5At-BfKGTC562rOQ",
          "width": 48,
          "height": 27,
          "fps": 0.6451612903225806,
          "rows": 10,
          "columns": 10,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L0/default.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLDfjLTwZbhYgE5At-BfKGTC562rOQ",
              "duration": 155.0
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "48x27",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb2 - 48x27 (storyboard)"
        },
        {
          "format_id": "sb1",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L1/M$M.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLD6IPGBx5vJqZCH5xsdvbEVa9Zgaw",
          "width": 80,
          "height": 45,
          "fps": 0.5096774193548387,
          "rows": 10,
          "columns": 10,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L1/M0.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLD6IPGBx5vJqZCH5xsdvbEVa9Zgaw",
              "duration": 155.0
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "80x45",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb1 - 80x45 (storyboard)"
        },
        {
          "format_id": "sb0",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L2/M$M.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLBkyf25PeVl7hlEW6gioFZfoIm8vQ",
          "width": 160,
          "height": 90,
          "fps": 0.5096774193548387,
          "rows": 5,
          "columns": 5,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L2/M0.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLBkyf25PeVl7hlEW6gioFZfoIm8vQ",
              "duration": 49.050632911392405
            },
            {
              "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L2/M1.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLBkyf25PeVl7hlEW6gioFZfoIm8vQ",
              "duration": 49.050632911392405
            },
            {
              "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L2/M2.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLBkyf25PeVl7hlEW6gioFZfoIm8vQ",
              "duration": 49.050632911392405
            },
            {
              "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L2/M3.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLBkyf25PeVl7hlEW6gioFZfoIm8vQ",
              "duration": 7.848101265822777
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "160x90",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb0 - 160x90 (storyboard)"
        },
        {
          "asr": 22050,
          "filesize": 944004,
          "format_id": "139",
          "format_note": "low",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 2.0,
          "has_drm": False,
          "tbr": 48.849,
          "filesize_approx": 943994,
          "width": None,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "m4a",
          "vcodec": "none",
          "acodec": "mp4a.40.5",
          "dynamic_range": None,
          "container": "m4a_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=139&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=944004&dur=154.598&lmt=1620800567370438&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAJj7_UPMuB-lFXDvqLiclyl6aFYbtvo1WyiJT89DVT7GAiA8l_SWZviTnGvt2TwbuIiulAUARPyrWLkjlY2t79pz3Q%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "m4a",
          "video_ext": "none",
          "vbr": 0,
          "abr": 48.849,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "139 - audio only (low)"
        },
        {
          "asr": 48000,
          "filesize": 1009704,
          "format_id": "249",
          "format_note": "low",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 2.0,
          "has_drm": False,
          "tbr": 52.275,
          "filesize_approx": 1009698,
          "width": None,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "none",
          "acodec": "opus",
          "dynamic_range": None,
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=249&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=audio%2Fwebm&rqh=1&gir=yes&clen=1009704&dur=154.521&lmt=1620800559724748&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAM2WYwrhgYYyAvDxpk3_iG7Re_Lj_pcwTv7IchlnMEHwAiBiOCGrccVDQ4rmJBPVVnM0GKzeL4DCSKJ-n1KCzHRCOw%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "webm",
          "video_ext": "none",
          "vbr": 0,
          "abr": 52.275,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "249 - audio only (low)"
        },
        {
          "asr": 44100,
          "filesize": 2502029,
          "format_id": "140",
          "format_note": "medium",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 3.0,
          "has_drm": False,
          "tbr": 129.511,
          "filesize_approx": 2502023,
          "width": None,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "m4a",
          "vcodec": "none",
          "acodec": "mp4a.40.2",
          "dynamic_range": None,
          "container": "m4a_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=140&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=2502029&dur=154.552&lmt=1620800567228956&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhALp6ptDtjnVaKzlU9ecf6n9TrY-0DXRlkpKboX8m22g0AiEAlMfSFBoyQeNvzGYxligF666gDaTynAtF8PcBUsWOYAc%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "m4a",
          "video_ext": "none",
          "vbr": 0,
          "abr": 129.511,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "140 - audio only (medium)"
        },
        {
          "asr": 48000,
          "filesize": 2553372,
          "format_id": "251",
          "format_note": "medium",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 3.0,
          "has_drm": False,
          "tbr": 132.195,
          "filesize_approx": 2553362,
          "width": None,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "none",
          "acodec": "opus",
          "dynamic_range": None,
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=audio%2Fwebm&rqh=1&gir=yes&clen=2553372&dur=154.521&lmt=1620800559725924&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgG6NlTnYk5JGl_x2TdVe5BTbEkm4P6gfLeA0oNH8K4zACIBmK2sPEidMW_l0sqvRDvZySi5Jj43l46An3xGd7_Arc&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "webm",
          "video_ext": "none",
          "vbr": 0,
          "abr": 132.195,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "251 - audio only (medium)"
        },
        {
          "format_id": "91",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/itag/91/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D944004%3Bdur%3D154.598%3Bgir%3Dyes%3Bitag%3D139%3Blmt%3D1620800567370438/sgovp/clen%3D1418233%3Bdur%3D154.487%3Bgir%3Dyes%3Bitag%3D160%3Blmt%3D1620811969833604/rqh/1/hls_chunk_host/rr3---sn-qja5mc-5h.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/412/met/1782286468,/mh/A-/mm/31,26/mn/sn-qja5mc-5h,sn-vgqsknd7/ms/au,onr/mv/m/mvi/3/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/playlist_type/CLEAN/dover/11/txp/5535434/mt/1782286149/fvip/4/keepalive/yes/fexp/51565116,51565682,51946837,51987687/n/6IWcqr32jOxDdQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRQIgG6DxON34tVjHO2t4AbrXZ8AN75I1tbpBmIyv5ometA8CIQCV4OfAtl5xkgbySm1mW4FgoYMuOcy1dNLck6VRQSXU6A%3D%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIgIqCG79ltJ1Hs6ymxq082WzSz6ig4Rpn9ZOQQ_bdDqBkCIQCUYsEhayYqMIvrBRg9ZfA36jjco_5kElbN3TqlCDok1w%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-qja5mc-5h.googlevideo.com/cps/412/met/1782286468%2C/mh/A-/mm/31%2C26/mn/sn-qja5mc-5h%2Csn-vgqsknd7/ms/au%2Conr/mv/m/mvi/3/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/go/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/rqh/5/mt/1782286149/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51946837%2C51987687/dover/11/n/6IWcqr32jOxDdQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRQIhAPzFMxvQaPDsdntboHZHd2MuWEuoAslD6KGRhNknC_8MAiAmEiiOMgQWVqW9od5dQ56S5nirOlYyNxN9dbPfrudW8w%3D%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgXXbfb4X6AW6Nd0P99hEp12DVWFQNpKd0yGjJlTRCtl0CIQDnfCGcHu7muhwzP3RI4eR0XCHBMHRK5uyEQ69AojjSvQ%3D%3D/file/index.m3u8",
          "tbr": 166.518,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 0,
          "has_drm": False,
          "width": 256,
          "height": 144,
          "vcodec": "avc1.4D400C",
          "acodec": "mp4a.40.5",
          "dynamic_range": "SDR",
          "available_at": 1782286470,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "91 - 256x144"
        },
        {
          "asr": None,
          "filesize": 1418233,
          "format_id": "160",
          "format_note": "144p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 144,
          "quality": 0.0,
          "has_drm": False,
          "tbr": 73.442,
          "filesize_approx": 1418229,
          "width": 256,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d400c",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=160&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=1418233&dur=154.487&lmt=1620811969833604&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAPVzdtSNCGsIbvpgS2JvqpIYPljL5JKbGHkRPn5sPVYAAiEAvz7o6-RuFe2sGk3_WN5eLu0XGgGzFFETEBQITZ7a_H0%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 73.442,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "160 - 256x144 (144p)"
        },
        {
          "asr": None,
          "filesize": 1760602,
          "format_id": "278",
          "format_note": "144p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 144,
          "quality": 0.0,
          "has_drm": False,
          "tbr": 91.171,
          "filesize_approx": 1760591,
          "width": 256,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=278&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=1760602&dur=154.487&lmt=1663550537598295&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAOGtk0JZnO8ujMXy6ibFyWQxcxUIic0yY6ip20E0hEfwAiBnr9GdMkUHlfCe7njRk5s-VA547ruz8rWPBgBhZ3y_6g%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 91.171,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "278 - 256x144 (144p)"
        },
        {
          "asr": None,
          "filesize": 1076585,
          "format_id": "394",
          "format_note": "144p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 144,
          "quality": 0.0,
          "has_drm": False,
          "tbr": 55.75,
          "filesize_approx": 1076581,
          "width": 256,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.00M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=394&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=1076585&dur=154.487&lmt=1744923181763504&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgV5fiD94OIzwgnon1M3oQdIhwAc_7bDoj_VB2tcEPDSwCIE3_qM3T0yM2ifcmuMvQ9QALOTUal6v1AQeOhxiYel7U&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 55.75,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "394 - 256x144 (144p)"
        },
        {
          "format_id": "92",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/itag/92/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D944004%3Bdur%3D154.598%3Bgir%3Dyes%3Bitag%3D139%3Blmt%3D1620800567370438/sgovp/clen%3D2145254%3Bdur%3D154.487%3Bgir%3Dyes%3Bitag%3D133%3Blmt%3D1620811967507984/rqh/1/hls_chunk_host/rr3---sn-qja5mc-5h.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/412/met/1782286468,/mh/A-/mm/31,26/mn/sn-qja5mc-5h,sn-vgqsknd7/ms/au,onr/mv/m/mvi/3/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/playlist_type/CLEAN/dover/11/txp/5535434/mt/1782286149/fvip/4/keepalive/yes/fexp/51565116,51565682,51946837,51987687/n/6IWcqr32jOxDdQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRgIhALjEPabWba3YJbqhptF8wX-dwRSVGg1yLAhB2qQeoVvaAiEAx96XWk2bYOQSgnvt1RXP7qWvWtiDq0QROFG72ZgSdHc%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIgCl374sBf8z3Xt8ANfK11_c3loxdqn2_91am9ja2uk5ICIQD6yre3LmWyN0U0rGcYE0KD8wnROH39t4XwyaYjywuWfQ%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-qja5mc-5h.googlevideo.com/cps/412/met/1782286468%2C/mh/A-/mm/31%2C26/mn/sn-qja5mc-5h%2Csn-vgqsknd7/ms/au%2Conr/mv/m/mvi/3/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/go/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/rqh/5/mt/1782286149/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51946837%2C51987687/dover/11/n/6IWcqr32jOxDdQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRQIhAPzFMxvQaPDsdntboHZHd2MuWEuoAslD6KGRhNknC_8MAiAmEiiOMgQWVqW9od5dQ56S5nirOlYyNxN9dbPfrudW8w%3D%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgXXbfb4X6AW6Nd0P99hEp12DVWFQNpKd0yGjJlTRCtl0CIQDnfCGcHu7muhwzP3RI4eR0XCHBMHRK5uyEQ69AojjSvQ%3D%3D/file/index.m3u8",
          "tbr": 223.165,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 5,
          "has_drm": False,
          "width": 426,
          "height": 240,
          "vcodec": "avc1.4D4015",
          "acodec": "mp4a.40.5",
          "dynamic_range": "SDR",
          "available_at": 1782286470,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "426x240",
          "aspect_ratio": 1.77,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "92 - 426x240"
        },
        {
          "asr": None,
          "filesize": 2145254,
          "format_id": "133",
          "format_note": "240p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 240,
          "quality": 5.0,
          "has_drm": False,
          "tbr": 111.09,
          "filesize_approx": 2145245,
          "width": 426,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d4015",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=133&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=2145254&dur=154.487&lmt=1620811967507984&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAK7ixwH2xU6RqYpz7hEfzVXiz46WBSapv5fvNQnFbK9aAiAYeHFvRTU2ofn8Fk7gz9LlWqcDdHnI7jjQOO7wUUFEkA%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 111.09,
          "resolution": "426x240",
          "aspect_ratio": 1.77,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "133 - 426x240 (240p)"
        },
        {
          "asr": None,
          "filesize": 2665562,
          "format_id": "242",
          "format_note": "240p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 240,
          "quality": 5.0,
          "has_drm": False,
          "tbr": 138.034,
          "filesize_approx": 2665557,
          "width": 426,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=242&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=2665562&dur=154.487&lmt=1663550467055869&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgKKGdi1bD0UiqYQmrYwqUKTafqD18gM3F4ZkiVnuQ8QUCIEsD2Qj_TJEWhZyTAH5Ceq_SzN32tY6r1-_f487KJed0&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 138.034,
          "resolution": "426x240",
          "aspect_ratio": 1.77,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "242 - 426x240 (240p)"
        },
        {
          "asr": None,
          "filesize": 2078733,
          "format_id": "395",
          "format_note": "240p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 240,
          "quality": 5.0,
          "has_drm": False,
          "tbr": 107.645,
          "filesize_approx": 2078719,
          "width": 426,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.00M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=395&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=2078733&dur=154.487&lmt=1744924110140620&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAMpUMFPHJd4VYutca06B8PRSLgEsP0mnHtSQFM3xN9I_AiEAt_oh-mVHfldk0NU4wwDsQRnDQOcJvVU6YShRXn1akIs%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 107.645,
          "resolution": "426x240",
          "aspect_ratio": 1.77,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "395 - 426x240 (240p)"
        },
        {
          "format_id": "93",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/itag/93/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2502029%3Bdur%3D154.552%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1620800567228956/sgovp/clen%3D3683992%3Bdur%3D154.487%3Bgir%3Dyes%3Bitag%3D134%3Blmt%3D1620811972662483/rqh/1/hls_chunk_host/rr3---sn-qja5mc-5h.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/412/met/1782286468,/mh/A-/mm/31,26/mn/sn-qja5mc-5h,sn-vgqsknd7/ms/au,onr/mv/m/mvi/3/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/playlist_type/CLEAN/dover/11/txp/5535434/mt/1782286149/fvip/4/keepalive/yes/fexp/51565116,51565682,51946837,51987687/n/6IWcqr32jOxDdQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRAIgfvwxCVm9fgBXEcIQoukiLZZAaRiyXN5vqpIBYUH7iboCIEDk-UUB_oMIjCVgKRJD4lc3fDG0Kd4tCEQcfsSZqm80/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRAIgZcxJ8hhrO4m-qQ0A-cT4jCisDTGXXKr0f7uItFGY9VkCIEGmWJ_7Ey3yiR8ahwV7qIJgKT19IREUkalyqdXpJ2GU/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-qja5mc-5h.googlevideo.com/cps/412/met/1782286468%2C/mh/A-/mm/31%2C26/mn/sn-qja5mc-5h%2Csn-vgqsknd7/ms/au%2Conr/mv/m/mvi/3/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/go/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/rqh/5/mt/1782286149/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51946837%2C51987687/dover/11/n/6IWcqr32jOxDdQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRQIhAPzFMxvQaPDsdntboHZHd2MuWEuoAslD6KGRhNknC_8MAiAmEiiOMgQWVqW9od5dQ56S5nirOlYyNxN9dbPfrudW8w%3D%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgXXbfb4X6AW6Nd0P99hEp12DVWFQNpKd0yGjJlTRCtl0CIQDnfCGcHu7muhwzP3RI4eR0XCHBMHRK5uyEQ69AojjSvQ%3D%3D/file/index.m3u8",
          "tbr": 438.822,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 6,
          "has_drm": False,
          "width": 640,
          "height": 360,
          "vcodec": "avc1.4D401E",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286470,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "93 - 640x360"
        },
        {
          "asr": None,
          "filesize": 3683992,
          "format_id": "134",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 190.772,
          "filesize_approx": 3683974,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d401e",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=134&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=3683992&dur=154.487&lmt=1620811972662483&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhALWZCL95ByhS1WjDvupJ4uvCaI1HyVKk0ISMqBW2E2PeAiEA52teWQMi30YsGQrvxM_82yKSnI_87IxZS6q4XJDQ6Vs%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 190.772,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "134 - 640x360 (360p)"
        },
        {
          "asr": 44100,
          "filesize": None,
          "format_id": "18",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": 2,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 320.006,
          "filesize_approx": 6182195,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.42001E",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEXPuyxfqeFMGWm5O45_1km1Z_cGOsfAgKbbc81OLyLmcs1ikwl_xzrWKRvNq_Y7WTCH9R0ZiLqC&spc=SQ-umu_XbF7uiTgaOScEnCsDNy9LTqCV9wnehhaCuHREe4eDr_qL&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&cnr=14&ratebypass=yes&dur=154.552&lmt=1665182629204497&mt=1782286149&fvip=3&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5538434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AHEqNM4wRgIhAPzBRUaVoCTiOOlLU4pKN_QkyTxLHIjiwC74Bd8J52qUAiEArvu8J5pHsL24IQP8_Xg7U3G-lxqFVLG8g1hxIudgOsQ%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "18 - 640x360 (360p)"
        },
        {
          "asr": None,
          "filesize": 4371515,
          "format_id": "243",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 226.375,
          "filesize_approx": 4371499,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=243&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=4371515&dur=154.487&lmt=1663550493681665&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgUCkw1A_Po2tV-445JUPyZtwiILHY9DsTWJZC7CsxDEUCIQC34RIoWhxsJNbZ9NQFimfPR99AQsfFeuVCITSaQm5r4Q%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 226.375,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "243 - 640x360 (360p)"
        },
        {
          "asr": None,
          "filesize": 3431033,
          "format_id": "396",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 177.673,
          "filesize_approx": 3431021,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.01M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=396&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=3431033&dur=154.487&lmt=1744923802257142&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAJvs2Z6CFoC09eiEymKvjLpsRHC2xtyCb_m59mx9JfisAiBe7_rv-vvh1xkACry1mBZJFyAYlp4voFWJw9IwDU_ykw%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 177.673,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "396 - 640x360 (360p)"
        },
        {
          "format_id": "94",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/itag/94/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2502029%3Bdur%3D154.552%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1620800567228956/sgovp/clen%3D5295775%3Bdur%3D154.487%3Bgir%3Dyes%3Bitag%3D135%3Blmt%3D1620811977389502/rqh/1/hls_chunk_host/rr3---sn-qja5mc-5h.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/412/met/1782286468,/mh/A-/mm/31,26/mn/sn-qja5mc-5h,sn-vgqsknd7/ms/au,onr/mv/m/mvi/3/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/playlist_type/CLEAN/dover/11/txp/5535434/mt/1782286149/fvip/4/keepalive/yes/fexp/51565116,51565682,51946837,51987687/n/6IWcqr32jOxDdQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRQIgA9AlUtZW_kr4SkXgSQUvgUntJxHQrYLPl7_hd2B_jr0CIQCX3Pyc5HIBKRg_4XpMJvPPw4tX3rB7u2LcV1Q9lXyMPw%3D%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIhAPkvJoz02hrEFcM896VfuUDTBRZpsIP-2JaNU-qxuR-wAiBxgRMdCekswC9lQbzAwhiER5FbL3d2F0uIIWiokPid8w%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-qja5mc-5h.googlevideo.com/cps/412/met/1782286468%2C/mh/A-/mm/31%2C26/mn/sn-qja5mc-5h%2Csn-vgqsknd7/ms/au%2Conr/mv/m/mvi/3/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/go/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/rqh/5/mt/1782286149/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51946837%2C51987687/dover/11/n/6IWcqr32jOxDdQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRQIhAPzFMxvQaPDsdntboHZHd2MuWEuoAslD6KGRhNknC_8MAiAmEiiOMgQWVqW9od5dQ56S5nirOlYyNxN9dbPfrudW8w%3D%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgXXbfb4X6AW6Nd0P99hEp12DVWFQNpKd0yGjJlTRCtl0CIQDnfCGcHu7muhwzP3RI4eR0XCHBMHRK5uyEQ69AojjSvQ%3D%3D/file/index.m3u8",
          "tbr": 564.378,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 7,
          "has_drm": False,
          "width": 854,
          "height": 480,
          "vcodec": "avc1.4D401E",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286470,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "854x480",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "94 - 854x480"
        },
        {
          "asr": None,
          "filesize": 5295775,
          "format_id": "135",
          "format_note": "480p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 480,
          "quality": 7.0,
          "has_drm": False,
          "tbr": 274.237,
          "filesize_approx": 5295756,
          "width": 854,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d401e",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=135&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=5295775&dur=154.487&lmt=1620811977389502&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgHlm6VikpOJOS6e4gGK1Emyx4ShotqwVfoOEM2j3O_jICIExK170o5VP7dNKjtQaJeYzJLN8NLigy3_reAnMpLBgX&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 274.237,
          "resolution": "854x480",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "135 - 854x480 (480p)"
        },
        {
          "asr": None,
          "filesize": 6173279,
          "format_id": "244",
          "format_note": "480p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 480,
          "quality": 7.0,
          "has_drm": False,
          "tbr": 319.678,
          "filesize_approx": 6173261,
          "width": 854,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=244&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=6173279&dur=154.487&lmt=1663550493738090&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgYs8cxF39Oki6RYmoiLq5Mig7qI8yGx8xw5esBboJ558CIQCliOu67A8cuiE06yWYoOjeZU_NkbxgRB3l01tuEKbRVQ%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 319.678,
          "resolution": "854x480",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "244 - 854x480 (480p)"
        },
        {
          "asr": None,
          "filesize": 5597111,
          "format_id": "397",
          "format_note": "480p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 480,
          "quality": 7.0,
          "has_drm": False,
          "tbr": 289.842,
          "filesize_approx": 5597102,
          "width": 854,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.04M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=397&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=5597111&dur=154.487&lmt=1744926219410447&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgDTuZo6FD_jYepAk6CDh1DYkaaL40L8TDYsBJOPkuujUCIDmEbr_RbxwsVVIOuHzWvzt7cDF4gXfM4wE7aPJ1Ruqp&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 289.842,
          "resolution": "854x480",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "397 - 854x480 (480p)"
        },
        {
          "format_id": "95",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/itag/95/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2502029%3Bdur%3D154.552%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1620800567228956/sgovp/clen%3D8614765%3Bdur%3D154.487%3Bgir%3Dyes%3Bitag%3D136%3Blmt%3D1620811967459677/rqh/1/hls_chunk_host/rr3---sn-qja5mc-5h.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/412/met/1782286468,/mh/A-/mm/31,26/mn/sn-qja5mc-5h,sn-vgqsknd7/ms/au,onr/mv/m/mvi/3/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/playlist_type/CLEAN/dover/11/txp/5535434/mt/1782286149/fvip/4/keepalive/yes/fexp/51565116,51565682,51946837,51987687/n/6IWcqr32jOxDdQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRgIhAJel4ICS2kiKnpsxvZ0W4LWRfXA6mxJBNcrOSoVz0gvyAiEAkC9u8iNWPvBxOzi9ZuZ1Yi_sPcjQR7wKa-BHQ_-x32k%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIhAOXE4CXsRwFxOdWBZdKOizankGdJ5W3WuyiZcBYcpPt7AiAh7VfurX5x1pXMqwj3c6nBZIrpjKxlOcf9x9acqeB48w%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-qja5mc-5h.googlevideo.com/cps/412/met/1782286468%2C/mh/A-/mm/31%2C26/mn/sn-qja5mc-5h%2Csn-vgqsknd7/ms/au%2Conr/mv/m/mvi/3/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/go/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/rqh/5/mt/1782286149/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51946837%2C51987687/dover/11/n/6IWcqr32jOxDdQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRQIhAPzFMxvQaPDsdntboHZHd2MuWEuoAslD6KGRhNknC_8MAiAmEiiOMgQWVqW9od5dQ56S5nirOlYyNxN9dbPfrudW8w%3D%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgXXbfb4X6AW6Nd0P99hEp12DVWFQNpKd0yGjJlTRCtl0CIQDnfCGcHu7muhwzP3RI4eR0XCHBMHRK5uyEQ69AojjSvQ%3D%3D/file/index.m3u8",
          "tbr": 835.965,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 8,
          "has_drm": False,
          "width": 1280,
          "height": 720,
          "vcodec": "avc1.4D401F",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286470,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "95 - 1280x720"
        },
        {
          "asr": None,
          "filesize": 8614765,
          "format_id": "136",
          "format_note": "720p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 720,
          "quality": 8.0,
          "has_drm": False,
          "tbr": 446.109,
          "filesize_approx": 8614755,
          "width": 1280,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d401f",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=136&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=8614765&dur=154.487&lmt=1620811967459677&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAMF8zAtDCip1fAh9-zwIiSvKOjSWh6o_gBahuhfE4tsdAiAU7GaK8xkGpQihjKMozU1jeDnY9O4vcrGb7vxtvfRyew%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 446.109,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "136 - 1280x720 (720p)"
        },
        {
          "asr": None,
          "filesize": 9558929,
          "format_id": "247",
          "format_note": "720p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 720,
          "quality": 8.0,
          "has_drm": False,
          "tbr": 495.002,
          "filesize_approx": 9558921,
          "width": 1280,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=247&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=9558929&dur=154.487&lmt=1663550493701245&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgDKn74xNNY9RFybUrxfU7ZdyxBabVGZL42DIM3Oy6fYACIQC8mMROC8sRC3MKPRa7hQb0ZXThYd-FLNzZCbJRBX4Qiw%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 495.002,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "247 - 1280x720 (720p)"
        },
        {
          "asr": None,
          "filesize": 9646191,
          "format_id": "398",
          "format_note": "720p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 720,
          "quality": 8.0,
          "has_drm": False,
          "tbr": 499.521,
          "filesize_approx": 9646187,
          "width": 1280,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.05M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=398&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=9646191&dur=154.487&lmt=1744925226812899&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhALVZDtSf0KLv_Ck9KGDJUBu6Kc-MhLe_-UO8ug25KsTWAiB3u23OkaKcI0nn5ZGuM5LQ_uCUClos8nOwsCIW2KfV_Q%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 499.521,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "398 - 1280x720 (720p)"
        },
        {
          "format_id": "96",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/itag/96/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2502029%3Bdur%3D154.552%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1620800567228956/sgovp/clen%3D27917372%3Bdur%3D154.487%3Bgir%3Dyes%3Bitag%3D137%3Blmt%3D1620811960251957/rqh/1/hls_chunk_host/rr3---sn-qja5mc-5h.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/412/met/1782286468,/mh/A-/mm/31,26/mn/sn-qja5mc-5h,sn-vgqsknd7/ms/au,onr/mv/m/mvi/3/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/playlist_type/CLEAN/dover/11/txp/5535434/mt/1782286149/fvip/4/keepalive/yes/fexp/51565116,51565682,51946837,51987687/n/6IWcqr32jOxDdQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRQIhAN2BBdObEsPkXjnzXHJjLzXb5k23AsmX5_vco2zBl-akAiBwot6g-xr66Nu6SGni1DtXwUu_2Exzbh2uWTUUw0_aLg%3D%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRAIgU0w2mAmSA7WVW-bjZS5z14yujyugkUT_dn5C8lQRNV8CIA7hQKEfVl5r4r9kM6LfK_8FTf3oF0-9cxhZUa5UPMj9/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-qja5mc-5h.googlevideo.com/cps/412/met/1782286468%2C/mh/A-/mm/31%2C26/mn/sn-qja5mc-5h%2Csn-vgqsknd7/ms/au%2Conr/mv/m/mvi/3/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/go/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/rqh/5/mt/1782286149/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51946837%2C51987687/dover/11/n/6IWcqr32jOxDdQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRQIhAPzFMxvQaPDsdntboHZHd2MuWEuoAslD6KGRhNknC_8MAiAmEiiOMgQWVqW9od5dQ56S5nirOlYyNxN9dbPfrudW8w%3D%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgXXbfb4X6AW6Nd0P99hEp12DVWFQNpKd0yGjJlTRCtl0CIQDnfCGcHu7muhwzP3RI4eR0XCHBMHRK5uyEQ69AojjSvQ%3D%3D/file/index.m3u8",
          "tbr": 2333.993,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 9,
          "has_drm": False,
          "width": 1920,
          "height": 1080,
          "vcodec": "avc1.640028",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286470,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "1920x1080",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "96 - 1920x1080"
        },
        {
          "asr": None,
          "filesize": 27917372,
          "format_id": "137",
          "format_note": "1080p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 1080,
          "quality": 9.0,
          "has_drm": False,
          "tbr": 1445.681,
          "filesize_approx": 27917365,
          "width": 1920,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.640028",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=137&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=27917372&dur=154.487&lmt=1620811960251957&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhANLbrHHvRiQOIdEX1QR291Tb_cGFrQm_tJn-TBNBmUhaAiEAy4mT4tWZGeGmnIJtpvg0wCtaQSTR1dxHIq2okyEA3CI%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 1445.681,
          "resolution": "1920x1080",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "137 - 1920x1080 (1080p)"
        },
        {
          "asr": None,
          "filesize": 27733188,
          "format_id": "248",
          "format_note": "1080p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 1080,
          "quality": 9.0,
          "has_drm": False,
          "tbr": 1436.143,
          "filesize_approx": 27733177,
          "width": 1920,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=248&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=27733188&dur=154.487&lmt=1663548451242854&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAPa_9DKqCxjSEpkjUOYUBzc4JZC6W3dhgADzAEEB7YvXAiEA5zyL7jRMR9eP4PAAqK7RvdAGw5xgv9QrC08hKOwX5CE%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 1436.143,
          "resolution": "1920x1080",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "248 - 1920x1080 (1080p)"
        },
        {
          "asr": None,
          "filesize": 16699919,
          "format_id": "399",
          "format_note": "1080p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 1080,
          "quality": 9.0,
          "has_drm": False,
          "tbr": 864.793,
          "filesize_approx": 16699909,
          "width": 1920,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.08M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=399&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=16699919&dur=154.487&lmt=1744928093943735&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAJkmkViGatyMqvhrd3uHTFUKi8mOSHFIPdmmqE6GVz8eAiBtU1XQpgkRbCn-sZiLQCop3Vv1-qbxH8Bka3lMb-OE7A%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 864.793,
          "resolution": "1920x1080",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "399 - 1920x1080 (1080p)"
        }
      ],
      "thumbnail": "https://i.ytimg.com/vi/7lVS5Ugo47s/maxresdefault.jpg",
      "average_rating": None,
      "age_limit": 0,
      "webpage_url": "https://www.youtube.com/watch?v=7lVS5Ugo47s",
      "categories": ["Music"],
      "tags": [],
      "playable_in_embed": True,
      "media_type": "video",
      "_format_sort_fields": [
        "quality",
        "res",
        "fps",
        "hdr:12",
        "source",
        "vcodec",
        "channels",
        "acodec",
        "lang",
        "proto"
      ],
      "automatic_captions": {},
      "subtitles": {},
      "comment_count": 3700,
      "chapters": [
        { "start_time": 0.0, "title": "Gura talks", "end_time": 34.0 },
        { "start_time": 34.0, "title": "Singing", "end_time": 146.0 },
        { "start_time": 146.0, "title": "Senzawa talks", "end_time": 155 }
      ],
      "heatmap": [
        { "start_time": 0.0, "end_time": 1.55, "value": 0.44198208885178764 },
        { "start_time": 1.55, "end_time": 3.1, "value": 0.04496327492997547 },
        { "start_time": 3.1, "end_time": 4.65, "value": 0.09446166645306969 },
        { "start_time": 4.65, "end_time": 6.2, "value": 0.08504487286424549 },
        { "start_time": 6.2, "end_time": 7.75, "value": 0.04237902925423101 },
        { "start_time": 7.75, "end_time": 9.3, "value": 0.022186115352034207 },
        { "start_time": 9.3, "end_time": 10.85, "value": 0.011618731227283794 },
        { "start_time": 10.85, "end_time": 12.4, "value": 0.0 },
        {
          "start_time": 12.4,
          "end_time": 13.95,
          "value": 0.0014062402871010036
        },
        {
          "start_time": 13.95,
          "end_time": 15.5,
          "value": 0.016484659265045297
        },
        {
          "start_time": 15.5,
          "end_time": 17.05,
          "value": 0.029073992937467305
        },
        {
          "start_time": 17.05,
          "end_time": 18.6,
          "value": 0.054831205335246984
        },
        { "start_time": 18.6, "end_time": 20.15, "value": 0.07199606959339523 },
        { "start_time": 20.15, "end_time": 21.7, "value": 0.07734171588979863 },
        { "start_time": 21.7, "end_time": 23.25, "value": 0.07534576462190752 },
        { "start_time": 23.25, "end_time": 24.8, "value": 0.07821490811357981 },
        { "start_time": 24.8, "end_time": 26.35, "value": 0.08516686479244623 },
        { "start_time": 26.35, "end_time": 27.9, "value": 0.10529778279670494 },
        { "start_time": 27.9, "end_time": 29.45, "value": 0.10516787472562232 },
        { "start_time": 29.45, "end_time": 31.0, "value": 0.1317992792810209 },
        { "start_time": 31.0, "end_time": 32.55, "value": 0.13706834731101958 },
        { "start_time": 32.55, "end_time": 34.1, "value": 0.5809295618273258 },
        { "start_time": 34.1, "end_time": 35.65, "value": 0.5765790163550845 },
        { "start_time": 35.65, "end_time": 37.2, "value": 0.3206435340861613 },
        { "start_time": 37.2, "end_time": 38.75, "value": 0.3400711652912299 },
        { "start_time": 38.75, "end_time": 40.3, "value": 0.2905122777709542 },
        { "start_time": 40.3, "end_time": 41.85, "value": 0.2578456058824108 },
        { "start_time": 41.85, "end_time": 43.4, "value": 0.25771644776170644 },
        { "start_time": 43.4, "end_time": 44.95, "value": 0.23544567134474603 },
        { "start_time": 44.95, "end_time": 46.5, "value": 0.21682473676325084 },
        { "start_time": 46.5, "end_time": 48.05, "value": 0.21583230242932258 },
        { "start_time": 48.05, "end_time": 49.6, "value": 0.19835995851607818 },
        { "start_time": 49.6, "end_time": 51.15, "value": 0.19818646999523531 },
        { "start_time": 51.15, "end_time": 52.7, "value": 0.19268091761261796 },
        { "start_time": 52.7, "end_time": 54.25, "value": 0.18770158041209606 },
        { "start_time": 54.25, "end_time": 55.8, "value": 0.1872382777339566 },
        { "start_time": 55.8, "end_time": 57.35, "value": 0.1999346043270137 },
        { "start_time": 57.35, "end_time": 58.9, "value": 0.2016064103758468 },
        { "start_time": 58.9, "end_time": 60.45, "value": 0.20600028631438885 },
        { "start_time": 60.45, "end_time": 62.0, "value": 0.21415383015490475 },
        { "start_time": 62.0, "end_time": 63.55, "value": 0.21594537828080376 },
        { "start_time": 63.55, "end_time": 65.1, "value": 0.2202282615633599 },
        { "start_time": 65.1, "end_time": 66.65, "value": 0.22438157008611265 },
        { "start_time": 66.65, "end_time": 68.2, "value": 0.2379761705767135 },
        { "start_time": 68.2, "end_time": 69.75, "value": 0.24607371812231757 },
        { "start_time": 69.75, "end_time": 71.3, "value": 0.2515073585964395 },
        { "start_time": 71.3, "end_time": 72.85, "value": 0.2694421719096253 },
        { "start_time": 72.85, "end_time": 74.4, "value": 0.2890406251453029 },
        { "start_time": 74.4, "end_time": 75.95, "value": 0.3017026206765986 },
        { "start_time": 75.95, "end_time": 77.5, "value": 0.34010657961464885 },
        { "start_time": 77.5, "end_time": 79.05, "value": 0.383706111445626 },
        { "start_time": 79.05, "end_time": 80.6, "value": 0.42452257742279387 },
        { "start_time": 80.6, "end_time": 82.15, "value": 0.4573275734922206 },
        { "start_time": 82.15, "end_time": 83.7, "value": 0.48643714740874644 },
        { "start_time": 83.7, "end_time": 85.25, "value": 0.4777140579198343 },
        { "start_time": 85.25, "end_time": 86.8, "value": 0.4549915613916879 },
        { "start_time": 86.8, "end_time": 88.35, "value": 0.47099116941762353 },
        { "start_time": 88.35, "end_time": 89.9, "value": 0.46586217545272424 },
        { "start_time": 89.9, "end_time": 91.45, "value": 0.4774880728725116 },
        { "start_time": 91.45, "end_time": 93.0, "value": 0.5103643975556951 },
        { "start_time": 93.0, "end_time": 94.55, "value": 0.5530822377252705 },
        { "start_time": 94.55, "end_time": 96.1, "value": 0.5535510400395174 },
        { "start_time": 96.1, "end_time": 97.65, "value": 0.5127255746578101 },
        { "start_time": 97.65, "end_time": 99.2, "value": 0.46719758709298737 },
        { "start_time": 99.2, "end_time": 100.75, "value": 0.4390292842290269 },
        {
          "start_time": 100.75,
          "end_time": 102.3,
          "value": 0.42253112585717245
        },
        {
          "start_time": 102.3,
          "end_time": 103.85,
          "value": 0.40677200191920637
        },
        {
          "start_time": 103.85,
          "end_time": 105.4,
          "value": 0.4053181814469943
        },
        {
          "start_time": 105.4,
          "end_time": 106.95,
          "value": 0.4084929713817269
        },
        { "start_time": 106.95, "end_time": 108.5, "value": 0.412193559859456 },
        {
          "start_time": 108.5,
          "end_time": 110.05,
          "value": 0.42204465804512603
        },
        {
          "start_time": 110.05,
          "end_time": 111.6,
          "value": 0.42926126387970664
        },
        {
          "start_time": 111.6,
          "end_time": 113.15,
          "value": 0.42909152511075516
        },
        {
          "start_time": 113.15,
          "end_time": 114.7,
          "value": 0.42799476434642575
        },
        {
          "start_time": 114.7,
          "end_time": 116.25,
          "value": 0.4402459537260618
        },
        { "start_time": 116.25, "end_time": 117.8, "value": 0.447525222081139 },
        {
          "start_time": 117.8,
          "end_time": 119.35,
          "value": 0.46057502528582694
        },
        {
          "start_time": 119.35,
          "end_time": 120.9,
          "value": 0.5155098904289166
        },
        {
          "start_time": 120.9,
          "end_time": 122.45,
          "value": 0.5435981985858602
        },
        {
          "start_time": 122.45,
          "end_time": 124.0,
          "value": 0.5793251679847183
        },
        {
          "start_time": 124.0,
          "end_time": 125.55,
          "value": 0.7637802965370458
        },
        {
          "start_time": 125.55,
          "end_time": 127.1,
          "value": 0.7819024307891628
        },
        {
          "start_time": 127.1,
          "end_time": 128.65,
          "value": 0.7689662867306947
        },
        {
          "start_time": 128.65,
          "end_time": 130.2,
          "value": 0.7264412671361579
        },
        {
          "start_time": 130.2,
          "end_time": 131.75,
          "value": 0.6753889784292606
        },
        { "start_time": 131.75, "end_time": 133.3, "value": 0.619417848519023 },
        {
          "start_time": 133.3,
          "end_time": 134.85,
          "value": 0.5906655842938392
        },
        {
          "start_time": 134.85,
          "end_time": 136.4,
          "value": 0.5912622114836735
        },
        {
          "start_time": 136.4,
          "end_time": 137.95,
          "value": 0.5850311237739769
        },
        {
          "start_time": 137.95,
          "end_time": 139.5,
          "value": 0.5897046478757989
        },
        { "start_time": 139.5, "end_time": 141.05, "value": 0.641570382759674 },
        {
          "start_time": 141.05,
          "end_time": 142.6,
          "value": 0.6715450661014596
        },
        {
          "start_time": 142.6,
          "end_time": 144.15,
          "value": 0.7153704996519397
        },
        {
          "start_time": 144.15,
          "end_time": 145.7,
          "value": 0.7864486299823161
        },
        { "start_time": 145.7, "end_time": 147.25, "value": 1.0 },
        {
          "start_time": 147.25,
          "end_time": 148.8,
          "value": 0.9256469196954802
        },
        {
          "start_time": 148.8,
          "end_time": 150.35,
          "value": 0.9099634574179009
        },
        {
          "start_time": 150.35,
          "end_time": 151.9,
          "value": 0.8516904798132524
        },
        {
          "start_time": 151.9,
          "end_time": 153.45,
          "value": 0.7471827280761589
        },
        { "start_time": 153.45, "end_time": 155.0, "value": 0.6347133364675704 }
      ],
      "like_count": 56935,
      "channel_follower_count": 1820,
      "creators": None,
      "upload_date": "20210418",
      "__post_extractor": None,
      "original_url": "7lVS5Ugo47s",
      "webpage_url_basename": "watch",
      "webpage_url_domain": "youtube.com",
      "extractor": "youtube",
      "extractor_key": "Youtube",
      "display_id": "7lVS5Ugo47s",
      "fulltitle": "When I'm Gone - Gura x Senzawa Cover Duet",
      "duration_string": "2:35",
      "release_year": None,
      "is_live": False,
      "was_live": False,
      "requested_subtitles": None,
      "_has_drm": None,
      "epoch": 1782286471
    }


x: Playlist_Amalgamation = {
  "id": "PLXOfMLBzXbbVV8P-wQyZ9MAKxFsGy5v0b",
  "title": "When I'm Gone",
  "availability": "private",
  "channel_follower_count": None,
  "description": "",
  "tags": [],
  "thumbnails": [
    {
      "url": "https://i.ytimg.com/vi/cP3eChqUphA/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLBEygfuNvSVv0W_8CR8aBITdh76uQ",
      "height": 94,
      "width": 168,
      "id": "0",
      "resolution": "168x94"
    },
    {
      "url": "https://i.ytimg.com/vi/cP3eChqUphA/hqdefault.jpg?sqp=-oaymwEWCMQBEG5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLDAi48k4tmtPc0O4ovbmP53XDx6-w",
      "height": 110,
      "width": 196,
      "id": "1",
      "resolution": "196x110"
    },
    {
      "url": "https://i.ytimg.com/vi/cP3eChqUphA/hqdefault.jpg?sqp=-oaymwEXCPYBEIoBSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLClS0e0kLzlGzH7y-djx0cKyta6CA",
      "height": 138,
      "width": 246,
      "id": "2",
      "resolution": "246x138"
    },
    {
      "url": "https://i.ytimg.com/vi/cP3eChqUphA/hqdefault.jpg?sqp=-oaymwEXCNACELwBSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLAEN87LwPYaxDV3osLKUL3Ii5nckQ",
      "height": 188,
      "width": 336,
      "id": "3",
      "resolution": "336x188"
    }
  ],
  "modified_date": "20241125",
  "view_count": 11,
  "playlist_count": 3,
  "channel": "Some Random User",
  "channel_id": "UCNneC8sL4qcbXn1xRYEd3OA",
  "uploader_id": "@somerandomuser8005",
  "uploader": "Some Random User",
  "channel_url": "https://www.youtube.com/channel/UCNneC8sL4qcbXn1xRYEd3OA",
  "uploader_url": "https://www.youtube.com/@somerandomuser8005",
  "_type": "playlist",
  "entries": [
    {
    'playlist_count':               1,
    'playlist_title':               '',
    'playlist_channel_id':          '',
    'playlist_webpage_url':         '',
    'n_entries':                    1,
    'playlist_autonumber':          1,
    'playlist':                     '',
    'playlist_channel':             '',
    'playlist_id':                  '',
    'playlist_uploader':            '',
    'playlist_uploader_id':         '',
    'playlist_index':               1,
      "_type": "url",
      "ie_key": "Youtube",
      "id": "cP3eChqUphA",
      "url": "https://www.youtube.com/watch?v=cP3eChqUphA",
      "title": "Senzawa - [\"When I'm Gone\"] Cups Cover",
      "description": "https://www.twitch.tv/senzawa\nJust wanted to save this.\nI just stumbled into the live stream last week and barely caught this awesome cover.\nI had to clip it and stitch it back together.",
      "duration": 135,
      "channel_id": "UCA8clt66DdCnGelwL_y7aFw",
      "channel": "Psyda",
      "channel_url": "https://www.youtube.com/channel/UCA8clt66DdCnGelwL_y7aFw",
      "uploader": "Psyda",
      "uploader_id": "@Psyda",
      "uploader_url": "https://www.youtube.com/@Psyda",
      "thumbnails": [
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/3.jpg",
          "preference": -37,
          "id": "0"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/3.webp",
          "preference": -36,
          "id": "1"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/2.jpg",
          "preference": -35,
          "id": "2"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/2.webp",
          "preference": -34,
          "id": "3"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/1.jpg",
          "preference": -33,
          "id": "4"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/1.webp",
          "preference": -32,
          "id": "5"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/mq3.jpg",
          "preference": -31,
          "id": "6"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/mq3.webp",
          "preference": -30,
          "id": "7"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/mq2.jpg",
          "preference": -29,
          "id": "8"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/mq2.webp",
          "preference": -28,
          "id": "9"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/mq1.jpg",
          "preference": -27,
          "id": "10"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/mq1.webp",
          "preference": -26,
          "id": "11"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/hq3.jpg",
          "preference": -25,
          "id": "12"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/hq3.webp",
          "preference": -24,
          "id": "13"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/hq2.jpg",
          "preference": -23,
          "id": "14"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/hq2.webp",
          "preference": -22,
          "id": "15"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/hq1.jpg",
          "preference": -21,
          "id": "16"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/hq1.webp",
          "preference": -20,
          "id": "17"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/sd3.jpg",
          "preference": -19,
          "id": "18"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/sd3.webp",
          "preference": -18,
          "id": "19"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/sd2.jpg",
          "preference": -17,
          "id": "20"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/sd2.webp",
          "preference": -16,
          "id": "21"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/sd1.jpg",
          "preference": -15,
          "id": "22"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/sd1.webp",
          "preference": -14,
          "id": "23"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/default.jpg",
          "height": 90,
          "width": 120,
          "preference": -13,
          "id": "24",
          "resolution": "120x90"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/default.webp",
          "preference": -12,
          "id": "25"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/mqdefault.jpg",
          "height": 180,
          "width": 320,
          "preference": -11,
          "id": "26",
          "resolution": "320x180"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/mqdefault.webp",
          "preference": -10,
          "id": "27"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/0.jpg",
          "preference": -9,
          "id": "28"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/0.webp",
          "preference": -8,
          "id": "29"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/hqdefault.jpg?sqp=-oaymwEiCKgBEF5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4CLD-Euf84B6ckQWav12-osvcx27pFw",
          "height": 94,
          "width": 168,
          "preference": -7,
          "id": "30",
          "resolution": "168x94"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/hqdefault.jpg?sqp=-oaymwEiCMQBEG5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4CLD4Bdl0qjoSlMYicB8YOPhqIl0kZA",
          "height": 110,
          "width": 196,
          "preference": -7,
          "id": "31",
          "resolution": "196x110"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/hqdefault.jpg?sqp=-oaymwEjCPYBEIoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLAsPuTsW_usH_NWxyNSntAzAV104w",
          "height": 138,
          "width": 246,
          "preference": -7,
          "id": "32",
          "resolution": "246x138"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/hqdefault.jpg?sqp=-oaymwEjCNACELwBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLBgChIsjtAs2SOFCoFUT6v_Wjfb6Q",
          "height": 188,
          "width": 336,
          "preference": -7,
          "id": "33",
          "resolution": "336x188"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/hqdefault.jpg",
          "height": 360,
          "width": 480,
          "preference": -7,
          "id": "34",
          "resolution": "480x360"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/hqdefault.webp",
          "preference": -6,
          "id": "35"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/sddefault.jpg",
          "height": 480,
          "width": 640,
          "preference": -5,
          "id": "36",
          "resolution": "640x480"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/sddefault.webp",
          "preference": -4,
          "id": "37"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/hq720.jpg",
          "preference": -3,
          "id": "38"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/hq720.webp",
          "preference": -2,
          "id": "39"
        },
        {
          "url": "https://i.ytimg.com/vi/cP3eChqUphA/maxresdefault.jpg",
          "height": 1080,
          "width": 1920,
          "preference": -1,
          "id": "40",
          "resolution": "1920x1080"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/cP3eChqUphA/maxresdefault.webp",
          "preference": 0,
          "id": "41",
          "filepath": "test\\When I'm Gone [...AKxFsGy5v0b]\\Videos\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover [cP3eChqUphA]\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover.webp"
        }
      ],
      "timestamp": 1570771308,
      "release_timestamp": None,
      "availability": "public",
      "view_count": 600849,
      "live_status": "not_live",
      "channel_is_verified": None,
      "__x_forwarded_for_ip": None,
      "playlist": None,
      "playlist_id": "PLXOfMLBzXbbVV8P-wQyZ9MAKxFsGy5v0b",
      "playlist_index": None,
      "playlist_uploader": "Some Random User",
      "playlist_uploader_id": "@somerandomuser8005",
      "playlist_channel": "Some Random User",
      "formats": [
        {
          "format_id": "sb2",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/cP3eChqUphA/storyboard3_L0/default.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCI-LgO0F&sigh=rs$AOn4CLAkHoIOP9_SNcXsZJrWKyCCvxIG4A",
          "width": 48,
          "height": 27,
          "fps": 0.7407407407407407,
          "rows": 10,
          "columns": 10,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/cP3eChqUphA/storyboard3_L0/default.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCI-LgO0F&sigh=rs$AOn4CLAkHoIOP9_SNcXsZJrWKyCCvxIG4A",
              "duration": 135.0
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "48x27",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb2 - 48x27 (storyboard)"
        },
        {
          "format_id": "sb1",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/cP3eChqUphA/storyboard3_L1/M$M.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCI-LgO0F&sigh=rs$AOn4CLD2yHJchDF4oPGxEmgSjmIT5k0pug",
          "width": 80,
          "height": 45,
          "fps": 0.5111111111111111,
          "rows": 10,
          "columns": 10,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/cP3eChqUphA/storyboard3_L1/M0.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCI-LgO0F&sigh=rs$AOn4CLD2yHJchDF4oPGxEmgSjmIT5k0pug",
              "duration": 135.0
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "80x45",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb1 - 80x45 (storyboard)"
        },
        {
          "format_id": "sb0",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/cP3eChqUphA/storyboard3_L2/M$M.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCI-LgO0F&sigh=rs$AOn4CLCf2LQBk-qZmqhXDYV0jqyCqu4Mfw",
          "width": 160,
          "height": 90,
          "fps": 0.5111111111111111,
          "rows": 5,
          "columns": 5,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/cP3eChqUphA/storyboard3_L2/M0.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCI-LgO0F&sigh=rs$AOn4CLCf2LQBk-qZmqhXDYV0jqyCqu4Mfw",
              "duration": 48.913043478260875
            },
            {
              "url": "https://i.ytimg.com/sb/cP3eChqUphA/storyboard3_L2/M1.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCI-LgO0F&sigh=rs$AOn4CLCf2LQBk-qZmqhXDYV0jqyCqu4Mfw",
              "duration": 48.913043478260875
            },
            {
              "url": "https://i.ytimg.com/sb/cP3eChqUphA/storyboard3_L2/M2.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCI-LgO0F&sigh=rs$AOn4CLCf2LQBk-qZmqhXDYV0jqyCqu4Mfw",
              "duration": 37.17391304347825
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "160x90",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb0 - 160x90 (storyboard)"
        },
        {
          "asr": 22050,
          "filesize": 823012,
          "format_id": "139",
          "format_note": "low",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 2.0,
          "has_drm": False,
          "tbr": 48.855,
          "filesize_approx": 823011,
          "width": None,
          "language": "en",
          "language_preference": -1,
          "preference": None,
          "ext": "m4a",
          "vcodec": "none",
          "acodec": "mp4a.40.5",
          "dynamic_range": None,
          "container": "m4a_dash",
          "url": "https://rr2---sn-a5meknzr.googlevideo.com/videoplayback?expire=1782308038&ei=Zog7ataHLdugsfIPr8XFkA8&ip=47.147.88.26&id=o-AKNIFvcG3SgOlNxz7CVhQ57Qsz1fyHRPBgdWYne_-Rl-&itag=139&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=381&met=1782286438%2C&mh=As&mm=31%2C26&mn=sn-a5meknzr%2Csn-vgqskn6y&ms=au%2Conr&mv=m&mvi=2&pl=12&rms=au%2Cau&initcwndbps=3750000&bui=ARmQxEW1Gsi3sb39UJHNcf0H4Zq8G-03EjXEnskInoyyW2K1yzd-cKsh_2UPSllc-wBVdtv6nN2Gm0L_&spc=SQ-umpTvy_oesEoe5hMTm0g4-6gnSxSxrPlXnPChMX6G&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=823012&dur=134.768&lmt=1744758845650026&mt=1782285909&fvip=4&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5308224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgIzBOwuPbIA6UUZW7SeXZrgKtrw66TswshHlw7fNXrdUCIA8X7TiB9G1ka90OMuRAjPxLP7tSUy9GZQC_X5vQRRVw&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRgIhAOAZex_mL1p_pDQPHZETwG81pWnS4VEv41O_YSWUkYghAiEAuyCow7d5mP3LhYVmbD-Iuaeu7Qxe7umQtw21bFb6mC4%3D",
          "available_at": 1782286439,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "m4a",
          "video_ext": "none",
          "vbr": 0,
          "abr": 48.855,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "139 - audio only (low)"
        },
        {
          "asr": 44100,
          "filesize": 2180941,
          "format_id": "140",
          "format_note": "medium",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 3.0,
          "has_drm": False,
          "tbr": 129.53,
          "filesize_approx": 2180928,
          "width": None,
          "language": "en",
          "language_preference": -1,
          "preference": None,
          "ext": "m4a",
          "vcodec": "none",
          "acodec": "mp4a.40.2",
          "dynamic_range": None,
          "container": "m4a_dash",
          "url": "https://rr2---sn-a5meknzr.googlevideo.com/videoplayback?expire=1782308038&ei=Zog7ataHLdugsfIPr8XFkA8&ip=47.147.88.26&id=o-AKNIFvcG3SgOlNxz7CVhQ57Qsz1fyHRPBgdWYne_-Rl-&itag=140&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=381&met=1782286438%2C&mh=As&mm=31%2C26&mn=sn-a5meknzr%2Csn-vgqskn6y&ms=au%2Conr&mv=m&mvi=2&pl=12&rms=au%2Cau&initcwndbps=3750000&bui=ARmQxEW1Gsi3sb39UJHNcf0H4Zq8G-03EjXEnskInoyyW2K1yzd-cKsh_2UPSllc-wBVdtv6nN2Gm0L_&spc=SQ-umpTvy_oesEoe5hMTm0g4-6gnSxSxrPlXnPChMX6G&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=2180941&dur=134.698&lmt=1744758845381853&mt=1782285909&fvip=4&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5308224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgBSqWgg0_h2e9ipdDvtmQTBpjNOOFj96v4qRB0HzQQXoCIASme5nLydUXo7B_ben1aUXRqK62zgW3eHC6rvv6iGZc&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRgIhAOAZex_mL1p_pDQPHZETwG81pWnS4VEv41O_YSWUkYghAiEAuyCow7d5mP3LhYVmbD-Iuaeu7Qxe7umQtw21bFb6mC4%3D",
          "available_at": 1782286439,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "m4a",
          "video_ext": "none",
          "vbr": 0,
          "abr": 129.53,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "140 - audio only (medium)"
        },
        {
          "asr": 48000,
          "filesize": 2393857,
          "format_id": "251",
          "format_note": "medium",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 3.0,
          "has_drm": False,
          "tbr": 142.215,
          "filesize_approx": 2393851,
          "width": None,
          "language": "en",
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "none",
          "acodec": "opus",
          "dynamic_range": None,
          "container": "webm_dash",
          "url": "https://rr2---sn-a5meknzr.googlevideo.com/videoplayback?expire=1782308038&ei=Zog7ataHLdugsfIPr8XFkA8&ip=47.147.88.26&id=o-AKNIFvcG3SgOlNxz7CVhQ57Qsz1fyHRPBgdWYne_-Rl-&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=381&met=1782286438%2C&mh=As&mm=31%2C26&mn=sn-a5meknzr%2Csn-vgqskn6y&ms=au%2Conr&mv=m&mvi=2&pl=12&rms=au%2Cau&initcwndbps=3750000&bui=ARmQxEW1Gsi3sb39UJHNcf0H4Zq8G-03EjXEnskInoyyW2K1yzd-cKsh_2UPSllc-wBVdtv6nN2Gm0L_&spc=SQ-umpTvy_oesEoe5hMTm0g4-6gnSxSxrPlXnPChMX6G&vprv=1&svpuc=1&mime=audio%2Fwebm&rqh=1&gir=yes&clen=2393857&dur=134.661&lmt=1744758855452408&mt=1782285909&fvip=4&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5308224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgd6SdQ3gDLuUNdOknwgzUYzrDfapI9ghKrvJoDXv8xZQCIQD1Uw33ACVjtLC54-c04KwiF0_Ssr9FWQLsrjPsUmA1eA%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRgIhAOAZex_mL1p_pDQPHZETwG81pWnS4VEv41O_YSWUkYghAiEAuyCow7d5mP3LhYVmbD-Iuaeu7Qxe7umQtw21bFb6mC4%3D",
          "available_at": 1782286439,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "webm",
          "video_ext": "none",
          "vbr": 0,
          "abr": 142.215,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "251 - audio only (medium)"
        },
        {
          "format_id": "91",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308037/ei/ZYg7aqX3NqqXsfIP-NO30Qg/ip/47.147.88.26/id/70fdde0a1a94a610/itag/91/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D823012%3Bdur%3D134.768%3Bgir%3Dyes%3Bitag%3D139%3Blmt%3D1744758845650026/sgovp/clen%3D1652845%3Bdur%3D134.634%3Bgir%3Dyes%3Bitag%3D160%3Blmt%3D1744758853194138/rqh/1/hls_chunk_host/rr2---sn-a5meknzr.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/386/met/1782286437,/mh/As/mm/31,29/mn/sn-a5meknzr,sn-a5msen7l/ms/au,rdu/mv/m/mvi/2/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWWXVCq5DpEKw48kP617dVBW8jRLLjv-3A8zB1RlpzCarXKlPRLey-0GhXMwNm88TOTCsSicAIr/spc/SQ-umoR-hJoJXTizSWuzQmw_3EQvwYyliVxMlC7y1Mija59ngO9e_EM-q974hh_BhrHfBE9G/vprv/1/ns/YVuRLcxEV7-Imu2769cUR0AW/playlist_type/CLEAN/dover/11/txp/5309224/mt/1782286149/fvip/2/keepalive/yes/fexp/51565116,51565682,51987687/n/r70ymaC8QkODvA/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRQIgKDtfR9LNHOFmitRjzK_Q9SLQSDvmPSFa3nFbDhspxn8CIQCXHvSX_PlyYf8DjTn5sxXf5i6Ya7aqKu6oB3UKILVQ8w%3D%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRgIhAJjYAl3jyoylVbVq7mhBa8Xk2D2LX3xqcK-7k1h-jmWxAiEAppgtyAJ1UG9_RmicuUIXg9zD0d43nbbzwC6Vt_M4860%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308037/ei/ZYg7aqX3NqqXsfIP-NO30Qg/ip/47.147.88.26/id/70fdde0a1a94a610/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr2---sn-a5meknzr.googlevideo.com/cps/386/met/1782286437%2C/mh/As/mm/31%2C29/mn/sn-a5meknzr%2Csn-a5msen7l/ms/au%2Crdu/mv/m/mvi/2/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWWXVCq5DpEKw48kP617dVBW8jRLLjv-3A8zB1RlpzCarXKlPRLey-0GhXMwNm88TOTCsSicAIr/spc/SQ-umoR-hJoJXTizSWuzQmw_3EQvwYyliVxMlC7y1Mija59ngO9e_EM-q974hh_BhrHfBE9G/vprv/1/go/1/ns/YVuRLcxEV7-Imu2769cUR0AW/rqh/5/mt/1782286149/fvip/2/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51987687/dover/11/n/r70ymaC8QkODvA/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRgIhAOuMe8Dlm8Sgfk649ymuHfiw89y5JzFlqfQsopMNx9biAiEA_qKmJYznQAJhcJhy07VoH1Jz4k6sE4Kg_15EfDSqLwM%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIhAN_QXY0XJPNOa-Uu4U8YO3R_xcdc-K7XTUoFAU2Zcnv6AiAaMRZ8VNj055EklztQYnVsEZRpyKtAONULfTx6HQ_8XA%3D%3D/file/index.m3u8",
          "tbr": 185.291,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 0,
          "has_drm": False,
          "width": 256,
          "height": 144,
          "vcodec": "avc1.4D400C",
          "acodec": "mp4a.40.5",
          "dynamic_range": "SDR",
          "available_at": 1782286439,
          "source_preference": -2,
          "language": "en",
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "91 - 256x144"
        },
        {
          "asr": None,
          "filesize": 1652845,
          "format_id": "160",
          "format_note": "144p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 144,
          "quality": 0.0,
          "has_drm": False,
          "tbr": 98.212,
          "filesize_approx": 1652834,
          "width": 256,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d400c",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr2---sn-a5meknzr.googlevideo.com/videoplayback?expire=1782308038&ei=Zog7ataHLdugsfIPr8XFkA8&ip=47.147.88.26&id=o-AKNIFvcG3SgOlNxz7CVhQ57Qsz1fyHRPBgdWYne_-Rl-&itag=160&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=381&met=1782286438%2C&mh=As&mm=31%2C26&mn=sn-a5meknzr%2Csn-vgqskn6y&ms=au%2Conr&mv=m&mvi=2&pl=12&rms=au%2Cau&initcwndbps=3750000&bui=ARmQxEW1Gsi3sb39UJHNcf0H4Zq8G-03EjXEnskInoyyW2K1yzd-cKsh_2UPSllc-wBVdtv6nN2Gm0L_&spc=SQ-umpTvy_oesEoe5hMTm0g4-6gnSxSxrPlXnPChMX6G&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=1652845&dur=134.634&lmt=1744758853194138&mt=1782285909&fvip=4&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5309224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgDNSVMMsBixhu0dIuoOicl1AEQlBrYIcidpM1rdtceFkCIQDm5rUdHdPyBb3aAIARTeFeLQyYjuClOsEoOCZLMCCakA%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRgIhAOAZex_mL1p_pDQPHZETwG81pWnS4VEv41O_YSWUkYghAiEAuyCow7d5mP3LhYVmbD-Iuaeu7Qxe7umQtw21bFb6mC4%3D",
          "available_at": 1782286439,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 98.212,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "160 - 256x144 (144p)"
        },
        {
          "format_id": "93",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308037/ei/ZYg7aqX3NqqXsfIP-NO30Qg/ip/47.147.88.26/id/70fdde0a1a94a610/itag/93/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2180941%3Bdur%3D134.698%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1744758845381853/sgovp/clen%3D6266578%3Bdur%3D134.634%3Bgir%3Dyes%3Bitag%3D134%3Blmt%3D1744758852676922/rqh/1/hls_chunk_host/rr2---sn-a5meknzr.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/386/met/1782286437,/mh/As/mm/31,29/mn/sn-a5meknzr,sn-a5msen7l/ms/au,rdu/mv/m/mvi/2/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWWXVCq5DpEKw48kP617dVBW8jRLLjv-3A8zB1RlpzCarXKlPRLey-0GhXMwNm88TOTCsSicAIr/spc/SQ-umoR-hJoJXTizSWuzQmw_3EQvwYyliVxMlC7y1Mija59ngO9e_EM-q974hh_BhrHfBE9G/vprv/1/ns/YVuRLcxEV7-Imu2769cUR0AW/playlist_type/CLEAN/dover/11/txp/5309224/mt/1782286149/fvip/2/keepalive/yes/fexp/51565116,51565682,51987687/n/r70ymaC8QkODvA/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRQIgZhtR44xE9mCX_rHyXuEYHXNESBCOyBBDVPbvt9YbzGwCIQDFEf-sjCLmL6yXBE8yfq11bc5madPTTKMa9NzXxKV9mQ%3D%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIgXBg8SZdq4t85yxzrOmi50mI8AWOEtArCGO59PBqTgJoCIQCVMQkg-5N-t18aJA3JNpoV9j8aYeIKOdz7dANp62MxYw%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308037/ei/ZYg7aqX3NqqXsfIP-NO30Qg/ip/47.147.88.26/id/70fdde0a1a94a610/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr2---sn-a5meknzr.googlevideo.com/cps/386/met/1782286437%2C/mh/As/mm/31%2C29/mn/sn-a5meknzr%2Csn-a5msen7l/ms/au%2Crdu/mv/m/mvi/2/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWWXVCq5DpEKw48kP617dVBW8jRLLjv-3A8zB1RlpzCarXKlPRLey-0GhXMwNm88TOTCsSicAIr/spc/SQ-umoR-hJoJXTizSWuzQmw_3EQvwYyliVxMlC7y1Mija59ngO9e_EM-q974hh_BhrHfBE9G/vprv/1/go/1/ns/YVuRLcxEV7-Imu2769cUR0AW/rqh/5/mt/1782286149/fvip/2/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51987687/dover/11/n/r70ymaC8QkODvA/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRgIhAOuMe8Dlm8Sgfk649ymuHfiw89y5JzFlqfQsopMNx9biAiEA_qKmJYznQAJhcJhy07VoH1Jz4k6sE4Kg_15EfDSqLwM%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIhAN_QXY0XJPNOa-Uu4U8YO3R_xcdc-K7XTUoFAU2Zcnv6AiAaMRZ8VNj055EklztQYnVsEZRpyKtAONULfTx6HQ_8XA%3D%3D/file/index.m3u8",
          "tbr": 709.72,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 6,
          "has_drm": False,
          "width": 640,
          "height": 360,
          "vcodec": "avc1.4D401E",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286439,
          "source_preference": -2,
          "language": "en",
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "93 - 640x360"
        },
        {
          "asr": None,
          "filesize": 6266578,
          "format_id": "134",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 372.362,
          "filesize_approx": 6266573,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d401e",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr2---sn-a5meknzr.googlevideo.com/videoplayback?expire=1782308038&ei=Zog7ataHLdugsfIPr8XFkA8&ip=47.147.88.26&id=o-AKNIFvcG3SgOlNxz7CVhQ57Qsz1fyHRPBgdWYne_-Rl-&itag=134&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=381&met=1782286438%2C&mh=As&mm=31%2C26&mn=sn-a5meknzr%2Csn-vgqskn6y&ms=au%2Conr&mv=m&mvi=2&pl=12&rms=au%2Cau&initcwndbps=3750000&bui=ARmQxEW1Gsi3sb39UJHNcf0H4Zq8G-03EjXEnskInoyyW2K1yzd-cKsh_2UPSllc-wBVdtv6nN2Gm0L_&spc=SQ-umpTvy_oesEoe5hMTm0g4-6gnSxSxrPlXnPChMX6G&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=6266578&dur=134.634&lmt=1744758852676922&mt=1782285909&fvip=4&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5309224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgSHxHkgsnFc6asIyS8SfATZ--Yqc-2pLBtU2vHjge_wgCICr-2P-um4Vi4P79NQ1n__uu9m-AjgORObolQv6iMMuW&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRgIhAOAZex_mL1p_pDQPHZETwG81pWnS4VEv41O_YSWUkYghAiEAuyCow7d5mP3LhYVmbD-Iuaeu7Qxe7umQtw21bFb6mC4%3D",
          "available_at": 1782286439,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 372.362,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "134 - 640x360 (360p)"
        },
        {
          "asr": 44100,
          "filesize": None,
          "format_id": "18",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": 2,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 501.049,
          "filesize_approx": 8436287,
          "width": 640,
          "language": "en",
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.42001E",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "url": "https://rr2---sn-a5meknzr.googlevideo.com/videoplayback?expire=1782308038&ei=Zog7ataHLdugsfIPr8XFkA8&ip=47.147.88.26&id=o-AKNIFvcG3SgOlNxz7CVhQ57Qsz1fyHRPBgdWYne_-Rl-&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=381&met=1782286438%2C&mh=As&mm=31%2C26&mn=sn-a5meknzr%2Csn-vgqskn6y&ms=au%2Conr&mv=m&mvi=2&pl=12&rms=au%2Cau&initcwndbps=3750000&bui=ARmQxEWxq1pn9uxNMAWT89i5lAWIOrQehs5csrg1qa8T6DQlqFP2-_b3XostVZmlQjVsZ2NXwljxOEw9&spc=SQ-umr7m8f8suEgmzhJRo2Alua1HV46x_PU1jHm4M1aNNjDAE5BR&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&cnr=14&ratebypass=yes&dur=134.698&lmt=1744758854399806&mt=1782285909&fvip=4&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5309224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AHEqNM4wRAIgJCPC0YdoOyyLaVn0oBqZg6FWrG-2s4dxCvd4lrHxZJkCIErMff3Qlor1Zx78GYaGtzLT9A8KRSNVoNh_c8Le85C2&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRgIhAOAZex_mL1p_pDQPHZETwG81pWnS4VEv41O_YSWUkYghAiEAuyCow7d5mP3LhYVmbD-Iuaeu7Qxe7umQtw21bFb6mC4%3D",
          "available_at": 1782286439,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "18 - 640x360 (360p)"
        },
        {
          "format_id": "95",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308037/ei/ZYg7aqX3NqqXsfIP-NO30Qg/ip/47.147.88.26/id/70fdde0a1a94a610/itag/95/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2180941%3Bdur%3D134.698%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1744758845381853/sgovp/clen%3D23515598%3Bdur%3D134.634%3Bgir%3Dyes%3Bitag%3D136%3Blmt%3D1744758854329087/rqh/1/hls_chunk_host/rr2---sn-a5meknzr.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/386/met/1782286437,/mh/As/mm/31,29/mn/sn-a5meknzr,sn-a5msen7l/ms/au,rdu/mv/m/mvi/2/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWWXVCq5DpEKw48kP617dVBW8jRLLjv-3A8zB1RlpzCarXKlPRLey-0GhXMwNm88TOTCsSicAIr/spc/SQ-umoR-hJoJXTizSWuzQmw_3EQvwYyliVxMlC7y1Mija59ngO9e_EM-q974hh_BhrHfBE9G/vprv/1/ns/YVuRLcxEV7-Imu2769cUR0AW/playlist_type/CLEAN/dover/11/txp/5309224/mt/1782286149/fvip/2/keepalive/yes/fexp/51565116,51565682,51987687/n/r70ymaC8QkODvA/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRgIhANJupRlnJ8DdtH3SllLkWGdlwEEcIGM7lkj_OFLTbjwpAiEAyd7_blQbR_tUz7FG5g14tA79atZCmuS6yOehIcPvMXA%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRAIgDJS8srAe2qzYQHU7oy2bKyDYPdgJSDosMYwsXFWwwHcCIGJz2wQMkpdcl4QgmadufFRV2UHGgBUU3gH8ME6mW4qD/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308037/ei/ZYg7aqX3NqqXsfIP-NO30Qg/ip/47.147.88.26/id/70fdde0a1a94a610/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr2---sn-a5meknzr.googlevideo.com/cps/386/met/1782286437%2C/mh/As/mm/31%2C29/mn/sn-a5meknzr%2Csn-a5msen7l/ms/au%2Crdu/mv/m/mvi/2/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWWXVCq5DpEKw48kP617dVBW8jRLLjv-3A8zB1RlpzCarXKlPRLey-0GhXMwNm88TOTCsSicAIr/spc/SQ-umoR-hJoJXTizSWuzQmw_3EQvwYyliVxMlC7y1Mija59ngO9e_EM-q974hh_BhrHfBE9G/vprv/1/go/1/ns/YVuRLcxEV7-Imu2769cUR0AW/rqh/5/mt/1782286149/fvip/2/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51987687/dover/11/n/r70ymaC8QkODvA/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRgIhAOuMe8Dlm8Sgfk649ymuHfiw89y5JzFlqfQsopMNx9biAiEA_qKmJYznQAJhcJhy07VoH1Jz4k6sE4Kg_15EfDSqLwM%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIhAN_QXY0XJPNOa-Uu4U8YO3R_xcdc-K7XTUoFAU2Zcnv6AiAaMRZ8VNj055EklztQYnVsEZRpyKtAONULfTx6HQ_8XA%3D%3D/file/index.m3u8",
          "tbr": 2209.784,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 8,
          "has_drm": False,
          "width": 1280,
          "height": 720,
          "vcodec": "avc1.64001F",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286439,
          "source_preference": -2,
          "language": "en",
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "95 - 1280x720"
        },
        {
          "asr": None,
          "filesize": 23515598,
          "format_id": "136",
          "format_note": "720p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 720,
          "quality": 8.0,
          "has_drm": False,
          "tbr": 1397.305,
          "filesize_approx": 23515595,
          "width": 1280,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.64001f",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr2---sn-a5meknzr.googlevideo.com/videoplayback?expire=1782308038&ei=Zog7ataHLdugsfIPr8XFkA8&ip=47.147.88.26&id=o-AKNIFvcG3SgOlNxz7CVhQ57Qsz1fyHRPBgdWYne_-Rl-&itag=136&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=381&met=1782286438%2C&mh=As&mm=31%2C26&mn=sn-a5meknzr%2Csn-vgqskn6y&ms=au%2Conr&mv=m&mvi=2&pl=12&rms=au%2Cau&initcwndbps=3750000&bui=ARmQxEW1Gsi3sb39UJHNcf0H4Zq8G-03EjXEnskInoyyW2K1yzd-cKsh_2UPSllc-wBVdtv6nN2Gm0L_&spc=SQ-umpTvy_oesEoe5hMTm0g4-6gnSxSxrPlXnPChMX6G&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=23515598&dur=134.634&lmt=1744758854329087&mt=1782285909&fvip=4&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5309224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgKVTEE6ZxgrjCXaFAaizYtPySb7_-mamNojBSsrTk3LwCIQDixT88oZuwvokb-FenHc8dnPgO0gKqp9opk6ge4MAyCQ%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRgIhAOAZex_mL1p_pDQPHZETwG81pWnS4VEv41O_YSWUkYghAiEAuyCow7d5mP3LhYVmbD-Iuaeu7Qxe7umQtw21bFb6mC4%3D",
          "available_at": 1782286439,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 1397.305,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "136 - 1280x720 (720p)"
        }
      ],
      "thumbnail": "https://i.ytimg.com/vi/cP3eChqUphA/maxresdefault.jpg",
      "average_rating": None,
      "age_limit": 0,
      "webpage_url": "https://www.youtube.com/watch?v=cP3eChqUphA",
      "categories": ["Gaming"],
      "tags": ["Senzawa", "sings", "gura", "cover"],
      "playable_in_embed": True,
      "media_type": "video",
      "_format_sort_fields": [
        "quality",
        "res",
        "fps",
        "hdr:12",
        "source",
        "vcodec",
        "channels",
        "acodec",
        "lang",
        "proto"
      ],
      "automatic_captions": {
        "ab": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ab",
            "name": "Abkhazian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ab",
            "name": "Abkhazian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ab",
            "name": "Abkhazian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ab",
            "name": "Abkhazian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ab",
            "name": "Abkhazian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ab",
            "name": "Abkhazian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ab",
            "name": "Abkhazian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "aa": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=aa",
            "name": "Afar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=aa",
            "name": "Afar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=aa",
            "name": "Afar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=aa",
            "name": "Afar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=aa",
            "name": "Afar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=aa",
            "name": "Afar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=aa",
            "name": "Afar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "af": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=af",
            "name": "Afrikaans",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=af",
            "name": "Afrikaans",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=af",
            "name": "Afrikaans",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=af",
            "name": "Afrikaans",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=af",
            "name": "Afrikaans",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=af",
            "name": "Afrikaans",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=af",
            "name": "Afrikaans",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ak": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ak",
            "name": "Akan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ak",
            "name": "Akan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ak",
            "name": "Akan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ak",
            "name": "Akan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ak",
            "name": "Akan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ak",
            "name": "Akan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ak",
            "name": "Akan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "sq": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=sq",
            "name": "Albanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=sq",
            "name": "Albanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=sq",
            "name": "Albanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=sq",
            "name": "Albanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=sq",
            "name": "Albanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=sq",
            "name": "Albanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=sq",
            "name": "Albanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "am": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=am",
            "name": "Amharic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=am",
            "name": "Amharic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=am",
            "name": "Amharic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=am",
            "name": "Amharic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=am",
            "name": "Amharic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=am",
            "name": "Amharic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=am",
            "name": "Amharic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ar": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ar",
            "name": "Arabic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ar",
            "name": "Arabic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ar",
            "name": "Arabic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ar",
            "name": "Arabic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ar",
            "name": "Arabic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ar",
            "name": "Arabic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ar",
            "name": "Arabic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "hy": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=hy",
            "name": "Armenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=hy",
            "name": "Armenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=hy",
            "name": "Armenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=hy",
            "name": "Armenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=hy",
            "name": "Armenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=hy",
            "name": "Armenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=hy",
            "name": "Armenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "as": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=as",
            "name": "Assamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=as",
            "name": "Assamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=as",
            "name": "Assamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=as",
            "name": "Assamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=as",
            "name": "Assamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=as",
            "name": "Assamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=as",
            "name": "Assamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ay": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ay",
            "name": "Aymara",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ay",
            "name": "Aymara",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ay",
            "name": "Aymara",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ay",
            "name": "Aymara",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ay",
            "name": "Aymara",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ay",
            "name": "Aymara",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ay",
            "name": "Aymara",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "az": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=az",
            "name": "Azerbaijani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=az",
            "name": "Azerbaijani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=az",
            "name": "Azerbaijani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=az",
            "name": "Azerbaijani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=az",
            "name": "Azerbaijani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=az",
            "name": "Azerbaijani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=az",
            "name": "Azerbaijani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "bn": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=bn",
            "name": "Bangla",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=bn",
            "name": "Bangla",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=bn",
            "name": "Bangla",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=bn",
            "name": "Bangla",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=bn",
            "name": "Bangla",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=bn",
            "name": "Bangla",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=bn",
            "name": "Bangla",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ba": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ba",
            "name": "Bashkir",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ba",
            "name": "Bashkir",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ba",
            "name": "Bashkir",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ba",
            "name": "Bashkir",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ba",
            "name": "Bashkir",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ba",
            "name": "Bashkir",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ba",
            "name": "Bashkir",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "eu": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=eu",
            "name": "Basque",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=eu",
            "name": "Basque",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=eu",
            "name": "Basque",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=eu",
            "name": "Basque",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=eu",
            "name": "Basque",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=eu",
            "name": "Basque",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=eu",
            "name": "Basque",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "be": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=be",
            "name": "Belarusian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=be",
            "name": "Belarusian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=be",
            "name": "Belarusian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=be",
            "name": "Belarusian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=be",
            "name": "Belarusian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=be",
            "name": "Belarusian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=be",
            "name": "Belarusian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "bho": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=bho",
            "name": "Bhojpuri",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=bho",
            "name": "Bhojpuri",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=bho",
            "name": "Bhojpuri",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=bho",
            "name": "Bhojpuri",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=bho",
            "name": "Bhojpuri",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=bho",
            "name": "Bhojpuri",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=bho",
            "name": "Bhojpuri",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "bs": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=bs",
            "name": "Bosnian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=bs",
            "name": "Bosnian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=bs",
            "name": "Bosnian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=bs",
            "name": "Bosnian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=bs",
            "name": "Bosnian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=bs",
            "name": "Bosnian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=bs",
            "name": "Bosnian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "br": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=br",
            "name": "Breton",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=br",
            "name": "Breton",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=br",
            "name": "Breton",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=br",
            "name": "Breton",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=br",
            "name": "Breton",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=br",
            "name": "Breton",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=br",
            "name": "Breton",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "bg": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=bg",
            "name": "Bulgarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=bg",
            "name": "Bulgarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=bg",
            "name": "Bulgarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=bg",
            "name": "Bulgarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=bg",
            "name": "Bulgarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=bg",
            "name": "Bulgarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=bg",
            "name": "Bulgarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "my": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=my",
            "name": "Burmese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=my",
            "name": "Burmese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=my",
            "name": "Burmese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=my",
            "name": "Burmese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=my",
            "name": "Burmese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=my",
            "name": "Burmese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=my",
            "name": "Burmese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ca": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ca",
            "name": "Catalan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ca",
            "name": "Catalan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ca",
            "name": "Catalan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ca",
            "name": "Catalan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ca",
            "name": "Catalan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ca",
            "name": "Catalan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ca",
            "name": "Catalan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ceb": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ceb",
            "name": "Cebuano",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ceb",
            "name": "Cebuano",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ceb",
            "name": "Cebuano",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ceb",
            "name": "Cebuano",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ceb",
            "name": "Cebuano",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ceb",
            "name": "Cebuano",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ceb",
            "name": "Cebuano",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "zh-Hans": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=zh-Hans",
            "name": "Chinese (Simplified)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=zh-Hans",
            "name": "Chinese (Simplified)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=zh-Hans",
            "name": "Chinese (Simplified)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=zh-Hans",
            "name": "Chinese (Simplified)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=zh-Hans",
            "name": "Chinese (Simplified)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=zh-Hans",
            "name": "Chinese (Simplified)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=zh-Hans",
            "name": "Chinese (Simplified)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "zh-Hant": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=zh-Hant",
            "name": "Chinese (Traditional)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=zh-Hant",
            "name": "Chinese (Traditional)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=zh-Hant",
            "name": "Chinese (Traditional)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=zh-Hant",
            "name": "Chinese (Traditional)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=zh-Hant",
            "name": "Chinese (Traditional)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=zh-Hant",
            "name": "Chinese (Traditional)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=zh-Hant",
            "name": "Chinese (Traditional)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "co": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=co",
            "name": "Corsican",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=co",
            "name": "Corsican",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=co",
            "name": "Corsican",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=co",
            "name": "Corsican",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=co",
            "name": "Corsican",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=co",
            "name": "Corsican",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=co",
            "name": "Corsican",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "hr": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=hr",
            "name": "Croatian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=hr",
            "name": "Croatian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=hr",
            "name": "Croatian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=hr",
            "name": "Croatian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=hr",
            "name": "Croatian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=hr",
            "name": "Croatian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=hr",
            "name": "Croatian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "cs": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=cs",
            "name": "Czech",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=cs",
            "name": "Czech",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=cs",
            "name": "Czech",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=cs",
            "name": "Czech",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=cs",
            "name": "Czech",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=cs",
            "name": "Czech",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=cs",
            "name": "Czech",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "da": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=da",
            "name": "Danish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=da",
            "name": "Danish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=da",
            "name": "Danish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=da",
            "name": "Danish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=da",
            "name": "Danish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=da",
            "name": "Danish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=da",
            "name": "Danish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "dv": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=dv",
            "name": "Divehi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=dv",
            "name": "Divehi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=dv",
            "name": "Divehi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=dv",
            "name": "Divehi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=dv",
            "name": "Divehi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=dv",
            "name": "Divehi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=dv",
            "name": "Divehi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "nl": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=nl",
            "name": "Dutch",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=nl",
            "name": "Dutch",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=nl",
            "name": "Dutch",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=nl",
            "name": "Dutch",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=nl",
            "name": "Dutch",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=nl",
            "name": "Dutch",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=nl",
            "name": "Dutch",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "dz": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=dz",
            "name": "Dzongkha",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=dz",
            "name": "Dzongkha",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=dz",
            "name": "Dzongkha",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=dz",
            "name": "Dzongkha",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=dz",
            "name": "Dzongkha",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=dz",
            "name": "Dzongkha",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=dz",
            "name": "Dzongkha",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "en-orig": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3",
            "name": "English (Original)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1",
            "name": "English (Original)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2",
            "name": "English (Original)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3",
            "name": "English (Original)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml",
            "name": "English (Original)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt",
            "name": "English (Original)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt",
            "name": "English (Original)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "en": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "eo": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=eo",
            "name": "Esperanto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=eo",
            "name": "Esperanto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=eo",
            "name": "Esperanto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=eo",
            "name": "Esperanto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=eo",
            "name": "Esperanto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=eo",
            "name": "Esperanto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=eo",
            "name": "Esperanto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "et": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=et",
            "name": "Estonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=et",
            "name": "Estonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=et",
            "name": "Estonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=et",
            "name": "Estonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=et",
            "name": "Estonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=et",
            "name": "Estonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=et",
            "name": "Estonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ee": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ee",
            "name": "Ewe",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ee",
            "name": "Ewe",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ee",
            "name": "Ewe",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ee",
            "name": "Ewe",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ee",
            "name": "Ewe",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ee",
            "name": "Ewe",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ee",
            "name": "Ewe",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "fo": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=fo",
            "name": "Faroese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=fo",
            "name": "Faroese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=fo",
            "name": "Faroese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=fo",
            "name": "Faroese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=fo",
            "name": "Faroese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=fo",
            "name": "Faroese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=fo",
            "name": "Faroese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "fj": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=fj",
            "name": "Fijian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=fj",
            "name": "Fijian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=fj",
            "name": "Fijian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=fj",
            "name": "Fijian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=fj",
            "name": "Fijian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=fj",
            "name": "Fijian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=fj",
            "name": "Fijian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "fil": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=fil",
            "name": "Filipino",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=fil",
            "name": "Filipino",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=fil",
            "name": "Filipino",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=fil",
            "name": "Filipino",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=fil",
            "name": "Filipino",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=fil",
            "name": "Filipino",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=fil",
            "name": "Filipino",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "fi": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=fi",
            "name": "Finnish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=fi",
            "name": "Finnish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=fi",
            "name": "Finnish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=fi",
            "name": "Finnish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=fi",
            "name": "Finnish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=fi",
            "name": "Finnish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=fi",
            "name": "Finnish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "fr": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=fr",
            "name": "French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=fr",
            "name": "French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=fr",
            "name": "French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=fr",
            "name": "French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=fr",
            "name": "French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=fr",
            "name": "French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=fr",
            "name": "French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "gaa": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=gaa",
            "name": "Ga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=gaa",
            "name": "Ga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=gaa",
            "name": "Ga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=gaa",
            "name": "Ga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=gaa",
            "name": "Ga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=gaa",
            "name": "Ga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=gaa",
            "name": "Ga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "gl": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=gl",
            "name": "Galician",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=gl",
            "name": "Galician",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=gl",
            "name": "Galician",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=gl",
            "name": "Galician",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=gl",
            "name": "Galician",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=gl",
            "name": "Galician",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=gl",
            "name": "Galician",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "lg": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=lg",
            "name": "Ganda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=lg",
            "name": "Ganda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=lg",
            "name": "Ganda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=lg",
            "name": "Ganda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=lg",
            "name": "Ganda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=lg",
            "name": "Ganda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=lg",
            "name": "Ganda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ka": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ka",
            "name": "Georgian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ka",
            "name": "Georgian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ka",
            "name": "Georgian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ka",
            "name": "Georgian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ka",
            "name": "Georgian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ka",
            "name": "Georgian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ka",
            "name": "Georgian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "de": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=de",
            "name": "German",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=de",
            "name": "German",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=de",
            "name": "German",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=de",
            "name": "German",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=de",
            "name": "German",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=de",
            "name": "German",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=de",
            "name": "German",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "el": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=el",
            "name": "Greek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=el",
            "name": "Greek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=el",
            "name": "Greek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=el",
            "name": "Greek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=el",
            "name": "Greek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=el",
            "name": "Greek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=el",
            "name": "Greek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "gn": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=gn",
            "name": "Guarani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=gn",
            "name": "Guarani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=gn",
            "name": "Guarani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=gn",
            "name": "Guarani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=gn",
            "name": "Guarani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=gn",
            "name": "Guarani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=gn",
            "name": "Guarani",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "gu": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=gu",
            "name": "Gujarati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=gu",
            "name": "Gujarati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=gu",
            "name": "Gujarati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=gu",
            "name": "Gujarati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=gu",
            "name": "Gujarati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=gu",
            "name": "Gujarati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=gu",
            "name": "Gujarati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ht": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ht",
            "name": "Haitian Creole",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ht",
            "name": "Haitian Creole",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ht",
            "name": "Haitian Creole",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ht",
            "name": "Haitian Creole",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ht",
            "name": "Haitian Creole",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ht",
            "name": "Haitian Creole",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ht",
            "name": "Haitian Creole",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ha": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ha",
            "name": "Hausa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ha",
            "name": "Hausa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ha",
            "name": "Hausa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ha",
            "name": "Hausa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ha",
            "name": "Hausa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ha",
            "name": "Hausa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ha",
            "name": "Hausa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "haw": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=haw",
            "name": "Hawaiian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=haw",
            "name": "Hawaiian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=haw",
            "name": "Hawaiian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=haw",
            "name": "Hawaiian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=haw",
            "name": "Hawaiian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=haw",
            "name": "Hawaiian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=haw",
            "name": "Hawaiian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "iw": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=iw",
            "name": "Hebrew",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=iw",
            "name": "Hebrew",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=iw",
            "name": "Hebrew",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=iw",
            "name": "Hebrew",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=iw",
            "name": "Hebrew",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=iw",
            "name": "Hebrew",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=iw",
            "name": "Hebrew",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "hi": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=hi",
            "name": "Hindi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=hi",
            "name": "Hindi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=hi",
            "name": "Hindi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=hi",
            "name": "Hindi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=hi",
            "name": "Hindi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=hi",
            "name": "Hindi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=hi",
            "name": "Hindi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "hmn": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=hmn",
            "name": "Hmong",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=hmn",
            "name": "Hmong",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=hmn",
            "name": "Hmong",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=hmn",
            "name": "Hmong",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=hmn",
            "name": "Hmong",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=hmn",
            "name": "Hmong",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=hmn",
            "name": "Hmong",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "hu": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=hu",
            "name": "Hungarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=hu",
            "name": "Hungarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=hu",
            "name": "Hungarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=hu",
            "name": "Hungarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=hu",
            "name": "Hungarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=hu",
            "name": "Hungarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=hu",
            "name": "Hungarian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "is": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=is",
            "name": "Icelandic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=is",
            "name": "Icelandic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=is",
            "name": "Icelandic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=is",
            "name": "Icelandic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=is",
            "name": "Icelandic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=is",
            "name": "Icelandic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=is",
            "name": "Icelandic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ig": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ig",
            "name": "Igbo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ig",
            "name": "Igbo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ig",
            "name": "Igbo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ig",
            "name": "Igbo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ig",
            "name": "Igbo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ig",
            "name": "Igbo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ig",
            "name": "Igbo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "id": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=id",
            "name": "Indonesian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=id",
            "name": "Indonesian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=id",
            "name": "Indonesian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=id",
            "name": "Indonesian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=id",
            "name": "Indonesian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=id",
            "name": "Indonesian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=id",
            "name": "Indonesian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "iu": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=iu",
            "name": "Inuktitut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=iu",
            "name": "Inuktitut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=iu",
            "name": "Inuktitut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=iu",
            "name": "Inuktitut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=iu",
            "name": "Inuktitut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=iu",
            "name": "Inuktitut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=iu",
            "name": "Inuktitut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ga": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ga",
            "name": "Irish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ga",
            "name": "Irish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ga",
            "name": "Irish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ga",
            "name": "Irish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ga",
            "name": "Irish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ga",
            "name": "Irish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ga",
            "name": "Irish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "it": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=it",
            "name": "Italian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=it",
            "name": "Italian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=it",
            "name": "Italian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=it",
            "name": "Italian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=it",
            "name": "Italian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=it",
            "name": "Italian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=it",
            "name": "Italian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ja": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ja",
            "name": "Japanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ja",
            "name": "Japanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ja",
            "name": "Japanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ja",
            "name": "Japanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ja",
            "name": "Japanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ja",
            "name": "Japanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ja",
            "name": "Japanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "jv": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=jv",
            "name": "Javanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=jv",
            "name": "Javanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=jv",
            "name": "Javanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=jv",
            "name": "Javanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=jv",
            "name": "Javanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=jv",
            "name": "Javanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=jv",
            "name": "Javanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "kl": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=kl",
            "name": "Kalaallisut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=kl",
            "name": "Kalaallisut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=kl",
            "name": "Kalaallisut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=kl",
            "name": "Kalaallisut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=kl",
            "name": "Kalaallisut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=kl",
            "name": "Kalaallisut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=kl",
            "name": "Kalaallisut",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "kn": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=kn",
            "name": "Kannada",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=kn",
            "name": "Kannada",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=kn",
            "name": "Kannada",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=kn",
            "name": "Kannada",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=kn",
            "name": "Kannada",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=kn",
            "name": "Kannada",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=kn",
            "name": "Kannada",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "kk": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=kk",
            "name": "Kazakh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=kk",
            "name": "Kazakh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=kk",
            "name": "Kazakh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=kk",
            "name": "Kazakh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=kk",
            "name": "Kazakh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=kk",
            "name": "Kazakh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=kk",
            "name": "Kazakh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "kha": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=kha",
            "name": "Khasi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=kha",
            "name": "Khasi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=kha",
            "name": "Khasi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=kha",
            "name": "Khasi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=kha",
            "name": "Khasi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=kha",
            "name": "Khasi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=kha",
            "name": "Khasi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "km": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=km",
            "name": "Khmer",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=km",
            "name": "Khmer",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=km",
            "name": "Khmer",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=km",
            "name": "Khmer",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=km",
            "name": "Khmer",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=km",
            "name": "Khmer",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=km",
            "name": "Khmer",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "rw": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=rw",
            "name": "Kinyarwanda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=rw",
            "name": "Kinyarwanda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=rw",
            "name": "Kinyarwanda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=rw",
            "name": "Kinyarwanda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=rw",
            "name": "Kinyarwanda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=rw",
            "name": "Kinyarwanda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=rw",
            "name": "Kinyarwanda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ko": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ko",
            "name": "Korean",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ko",
            "name": "Korean",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ko",
            "name": "Korean",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ko",
            "name": "Korean",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ko",
            "name": "Korean",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ko",
            "name": "Korean",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ko",
            "name": "Korean",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "kri": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=kri",
            "name": "Krio",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=kri",
            "name": "Krio",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=kri",
            "name": "Krio",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=kri",
            "name": "Krio",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=kri",
            "name": "Krio",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=kri",
            "name": "Krio",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=kri",
            "name": "Krio",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ku": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ku",
            "name": "Kurdish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ku",
            "name": "Kurdish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ku",
            "name": "Kurdish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ku",
            "name": "Kurdish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ku",
            "name": "Kurdish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ku",
            "name": "Kurdish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ku",
            "name": "Kurdish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ky": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ky",
            "name": "Kyrgyz",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ky",
            "name": "Kyrgyz",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ky",
            "name": "Kyrgyz",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ky",
            "name": "Kyrgyz",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ky",
            "name": "Kyrgyz",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ky",
            "name": "Kyrgyz",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ky",
            "name": "Kyrgyz",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "lo": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=lo",
            "name": "Lao",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=lo",
            "name": "Lao",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=lo",
            "name": "Lao",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=lo",
            "name": "Lao",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=lo",
            "name": "Lao",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=lo",
            "name": "Lao",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=lo",
            "name": "Lao",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "la": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=la",
            "name": "Latin",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=la",
            "name": "Latin",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=la",
            "name": "Latin",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=la",
            "name": "Latin",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=la",
            "name": "Latin",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=la",
            "name": "Latin",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=la",
            "name": "Latin",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "lv": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=lv",
            "name": "Latvian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=lv",
            "name": "Latvian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=lv",
            "name": "Latvian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=lv",
            "name": "Latvian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=lv",
            "name": "Latvian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=lv",
            "name": "Latvian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=lv",
            "name": "Latvian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ln": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ln",
            "name": "Lingala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ln",
            "name": "Lingala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ln",
            "name": "Lingala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ln",
            "name": "Lingala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ln",
            "name": "Lingala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ln",
            "name": "Lingala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ln",
            "name": "Lingala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "lt": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=lt",
            "name": "Lithuanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=lt",
            "name": "Lithuanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=lt",
            "name": "Lithuanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=lt",
            "name": "Lithuanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=lt",
            "name": "Lithuanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=lt",
            "name": "Lithuanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=lt",
            "name": "Lithuanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "lua": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=lua",
            "name": "Luba-Lulua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=lua",
            "name": "Luba-Lulua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=lua",
            "name": "Luba-Lulua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=lua",
            "name": "Luba-Lulua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=lua",
            "name": "Luba-Lulua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=lua",
            "name": "Luba-Lulua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=lua",
            "name": "Luba-Lulua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "luo": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=luo",
            "name": "Luo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=luo",
            "name": "Luo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=luo",
            "name": "Luo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=luo",
            "name": "Luo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=luo",
            "name": "Luo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=luo",
            "name": "Luo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=luo",
            "name": "Luo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "lb": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=lb",
            "name": "Luxembourgish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=lb",
            "name": "Luxembourgish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=lb",
            "name": "Luxembourgish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=lb",
            "name": "Luxembourgish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=lb",
            "name": "Luxembourgish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=lb",
            "name": "Luxembourgish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=lb",
            "name": "Luxembourgish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "mk": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=mk",
            "name": "Macedonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=mk",
            "name": "Macedonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=mk",
            "name": "Macedonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=mk",
            "name": "Macedonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=mk",
            "name": "Macedonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=mk",
            "name": "Macedonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=mk",
            "name": "Macedonian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "mg": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=mg",
            "name": "Malagasy",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=mg",
            "name": "Malagasy",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=mg",
            "name": "Malagasy",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=mg",
            "name": "Malagasy",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=mg",
            "name": "Malagasy",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=mg",
            "name": "Malagasy",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=mg",
            "name": "Malagasy",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ms": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ms",
            "name": "Malay",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ms",
            "name": "Malay",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ms",
            "name": "Malay",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ms",
            "name": "Malay",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ms",
            "name": "Malay",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ms",
            "name": "Malay",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ms",
            "name": "Malay",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ml": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ml",
            "name": "Malayalam",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ml",
            "name": "Malayalam",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ml",
            "name": "Malayalam",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ml",
            "name": "Malayalam",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ml",
            "name": "Malayalam",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ml",
            "name": "Malayalam",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ml",
            "name": "Malayalam",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "mt": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=mt",
            "name": "Maltese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=mt",
            "name": "Maltese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=mt",
            "name": "Maltese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=mt",
            "name": "Maltese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=mt",
            "name": "Maltese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=mt",
            "name": "Maltese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=mt",
            "name": "Maltese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "gv": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=gv",
            "name": "Manx",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=gv",
            "name": "Manx",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=gv",
            "name": "Manx",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=gv",
            "name": "Manx",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=gv",
            "name": "Manx",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=gv",
            "name": "Manx",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=gv",
            "name": "Manx",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "mi": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=mi",
            "name": "M\u0101ori",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=mi",
            "name": "M\u0101ori",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=mi",
            "name": "M\u0101ori",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=mi",
            "name": "M\u0101ori",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=mi",
            "name": "M\u0101ori",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=mi",
            "name": "M\u0101ori",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=mi",
            "name": "M\u0101ori",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "mr": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=mr",
            "name": "Marathi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=mr",
            "name": "Marathi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=mr",
            "name": "Marathi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=mr",
            "name": "Marathi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=mr",
            "name": "Marathi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=mr",
            "name": "Marathi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=mr",
            "name": "Marathi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "mn": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=mn",
            "name": "Mongolian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=mn",
            "name": "Mongolian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=mn",
            "name": "Mongolian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=mn",
            "name": "Mongolian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=mn",
            "name": "Mongolian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=mn",
            "name": "Mongolian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=mn",
            "name": "Mongolian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "mfe": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=mfe",
            "name": "Morisyen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=mfe",
            "name": "Morisyen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=mfe",
            "name": "Morisyen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=mfe",
            "name": "Morisyen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=mfe",
            "name": "Morisyen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=mfe",
            "name": "Morisyen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=mfe",
            "name": "Morisyen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ne": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ne",
            "name": "Nepali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ne",
            "name": "Nepali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ne",
            "name": "Nepali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ne",
            "name": "Nepali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ne",
            "name": "Nepali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ne",
            "name": "Nepali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ne",
            "name": "Nepali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "new": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=new",
            "name": "Newari",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=new",
            "name": "Newari",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=new",
            "name": "Newari",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=new",
            "name": "Newari",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=new",
            "name": "Newari",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=new",
            "name": "Newari",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=new",
            "name": "Newari",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "nso": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=nso",
            "name": "Northern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=nso",
            "name": "Northern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=nso",
            "name": "Northern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=nso",
            "name": "Northern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=nso",
            "name": "Northern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=nso",
            "name": "Northern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=nso",
            "name": "Northern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "no": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=no",
            "name": "Norwegian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=no",
            "name": "Norwegian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=no",
            "name": "Norwegian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=no",
            "name": "Norwegian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=no",
            "name": "Norwegian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=no",
            "name": "Norwegian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=no",
            "name": "Norwegian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ny": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ny",
            "name": "Nyanja",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ny",
            "name": "Nyanja",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ny",
            "name": "Nyanja",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ny",
            "name": "Nyanja",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ny",
            "name": "Nyanja",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ny",
            "name": "Nyanja",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ny",
            "name": "Nyanja",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "oc": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=oc",
            "name": "Occitan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=oc",
            "name": "Occitan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=oc",
            "name": "Occitan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=oc",
            "name": "Occitan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=oc",
            "name": "Occitan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=oc",
            "name": "Occitan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=oc",
            "name": "Occitan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "or": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=or",
            "name": "Odia",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=or",
            "name": "Odia",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=or",
            "name": "Odia",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=or",
            "name": "Odia",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=or",
            "name": "Odia",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=or",
            "name": "Odia",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=or",
            "name": "Odia",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "om": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=om",
            "name": "Oromo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=om",
            "name": "Oromo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=om",
            "name": "Oromo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=om",
            "name": "Oromo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=om",
            "name": "Oromo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=om",
            "name": "Oromo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=om",
            "name": "Oromo",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "os": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=os",
            "name": "Ossetic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=os",
            "name": "Ossetic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=os",
            "name": "Ossetic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=os",
            "name": "Ossetic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=os",
            "name": "Ossetic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=os",
            "name": "Ossetic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=os",
            "name": "Ossetic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "pam": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=pam",
            "name": "Pampanga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=pam",
            "name": "Pampanga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=pam",
            "name": "Pampanga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=pam",
            "name": "Pampanga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=pam",
            "name": "Pampanga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=pam",
            "name": "Pampanga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=pam",
            "name": "Pampanga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ps": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ps",
            "name": "Pashto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ps",
            "name": "Pashto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ps",
            "name": "Pashto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ps",
            "name": "Pashto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ps",
            "name": "Pashto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ps",
            "name": "Pashto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ps",
            "name": "Pashto",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "fa": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=fa",
            "name": "Persian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=fa",
            "name": "Persian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=fa",
            "name": "Persian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=fa",
            "name": "Persian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=fa",
            "name": "Persian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=fa",
            "name": "Persian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=fa",
            "name": "Persian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "pl": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=pl",
            "name": "Polish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=pl",
            "name": "Polish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=pl",
            "name": "Polish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=pl",
            "name": "Polish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=pl",
            "name": "Polish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=pl",
            "name": "Polish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=pl",
            "name": "Polish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "pt": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=pt",
            "name": "Portuguese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=pt",
            "name": "Portuguese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=pt",
            "name": "Portuguese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=pt",
            "name": "Portuguese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=pt",
            "name": "Portuguese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=pt",
            "name": "Portuguese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=pt",
            "name": "Portuguese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "pt-PT": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=pt-PT",
            "name": "Portuguese (Portugal)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=pt-PT",
            "name": "Portuguese (Portugal)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=pt-PT",
            "name": "Portuguese (Portugal)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=pt-PT",
            "name": "Portuguese (Portugal)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=pt-PT",
            "name": "Portuguese (Portugal)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=pt-PT",
            "name": "Portuguese (Portugal)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=pt-PT",
            "name": "Portuguese (Portugal)",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "pa": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=pa",
            "name": "Punjabi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=pa",
            "name": "Punjabi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=pa",
            "name": "Punjabi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=pa",
            "name": "Punjabi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=pa",
            "name": "Punjabi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=pa",
            "name": "Punjabi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=pa",
            "name": "Punjabi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "qu": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=qu",
            "name": "Quechua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=qu",
            "name": "Quechua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=qu",
            "name": "Quechua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=qu",
            "name": "Quechua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=qu",
            "name": "Quechua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=qu",
            "name": "Quechua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=qu",
            "name": "Quechua",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ro": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ro",
            "name": "Romanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ro",
            "name": "Romanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ro",
            "name": "Romanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ro",
            "name": "Romanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ro",
            "name": "Romanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ro",
            "name": "Romanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ro",
            "name": "Romanian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "rn": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=rn",
            "name": "Rundi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=rn",
            "name": "Rundi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=rn",
            "name": "Rundi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=rn",
            "name": "Rundi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=rn",
            "name": "Rundi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=rn",
            "name": "Rundi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=rn",
            "name": "Rundi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ru": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ru",
            "name": "Russian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ru",
            "name": "Russian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ru",
            "name": "Russian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ru",
            "name": "Russian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ru",
            "name": "Russian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ru",
            "name": "Russian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ru",
            "name": "Russian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "sm": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=sm",
            "name": "Samoan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=sm",
            "name": "Samoan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=sm",
            "name": "Samoan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=sm",
            "name": "Samoan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=sm",
            "name": "Samoan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=sm",
            "name": "Samoan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=sm",
            "name": "Samoan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "sg": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=sg",
            "name": "Sango",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=sg",
            "name": "Sango",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=sg",
            "name": "Sango",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=sg",
            "name": "Sango",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=sg",
            "name": "Sango",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=sg",
            "name": "Sango",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=sg",
            "name": "Sango",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "sa": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=sa",
            "name": "Sanskrit",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=sa",
            "name": "Sanskrit",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=sa",
            "name": "Sanskrit",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=sa",
            "name": "Sanskrit",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=sa",
            "name": "Sanskrit",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=sa",
            "name": "Sanskrit",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=sa",
            "name": "Sanskrit",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "gd": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=gd",
            "name": "Scottish Gaelic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=gd",
            "name": "Scottish Gaelic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=gd",
            "name": "Scottish Gaelic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=gd",
            "name": "Scottish Gaelic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=gd",
            "name": "Scottish Gaelic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=gd",
            "name": "Scottish Gaelic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=gd",
            "name": "Scottish Gaelic",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "sr": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=sr",
            "name": "Serbian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=sr",
            "name": "Serbian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=sr",
            "name": "Serbian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=sr",
            "name": "Serbian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=sr",
            "name": "Serbian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=sr",
            "name": "Serbian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=sr",
            "name": "Serbian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "crs": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=crs",
            "name": "Seselwa Creole French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=crs",
            "name": "Seselwa Creole French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=crs",
            "name": "Seselwa Creole French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=crs",
            "name": "Seselwa Creole French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=crs",
            "name": "Seselwa Creole French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=crs",
            "name": "Seselwa Creole French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=crs",
            "name": "Seselwa Creole French",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "sn": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=sn",
            "name": "Shona",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=sn",
            "name": "Shona",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=sn",
            "name": "Shona",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=sn",
            "name": "Shona",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=sn",
            "name": "Shona",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=sn",
            "name": "Shona",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=sn",
            "name": "Shona",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "sd": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=sd",
            "name": "Sindhi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=sd",
            "name": "Sindhi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=sd",
            "name": "Sindhi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=sd",
            "name": "Sindhi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=sd",
            "name": "Sindhi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=sd",
            "name": "Sindhi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=sd",
            "name": "Sindhi",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "si": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=si",
            "name": "Sinhala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=si",
            "name": "Sinhala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=si",
            "name": "Sinhala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=si",
            "name": "Sinhala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=si",
            "name": "Sinhala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=si",
            "name": "Sinhala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=si",
            "name": "Sinhala",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "sk": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=sk",
            "name": "Slovak",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=sk",
            "name": "Slovak",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=sk",
            "name": "Slovak",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=sk",
            "name": "Slovak",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=sk",
            "name": "Slovak",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=sk",
            "name": "Slovak",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=sk",
            "name": "Slovak",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "sl": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=sl",
            "name": "Slovenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=sl",
            "name": "Slovenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=sl",
            "name": "Slovenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=sl",
            "name": "Slovenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=sl",
            "name": "Slovenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=sl",
            "name": "Slovenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=sl",
            "name": "Slovenian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "so": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=so",
            "name": "Somali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=so",
            "name": "Somali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=so",
            "name": "Somali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=so",
            "name": "Somali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=so",
            "name": "Somali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=so",
            "name": "Somali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=so",
            "name": "Somali",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "st": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=st",
            "name": "Southern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=st",
            "name": "Southern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=st",
            "name": "Southern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=st",
            "name": "Southern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=st",
            "name": "Southern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=st",
            "name": "Southern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=st",
            "name": "Southern Sotho",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "es": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=es",
            "name": "Spanish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=es",
            "name": "Spanish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=es",
            "name": "Spanish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=es",
            "name": "Spanish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=es",
            "name": "Spanish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=es",
            "name": "Spanish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=es",
            "name": "Spanish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "su": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=su",
            "name": "Sundanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=su",
            "name": "Sundanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=su",
            "name": "Sundanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=su",
            "name": "Sundanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=su",
            "name": "Sundanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=su",
            "name": "Sundanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=su",
            "name": "Sundanese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "sw": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=sw",
            "name": "Swahili",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=sw",
            "name": "Swahili",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=sw",
            "name": "Swahili",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=sw",
            "name": "Swahili",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=sw",
            "name": "Swahili",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=sw",
            "name": "Swahili",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=sw",
            "name": "Swahili",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ss": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ss",
            "name": "Swati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ss",
            "name": "Swati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ss",
            "name": "Swati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ss",
            "name": "Swati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ss",
            "name": "Swati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ss",
            "name": "Swati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ss",
            "name": "Swati",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "sv": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=sv",
            "name": "Swedish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=sv",
            "name": "Swedish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=sv",
            "name": "Swedish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=sv",
            "name": "Swedish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=sv",
            "name": "Swedish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=sv",
            "name": "Swedish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=sv",
            "name": "Swedish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "tg": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=tg",
            "name": "Tajik",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=tg",
            "name": "Tajik",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=tg",
            "name": "Tajik",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=tg",
            "name": "Tajik",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=tg",
            "name": "Tajik",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=tg",
            "name": "Tajik",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=tg",
            "name": "Tajik",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ta": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ta",
            "name": "Tamil",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ta",
            "name": "Tamil",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ta",
            "name": "Tamil",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ta",
            "name": "Tamil",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ta",
            "name": "Tamil",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ta",
            "name": "Tamil",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ta",
            "name": "Tamil",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "tt": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=tt",
            "name": "Tatar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=tt",
            "name": "Tatar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=tt",
            "name": "Tatar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=tt",
            "name": "Tatar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=tt",
            "name": "Tatar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=tt",
            "name": "Tatar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=tt",
            "name": "Tatar",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "te": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=te",
            "name": "Telugu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=te",
            "name": "Telugu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=te",
            "name": "Telugu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=te",
            "name": "Telugu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=te",
            "name": "Telugu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=te",
            "name": "Telugu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=te",
            "name": "Telugu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "th": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=th",
            "name": "Thai",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=th",
            "name": "Thai",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=th",
            "name": "Thai",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=th",
            "name": "Thai",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=th",
            "name": "Thai",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=th",
            "name": "Thai",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=th",
            "name": "Thai",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "bo": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=bo",
            "name": "Tibetan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=bo",
            "name": "Tibetan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=bo",
            "name": "Tibetan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=bo",
            "name": "Tibetan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=bo",
            "name": "Tibetan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=bo",
            "name": "Tibetan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=bo",
            "name": "Tibetan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ti": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ti",
            "name": "Tigrinya",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ti",
            "name": "Tigrinya",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ti",
            "name": "Tigrinya",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ti",
            "name": "Tigrinya",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ti",
            "name": "Tigrinya",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ti",
            "name": "Tigrinya",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ti",
            "name": "Tigrinya",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "to": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=to",
            "name": "Tongan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=to",
            "name": "Tongan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=to",
            "name": "Tongan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=to",
            "name": "Tongan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=to",
            "name": "Tongan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=to",
            "name": "Tongan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=to",
            "name": "Tongan",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ts": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ts",
            "name": "Tsonga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ts",
            "name": "Tsonga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ts",
            "name": "Tsonga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ts",
            "name": "Tsonga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ts",
            "name": "Tsonga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ts",
            "name": "Tsonga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ts",
            "name": "Tsonga",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "tn": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=tn",
            "name": "Tswana",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=tn",
            "name": "Tswana",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=tn",
            "name": "Tswana",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=tn",
            "name": "Tswana",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=tn",
            "name": "Tswana",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=tn",
            "name": "Tswana",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=tn",
            "name": "Tswana",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "tum": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=tum",
            "name": "Tumbuka",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=tum",
            "name": "Tumbuka",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=tum",
            "name": "Tumbuka",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=tum",
            "name": "Tumbuka",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=tum",
            "name": "Tumbuka",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=tum",
            "name": "Tumbuka",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=tum",
            "name": "Tumbuka",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "tr": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=tr",
            "name": "Turkish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=tr",
            "name": "Turkish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=tr",
            "name": "Turkish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=tr",
            "name": "Turkish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=tr",
            "name": "Turkish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=tr",
            "name": "Turkish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=tr",
            "name": "Turkish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "tk": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=tk",
            "name": "Turkmen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=tk",
            "name": "Turkmen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=tk",
            "name": "Turkmen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=tk",
            "name": "Turkmen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=tk",
            "name": "Turkmen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=tk",
            "name": "Turkmen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=tk",
            "name": "Turkmen",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "uk": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=uk",
            "name": "Ukrainian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=uk",
            "name": "Ukrainian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=uk",
            "name": "Ukrainian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=uk",
            "name": "Ukrainian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=uk",
            "name": "Ukrainian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=uk",
            "name": "Ukrainian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=uk",
            "name": "Ukrainian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ur": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ur",
            "name": "Urdu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ur",
            "name": "Urdu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ur",
            "name": "Urdu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ur",
            "name": "Urdu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ur",
            "name": "Urdu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ur",
            "name": "Urdu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ur",
            "name": "Urdu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ug": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ug",
            "name": "Uyghur",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ug",
            "name": "Uyghur",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ug",
            "name": "Uyghur",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ug",
            "name": "Uyghur",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ug",
            "name": "Uyghur",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ug",
            "name": "Uyghur",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ug",
            "name": "Uyghur",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "uz": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=uz",
            "name": "Uzbek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=uz",
            "name": "Uzbek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=uz",
            "name": "Uzbek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=uz",
            "name": "Uzbek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=uz",
            "name": "Uzbek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=uz",
            "name": "Uzbek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=uz",
            "name": "Uzbek",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "ve": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=ve",
            "name": "Venda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=ve",
            "name": "Venda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=ve",
            "name": "Venda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=ve",
            "name": "Venda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=ve",
            "name": "Venda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=ve",
            "name": "Venda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=ve",
            "name": "Venda",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "vi": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=vi",
            "name": "Vietnamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=vi",
            "name": "Vietnamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=vi",
            "name": "Vietnamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=vi",
            "name": "Vietnamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=vi",
            "name": "Vietnamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=vi",
            "name": "Vietnamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=vi",
            "name": "Vietnamese",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "war": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=war",
            "name": "Waray",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=war",
            "name": "Waray",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=war",
            "name": "Waray",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=war",
            "name": "Waray",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=war",
            "name": "Waray",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=war",
            "name": "Waray",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=war",
            "name": "Waray",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "cy": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=cy",
            "name": "Welsh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=cy",
            "name": "Welsh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=cy",
            "name": "Welsh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=cy",
            "name": "Welsh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=cy",
            "name": "Welsh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=cy",
            "name": "Welsh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=cy",
            "name": "Welsh",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "fy": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=fy",
            "name": "Western Frisian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=fy",
            "name": "Western Frisian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=fy",
            "name": "Western Frisian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=fy",
            "name": "Western Frisian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=fy",
            "name": "Western Frisian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=fy",
            "name": "Western Frisian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=fy",
            "name": "Western Frisian",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "wo": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=wo",
            "name": "Wolof",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=wo",
            "name": "Wolof",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=wo",
            "name": "Wolof",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=wo",
            "name": "Wolof",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=wo",
            "name": "Wolof",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=wo",
            "name": "Wolof",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=wo",
            "name": "Wolof",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "xh": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=xh",
            "name": "Xhosa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=xh",
            "name": "Xhosa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=xh",
            "name": "Xhosa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=xh",
            "name": "Xhosa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=xh",
            "name": "Xhosa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=xh",
            "name": "Xhosa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=xh",
            "name": "Xhosa",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "yi": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=yi",
            "name": "Yiddish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=yi",
            "name": "Yiddish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=yi",
            "name": "Yiddish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=yi",
            "name": "Yiddish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=yi",
            "name": "Yiddish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=yi",
            "name": "Yiddish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=yi",
            "name": "Yiddish",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "yo": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=yo",
            "name": "Yoruba",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=yo",
            "name": "Yoruba",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=yo",
            "name": "Yoruba",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=yo",
            "name": "Yoruba",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=yo",
            "name": "Yoruba",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=yo",
            "name": "Yoruba",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=yo",
            "name": "Yoruba",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ],
        "zu": [
          {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=json3&tlang=zu",
            "name": "Zulu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv1&tlang=zu",
            "name": "Zulu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv2&tlang=zu",
            "name": "Zulu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srv3&tlang=zu",
            "name": "Zulu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=ttml&tlang=zu",
            "name": "Zulu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=srt&tlang=zu",
            "name": "Zulu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          },
          {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=cP3eChqUphA&ei=Zog7ataHLdugsfIPr8XFkA8&caps=asr&opi=112496729&xoaf=4&xowf=1&hl=en&ip=0.0.0.0&ipbits=0&expire=1782311638&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=A71830BC4F5B47687E40959ED23E8C8DD986D0F6.C0164684D083EF103330482619E8C2F1E29DDE56&key=yt8&kind=asr&lang=en&fmt=vtt&tlang=zu",
            "name": "Zulu",
            "impersonate": True,
            "__yt_dlp_client": "android_vr"
          }
        ]
      },
      "subtitles": {},
      "comment_count": 2300,
      "chapters": None,
      "heatmap": [
        { "start_time": 0.0, "end_time": 1.35, "value": 0.0007013541673999828 },
        { "start_time": 1.35, "end_time": 2.7, "value": 0.0 },
        { "start_time": 2.7, "end_time": 4.05, "value": 0.0561962889212759 },
        { "start_time": 4.05, "end_time": 5.4, "value": 0.07031573829761013 },
        { "start_time": 5.4, "end_time": 6.75, "value": 0.07417212600219049 },
        { "start_time": 6.75, "end_time": 8.1, "value": 0.07911180012907496 },
        { "start_time": 8.1, "end_time": 9.45, "value": 0.08001697024329585 },
        { "start_time": 9.45, "end_time": 10.8, "value": 0.07444489840542648 },
        { "start_time": 10.8, "end_time": 12.15, "value": 0.06938893977455056 },
        { "start_time": 12.15, "end_time": 13.5, "value": 0.0704899530103734 },
        { "start_time": 13.5, "end_time": 14.85, "value": 0.06977943857570057 },
        { "start_time": 14.85, "end_time": 16.2, "value": 0.07573463011052796 },
        { "start_time": 16.2, "end_time": 17.55, "value": 0.07678212363663628 },
        { "start_time": 17.55, "end_time": 18.9, "value": 0.07711155398930064 },
        { "start_time": 18.9, "end_time": 20.25, "value": 0.08025072669333266 },
        { "start_time": 20.25, "end_time": 21.6, "value": 0.08947715145204231 },
        { "start_time": 21.6, "end_time": 22.95, "value": 0.0927080116460924 },
        { "start_time": 22.95, "end_time": 24.3, "value": 0.09823818374291744 },
        { "start_time": 24.3, "end_time": 25.65, "value": 0.10444188993616565 },
        { "start_time": 25.65, "end_time": 27.0, "value": 0.11493938659627284 },
        { "start_time": 27.0, "end_time": 28.35, "value": 0.11935293907599535 },
        { "start_time": 28.35, "end_time": 29.7, "value": 0.14265682865270535 },
        { "start_time": 29.7, "end_time": 31.05, "value": 0.14648454811341327 },
        { "start_time": 31.05, "end_time": 32.4, "value": 0.15237137691285252 },
        { "start_time": 32.4, "end_time": 33.75, "value": 0.15569579057729108 },
        { "start_time": 33.75, "end_time": 35.1, "value": 0.16145149184706525 },
        { "start_time": 35.1, "end_time": 36.45, "value": 0.16588786017768034 },
        { "start_time": 36.45, "end_time": 37.8, "value": 0.17508697376915058 },
        { "start_time": 37.8, "end_time": 39.15, "value": 0.1840368093465939 },
        { "start_time": 39.15, "end_time": 40.5, "value": 0.20743213196145324 },
        { "start_time": 40.5, "end_time": 41.85, "value": 0.2170094458470868 },
        { "start_time": 41.85, "end_time": 43.2, "value": 0.23664515728475768 },
        { "start_time": 43.2, "end_time": 44.55, "value": 0.25023322634197703 },
        { "start_time": 44.55, "end_time": 45.9, "value": 0.2684088929571031 },
        { "start_time": 45.9, "end_time": 47.25, "value": 0.28566005111598775 },
        { "start_time": 47.25, "end_time": 48.6, "value": 0.3055218006303451 },
        { "start_time": 48.6, "end_time": 49.95, "value": 0.3030252885293352 },
        { "start_time": 49.95, "end_time": 51.3, "value": 0.2951700200737079 },
        { "start_time": 51.3, "end_time": 52.65, "value": 0.300747011314372 },
        { "start_time": 52.65, "end_time": 54.0, "value": 0.3281016898233417 },
        { "start_time": 54.0, "end_time": 55.35, "value": 0.34218653374553404 },
        { "start_time": 55.35, "end_time": 56.7, "value": 0.3556936871085099 },
        { "start_time": 56.7, "end_time": 58.05, "value": 0.3869045836874809 },
        { "start_time": 58.05, "end_time": 59.4, "value": 0.41848231504381367 },
        { "start_time": 59.4, "end_time": 60.75, "value": 0.4442241079744452 },
        { "start_time": 60.75, "end_time": 62.1, "value": 0.44461850837091516 },
        { "start_time": 62.1, "end_time": 63.45, "value": 0.4129913285347669 },
        { "start_time": 63.45, "end_time": 64.8, "value": 0.3880485992891124 },
        { "start_time": 64.8, "end_time": 66.15, "value": 0.37092890792905103 },
        { "start_time": 66.15, "end_time": 67.5, "value": 0.3599702596655875 },
        { "start_time": 67.5, "end_time": 68.85, "value": 0.35325120362095186 },
        { "start_time": 68.85, "end_time": 70.2, "value": 0.347849614535105 },
        { "start_time": 70.2, "end_time": 71.55, "value": 0.3431736373614732 },
        { "start_time": 71.55, "end_time": 72.9, "value": 0.3414526945562313 },
        { "start_time": 72.9, "end_time": 74.25, "value": 0.34208263256581883 },
        { "start_time": 74.25, "end_time": 75.6, "value": 0.3475052563394775 },
        { "start_time": 75.6, "end_time": 76.95, "value": 0.3487062691596956 },
        { "start_time": 76.95, "end_time": 78.3, "value": 0.349895577193954 },
        { "start_time": 78.3, "end_time": 79.65, "value": 0.35163526462018946 },
        { "start_time": 79.65, "end_time": 81.0, "value": 0.35807841002187524 },
        { "start_time": 81.0, "end_time": 82.35, "value": 0.3603893418933204 },
        { "start_time": 82.35, "end_time": 83.7, "value": 0.3647810963296251 },
        { "start_time": 83.7, "end_time": 85.05, "value": 0.36916436903697347 },
        { "start_time": 85.05, "end_time": 86.4, "value": 0.3803535506934704 },
        { "start_time": 86.4, "end_time": 87.75, "value": 0.3872896541820988 },
        { "start_time": 87.75, "end_time": 89.1, "value": 0.3935830122504156 },
        { "start_time": 89.1, "end_time": 90.45, "value": 0.4009532954443192 },
        { "start_time": 90.45, "end_time": 91.8, "value": 0.41428648854640043 },
        { "start_time": 91.8, "end_time": 93.15, "value": 0.42105914911804015 },
        { "start_time": 93.15, "end_time": 94.5, "value": 0.42758244685836333 },
        { "start_time": 94.5, "end_time": 95.85, "value": 0.4321159309855286 },
        { "start_time": 95.85, "end_time": 97.2, "value": 0.44617490563440404 },
        { "start_time": 97.2, "end_time": 98.55, "value": 0.4536590136309018 },
        { "start_time": 98.55, "end_time": 99.9, "value": 0.46542995707651424 },
        { "start_time": 99.9, "end_time": 101.25, "value": 0.4787746005126866 },
        {
          "start_time": 101.25,
          "end_time": 102.6,
          "value": 0.5097601375532875
        },
        {
          "start_time": 102.6,
          "end_time": 103.95,
          "value": 0.5285933077971092
        },
        {
          "start_time": 103.95,
          "end_time": 105.3,
          "value": 0.5581005642979092
        },
        {
          "start_time": 105.3,
          "end_time": 106.65,
          "value": 0.6051046098281695
        },
        {
          "start_time": 106.65,
          "end_time": 108.0,
          "value": 0.7332762569519431
        },
        {
          "start_time": 108.0,
          "end_time": 109.35,
          "value": 0.8006242382877289
        },
        {
          "start_time": 109.35,
          "end_time": 110.7,
          "value": 0.8640862306848767
        },
        {
          "start_time": 110.7,
          "end_time": 112.05,
          "value": 0.9315682233381727
        },
        { "start_time": 112.05, "end_time": 113.4, "value": 1.0 },
        {
          "start_time": 113.4,
          "end_time": 114.75,
          "value": 0.9866405983554436
        },
        {
          "start_time": 114.75,
          "end_time": 116.1,
          "value": 0.9380156944216262
        },
        {
          "start_time": 116.1,
          "end_time": 117.45,
          "value": 0.8392417198605366
        },
        {
          "start_time": 117.45,
          "end_time": 118.8,
          "value": 0.7152003354693437
        },
        {
          "start_time": 118.8,
          "end_time": 120.15,
          "value": 0.6276454830679669
        },
        {
          "start_time": 120.15,
          "end_time": 121.5,
          "value": 0.5754132998090169
        },
        {
          "start_time": 121.5,
          "end_time": 122.85,
          "value": 0.5709968635414492
        },
        {
          "start_time": 122.85,
          "end_time": 124.2,
          "value": 0.5791299934376863
        },
        {
          "start_time": 124.2,
          "end_time": 125.55,
          "value": 0.5964242387796692
        },
        {
          "start_time": 125.55,
          "end_time": 126.9,
          "value": 0.6086535348580825
        },
        {
          "start_time": 126.9,
          "end_time": 128.25,
          "value": 0.6301667618175294
        },
        { "start_time": 128.25, "end_time": 129.6, "value": 0.657281322579745 },
        {
          "start_time": 129.6,
          "end_time": 130.95,
          "value": 0.6852462614871236
        },
        {
          "start_time": 130.95,
          "end_time": 132.3,
          "value": 0.6985878515008717
        },
        {
          "start_time": 132.3,
          "end_time": 133.65,
          "value": 0.7345902464018598
        },
        { "start_time": 133.65, "end_time": 135.0, "value": 0.7556629323593141 }
      ],
      "like_count": 19770,
      "channel_follower_count": 645,
      "creators": None,
      "upload_date": "20191011",
      "original_url": "cP3eChqUphA",
      "webpage_url_basename": "watch",
      "webpage_url_domain": "youtube.com",
      "extractor": "youtube",
      "extractor_key": "Youtube",
      "display_id": "cP3eChqUphA",
      "fulltitle": "Senzawa - [\"When I'm Gone\"] Cups Cover",
      "duration_string": "2:15",
      "release_year": None,
      "is_live": False,
      "was_live": False,
      "requested_subtitles": None,
      "_has_drm": None,
      "epoch": 1782286440,
      "requested_downloads": [
        {
          "requested_formats": [
            {
              "asr": None,
              "filesize": 23515598,
              "format_id": "136",
              "format_note": "720p",
              "source_preference": -1,
              "fps": 24,
              "audio_channels": None,
              "height": 720,
              "quality": 8.0,
              "has_drm": False,
              "tbr": 1397.305,
              "filesize_approx": 23515595,
              "width": 1280,
              "language": None,
              "language_preference": -1,
              "preference": None,
              "ext": "mp4",
              "vcodec": "avc1.64001f",
              "acodec": "none",
              "dynamic_range": "SDR",
              "container": "mp4_dash",
              "url": "https://rr2---sn-a5meknzr.googlevideo.com/videoplayback?expire=1782308038&ei=Zog7ataHLdugsfIPr8XFkA8&ip=47.147.88.26&id=o-AKNIFvcG3SgOlNxz7CVhQ57Qsz1fyHRPBgdWYne_-Rl-&itag=136&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=381&met=1782286438%2C&mh=As&mm=31%2C26&mn=sn-a5meknzr%2Csn-vgqskn6y&ms=au%2Conr&mv=m&mvi=2&pl=12&rms=au%2Cau&initcwndbps=3750000&bui=ARmQxEW1Gsi3sb39UJHNcf0H4Zq8G-03EjXEnskInoyyW2K1yzd-cKsh_2UPSllc-wBVdtv6nN2Gm0L_&spc=SQ-umpTvy_oesEoe5hMTm0g4-6gnSxSxrPlXnPChMX6G&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=23515598&dur=134.634&lmt=1744758854329087&mt=1782285909&fvip=4&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5309224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgKVTEE6ZxgrjCXaFAaizYtPySb7_-mamNojBSsrTk3LwCIQDixT88oZuwvokb-FenHc8dnPgO0gKqp9opk6ge4MAyCQ%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRgIhAOAZex_mL1p_pDQPHZETwG81pWnS4VEv41O_YSWUkYghAiEAuyCow7d5mP3LhYVmbD-Iuaeu7Qxe7umQtw21bFb6mC4%3D",
              "available_at": 1782286439,
              "downloader_options": { "http_chunk_size": 10485760 },
              "protocol": "https",
              "video_ext": "mp4",
              "audio_ext": "none",
              "abr": 0,
              "vbr": 1397.305,
              "resolution": "1280x720",
              "aspect_ratio": 1.78,
              "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-us,en;q=0.5",
                "Sec-Fetch-Mode": "navigate"
              },
              "format": "136 - 1280x720 (720p)",
              "filepath": "test\\When I'm Gone [...AKxFsGy5v0b]\\Videos\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover [cP3eChqUphA]\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover.f136.mp4"
            },
            {
              "asr": 48000,
              "filesize": 2393857,
              "format_id": "251",
              "format_note": "medium",
              "source_preference": -1,
              "fps": None,
              "audio_channels": 2,
              "height": None,
              "quality": 3.0,
              "has_drm": False,
              "tbr": 142.215,
              "filesize_approx": 2393851,
              "width": None,
              "language": "en",
              "language_preference": -1,
              "preference": None,
              "ext": "webm",
              "vcodec": "none",
              "acodec": "opus",
              "dynamic_range": None,
              "container": "webm_dash",
              "url": "https://rr2---sn-a5meknzr.googlevideo.com/videoplayback?expire=1782308038&ei=Zog7ataHLdugsfIPr8XFkA8&ip=47.147.88.26&id=o-AKNIFvcG3SgOlNxz7CVhQ57Qsz1fyHRPBgdWYne_-Rl-&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=381&met=1782286438%2C&mh=As&mm=31%2C26&mn=sn-a5meknzr%2Csn-vgqskn6y&ms=au%2Conr&mv=m&mvi=2&pl=12&rms=au%2Cau&initcwndbps=3750000&bui=ARmQxEW1Gsi3sb39UJHNcf0H4Zq8G-03EjXEnskInoyyW2K1yzd-cKsh_2UPSllc-wBVdtv6nN2Gm0L_&spc=SQ-umpTvy_oesEoe5hMTm0g4-6gnSxSxrPlXnPChMX6G&vprv=1&svpuc=1&mime=audio%2Fwebm&rqh=1&gir=yes&clen=2393857&dur=134.661&lmt=1744758855452408&mt=1782285909&fvip=4&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5308224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgd6SdQ3gDLuUNdOknwgzUYzrDfapI9ghKrvJoDXv8xZQCIQD1Uw33ACVjtLC54-c04KwiF0_Ssr9FWQLsrjPsUmA1eA%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRgIhAOAZex_mL1p_pDQPHZETwG81pWnS4VEv41O_YSWUkYghAiEAuyCow7d5mP3LhYVmbD-Iuaeu7Qxe7umQtw21bFb6mC4%3D",
              "available_at": 1782286439,
              "downloader_options": { "http_chunk_size": 10485760 },
              "protocol": "https",
              "audio_ext": "webm",
              "video_ext": "none",
              "vbr": 0,
              "abr": 142.215,
              "resolution": "audio only",
              "aspect_ratio": None,
              "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-us,en;q=0.5",
                "Sec-Fetch-Mode": "navigate"
              },
              "format": "251 - audio only (medium)",
              "filepath": "test\\When I'm Gone [...AKxFsGy5v0b]\\Videos\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover [cP3eChqUphA]\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover.f251.webm"
            }
          ],
          "format": "136 - 1280x720 (720p)+251 - audio only (medium)",
          "format_id": "136+251",
          "ext": "mkv",
          "protocol": "https+https",
          "language": "en",
          "format_note": "720p+medium",
          "filesize_approx": 25909455,
          "tbr": 1539.52,
          "width": 1280,
          "height": 720,
          "resolution": "1280x720",
          "fps": 24,
          "dynamic_range": "SDR",
          "vcodec": "avc1.64001f",
          "vbr": 1397.305,
          "aspect_ratio": 1.78,
          "acodec": "opus",
          "abr": 142.215,
          "asr": 48000,
          "audio_channels": 2,
          "_filename": "test\\When I'm Gone [...AKxFsGy5v0b]\\Videos\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover [cP3eChqUphA]\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover.mkv",
          "filename": "test\\When I'm Gone [...AKxFsGy5v0b]\\Videos\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover [cP3eChqUphA]\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover.mkv",
          "__postprocessors": [
            "<yt_dlp.postprocessor.ffmpeg.FFmpegMergerPP object at 0x00000283142379D0>"
          ],
          "__real_download": True,
          "__files_to_merge": [
            "test\\When I'm Gone [...AKxFsGy5v0b]\\Videos\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover [cP3eChqUphA]\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover.f136.mp4",
            "test\\When I'm Gone [...AKxFsGy5v0b]\\Videos\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover [cP3eChqUphA]\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover.f251.webm"
          ],
          "__finaldir": "C:\\Users\\nicol\\Documents\\VS-Code-Projects\\yt_downloader\\test\\When I'm Gone [...AKxFsGy5v0b]\\Videos\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover [cP3eChqUphA]",
          "filepath": "C:\\Users\\nicol\\Documents\\VS-Code-Projects\\yt_downloader\\test\\When I'm Gone [...AKxFsGy5v0b]\\Videos\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover [cP3eChqUphA]\\Senzawa - [\uff02When I'm Gone\uff02] Cups Cover.mkv",
          "__write_download_archive": True
        }
      ],
      "requested_formats": [
        {
          "asr": None,
          "filesize": 23515598,
          "format_id": "136",
          "format_note": "720p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 720,
          "quality": 8.0,
          "has_drm": False,
          "tbr": 1397.305,
          "filesize_approx": 23515595,
          "width": 1280,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.64001f",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr2---sn-a5meknzr.googlevideo.com/videoplayback?expire=1782308038&ei=Zog7ataHLdugsfIPr8XFkA8&ip=47.147.88.26&id=o-AKNIFvcG3SgOlNxz7CVhQ57Qsz1fyHRPBgdWYne_-Rl-&itag=136&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=381&met=1782286438%2C&mh=As&mm=31%2C26&mn=sn-a5meknzr%2Csn-vgqskn6y&ms=au%2Conr&mv=m&mvi=2&pl=12&rms=au%2Cau&initcwndbps=3750000&bui=ARmQxEW1Gsi3sb39UJHNcf0H4Zq8G-03EjXEnskInoyyW2K1yzd-cKsh_2UPSllc-wBVdtv6nN2Gm0L_&spc=SQ-umpTvy_oesEoe5hMTm0g4-6gnSxSxrPlXnPChMX6G&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=23515598&dur=134.634&lmt=1744758854329087&mt=1782285909&fvip=4&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5309224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgKVTEE6ZxgrjCXaFAaizYtPySb7_-mamNojBSsrTk3LwCIQDixT88oZuwvokb-FenHc8dnPgO0gKqp9opk6ge4MAyCQ%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRgIhAOAZex_mL1p_pDQPHZETwG81pWnS4VEv41O_YSWUkYghAiEAuyCow7d5mP3LhYVmbD-Iuaeu7Qxe7umQtw21bFb6mC4%3D",
          "available_at": 1782286439,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 1397.305,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "136 - 1280x720 (720p)"
        },
        {
          "asr": 48000,
          "filesize": 2393857,
          "format_id": "251",
          "format_note": "medium",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 3.0,
          "has_drm": False,
          "tbr": 142.215,
          "filesize_approx": 2393851,
          "width": None,
          "language": "en",
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "none",
          "acodec": "opus",
          "dynamic_range": None,
          "container": "webm_dash",
          "url": "https://rr2---sn-a5meknzr.googlevideo.com/videoplayback?expire=1782308038&ei=Zog7ataHLdugsfIPr8XFkA8&ip=47.147.88.26&id=o-AKNIFvcG3SgOlNxz7CVhQ57Qsz1fyHRPBgdWYne_-Rl-&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=381&met=1782286438%2C&mh=As&mm=31%2C26&mn=sn-a5meknzr%2Csn-vgqskn6y&ms=au%2Conr&mv=m&mvi=2&pl=12&rms=au%2Cau&initcwndbps=3750000&bui=ARmQxEW1Gsi3sb39UJHNcf0H4Zq8G-03EjXEnskInoyyW2K1yzd-cKsh_2UPSllc-wBVdtv6nN2Gm0L_&spc=SQ-umpTvy_oesEoe5hMTm0g4-6gnSxSxrPlXnPChMX6G&vprv=1&svpuc=1&mime=audio%2Fwebm&rqh=1&gir=yes&clen=2393857&dur=134.661&lmt=1744758855452408&mt=1782285909&fvip=4&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5308224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgd6SdQ3gDLuUNdOknwgzUYzrDfapI9ghKrvJoDXv8xZQCIQD1Uw33ACVjtLC54-c04KwiF0_Ssr9FWQLsrjPsUmA1eA%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRgIhAOAZex_mL1p_pDQPHZETwG81pWnS4VEv41O_YSWUkYghAiEAuyCow7d5mP3LhYVmbD-Iuaeu7Qxe7umQtw21bFb6mC4%3D",
          "available_at": 1782286439,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "webm",
          "video_ext": "none",
          "vbr": 0,
          "abr": 142.215,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "251 - audio only (medium)"
        }
      ],
      "format": "136 - 1280x720 (720p)+251 - audio only (medium)",
      "format_id": "136+251",
      "ext": "mkv",
      "protocol": "https+https",
      "language": "en",
      "format_note": "720p+medium",
      "filesize_approx": 25909455,
      "tbr": 1539.52,
      "width": 1280,
      "height": 720,
      "resolution": "1280x720",
      "fps": 24,
      "dynamic_range": "SDR",
      "vcodec": "avc1.64001f",
      "vbr": 1397.305,
      "stretched_ratio": None,
      "aspect_ratio": 1.78,
      "acodec": "opus",
      "abr": 142.215,
      "asr": 48000,
      "audio_channels": 2
    },
    {
        'playlist_count':               1,
    'playlist_title':               '',
    'playlist_channel_id':          '',
    'playlist_webpage_url':         '',
    'n_entries':                    1,
    'playlist_autonumber':          1,
    'playlist':                     '',
    'playlist_channel':             '',
    'playlist_id':                  '',
    'playlist_uploader':            '',
    'playlist_uploader_id':         '',
    'playlist_index':               1,
      "_type": "url",
      "ie_key": "Youtube",
      "id": "YZwSzGYtvWg",
      "url": "https://www.youtube.com/watch?v=YZwSzGYtvWg",
      "title": "Gawr Gura - When I'm Gone",
      "description": "Bye bye.\n\n----------------------------------\nShe\u2018s gone, watch the shark legacy here:\n@GawrGura \n\nOuttro:\nhttps://www.youtube.com/watch?v=fdtbaAGxxQA\n\nThumbnail artwork:\nhttps://twitter.com/Weizen029/status/1326586726790426626?s=20\n\nMy Twitter:\nhttps://twitter.com/blueAwoo2\n\n----------------------------------\nThis is a fanmade edit.\n\nRespect the talents current role and don't unrelatedly bring up past lives, please.\nRemember to behave in their streams and read the rules as well!\n\n#gawrgura #chumbuds #HololiveEnglish",
      "duration": 125,
      "channel_id": "UCE6l02Iwv7vJlAXfBE7ZUcw",
      "channel": "blueAwoo",
      "channel_url": "https://www.youtube.com/channel/UCE6l02Iwv7vJlAXfBE7ZUcw",
      "uploader": "blueAwoo",
      "uploader_id": "@blueAwoo",
      "uploader_url": "https://www.youtube.com/@blueAwoo",
      "thumbnails": [
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/3.jpg",
          "preference": -37,
          "id": "0"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/3.webp",
          "preference": -36,
          "id": "1"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/2.jpg",
          "preference": -35,
          "id": "2"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/2.webp",
          "preference": -34,
          "id": "3"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/1.jpg",
          "preference": -33,
          "id": "4"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/1.webp",
          "preference": -32,
          "id": "5"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/mq3.jpg",
          "preference": -31,
          "id": "6"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/mq3.webp",
          "preference": -30,
          "id": "7"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/mq2.jpg",
          "preference": -29,
          "id": "8"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/mq2.webp",
          "preference": -28,
          "id": "9"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/mq1.jpg",
          "preference": -27,
          "id": "10"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/mq1.webp",
          "preference": -26,
          "id": "11"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/hq3.jpg",
          "preference": -25,
          "id": "12"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/hq3.webp",
          "preference": -24,
          "id": "13"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/hq2.jpg",
          "preference": -23,
          "id": "14"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/hq2.webp",
          "preference": -22,
          "id": "15"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/hq1.jpg",
          "preference": -21,
          "id": "16"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/hq1.webp",
          "preference": -20,
          "id": "17"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/sd3.jpg",
          "preference": -19,
          "id": "18"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/sd3.webp",
          "preference": -18,
          "id": "19"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/sd2.jpg",
          "preference": -17,
          "id": "20"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/sd2.webp",
          "preference": -16,
          "id": "21"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/sd1.jpg",
          "preference": -15,
          "id": "22"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/sd1.webp",
          "preference": -14,
          "id": "23"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/default.jpg",
          "height": 90,
          "width": 120,
          "preference": -13,
          "id": "24",
          "resolution": "120x90"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/default.webp",
          "preference": -12,
          "id": "25"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/mqdefault.jpg",
          "height": 180,
          "width": 320,
          "preference": -11,
          "id": "26",
          "resolution": "320x180"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/mqdefault.webp",
          "preference": -10,
          "id": "27"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/0.jpg",
          "preference": -9,
          "id": "28"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/0.webp",
          "preference": -8,
          "id": "29"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/hqdefault.jpg?sqp=-oaymwEiCKgBEF5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4CLAWCbHM9awUbLx5oqzYe8Vs2UjWcg",
          "height": 94,
          "width": 168,
          "preference": -7,
          "id": "30",
          "resolution": "168x94"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/hqdefault.jpg?sqp=-oaymwEiCMQBEG5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4CLAQvxuf5GuMWWSaoK4e-f_a-8N4Aw",
          "height": 110,
          "width": 196,
          "preference": -7,
          "id": "31",
          "resolution": "196x110"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/hqdefault.jpg?sqp=-oaymwEjCPYBEIoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLDRHJnayY_uWGQiKZJVHzgeyURC-A",
          "height": 138,
          "width": 246,
          "preference": -7,
          "id": "32",
          "resolution": "246x138"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/hqdefault.jpg?sqp=-oaymwEjCNACELwBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLBpjDdnzYDnyERi1hPpVqzsPWmFqQ",
          "height": 188,
          "width": 336,
          "preference": -7,
          "id": "33",
          "resolution": "336x188"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/hqdefault.jpg",
          "height": 360,
          "width": 480,
          "preference": -7,
          "id": "34",
          "resolution": "480x360"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/hqdefault.webp",
          "preference": -6,
          "id": "35"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/sddefault.jpg",
          "height": 480,
          "width": 640,
          "preference": -5,
          "id": "36",
          "resolution": "640x480"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/sddefault.webp",
          "preference": -4,
          "id": "37"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/hq720.jpg",
          "preference": -3,
          "id": "38"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/hq720.webp",
          "preference": -2,
          "id": "39"
        },
        {
          "url": "https://i.ytimg.com/vi/YZwSzGYtvWg/maxresdefault.jpg",
          "height": 1080,
          "width": 1920,
          "preference": -1,
          "id": "40",
          "resolution": "1920x1080"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/YZwSzGYtvWg/maxresdefault.webp",
          "preference": 0,
          "id": "41"
        }
      ],
      "timestamp": 1613182016,
      "release_timestamp": None,
      "availability": "public",
      "view_count": 5765682,
      "live_status": "not_live",
      "channel_is_verified": True,
      "__x_forwarded_for_ip": None,
      "playlist": None,
      "playlist_id": "PLXOfMLBzXbbVV8P-wQyZ9MAKxFsGy5v0b",
      "playlist_index": None,
      "playlist_uploader": "Some Random User",
      "playlist_uploader_id": "@somerandomuser8005",
      "playlist_channel": "Some Random User",
      "formats": [
        {
          "format_id": "sb3",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L0/default.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLD2wa81HdIgWZ4Czzo7mUp3EPq_EQ",
          "width": 48,
          "height": 27,
          "fps": 0.8,
          "rows": 10,
          "columns": 10,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L0/default.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLD2wa81HdIgWZ4Czzo7mUp3EPq_EQ",
              "duration": 125.0
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "48x27",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb3 - 48x27 (storyboard)"
        },
        {
          "format_id": "sb2",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L1/M$M.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLCmZQZJZgSvqKdcXLsBJqL8LRDGSg",
          "width": 80,
          "height": 45,
          "fps": 0.512,
          "rows": 10,
          "columns": 10,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L1/M0.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLCmZQZJZgSvqKdcXLsBJqL8LRDGSg",
              "duration": 125.0
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "80x45",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb2 - 80x45 (storyboard)"
        },
        {
          "format_id": "sb1",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L2/M$M.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBWNKBciEtxeNgEGID9ABWWzE9VLg",
          "width": 160,
          "height": 90,
          "fps": 0.512,
          "rows": 5,
          "columns": 5,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L2/M0.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBWNKBciEtxeNgEGID9ABWWzE9VLg",
              "duration": 48.828125
            },
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L2/M1.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBWNKBciEtxeNgEGID9ABWWzE9VLg",
              "duration": 48.828125
            },
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L2/M2.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBWNKBciEtxeNgEGID9ABWWzE9VLg",
              "duration": 27.34375
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "160x90",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb1 - 160x90 (storyboard)"
        },
        {
          "format_id": "sb0",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L3/M$M.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBZLp-1al0p5GkFBcVMj7D-WyL2-g",
          "width": 320,
          "height": 180,
          "fps": 0.512,
          "rows": 3,
          "columns": 3,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L3/M0.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBZLp-1al0p5GkFBcVMj7D-WyL2-g",
              "duration": 17.578125
            },
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L3/M1.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBZLp-1al0p5GkFBcVMj7D-WyL2-g",
              "duration": 17.578125
            },
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L3/M2.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBZLp-1al0p5GkFBcVMj7D-WyL2-g",
              "duration": 17.578125
            },
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L3/M3.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBZLp-1al0p5GkFBcVMj7D-WyL2-g",
              "duration": 17.578125
            },
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L3/M4.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBZLp-1al0p5GkFBcVMj7D-WyL2-g",
              "duration": 17.578125
            },
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L3/M5.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBZLp-1al0p5GkFBcVMj7D-WyL2-g",
              "duration": 17.578125
            },
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L3/M6.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBZLp-1al0p5GkFBcVMj7D-WyL2-g",
              "duration": 17.578125
            },
            {
              "url": "https://i.ytimg.com/sb/YZwSzGYtvWg/storyboard3_L3/M7.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCMn8kKgG&sigh=rs$AOn4CLBZLp-1al0p5GkFBcVMj7D-WyL2-g",
              "duration": 1.953125
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "320x180",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb0 - 320x180 (storyboard)"
        },
        {
          "asr": 22050,
          "filesize": 765910,
          "format_id": "139",
          "format_note": "low",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 2.0,
          "has_drm": False,
          "tbr": 48.866,
          "filesize_approx": 765895,
          "width": None,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "m4a",
          "vcodec": "none",
          "acodec": "mp4a.40.5",
          "dynamic_range": None,
          "container": "m4a_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=139&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=765910&dur=125.387&lmt=1744772028521410&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5532534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAPXw_QPQ0lfY_44hZnDKS44eVAvpkyfS_rBM08beclv-AiEAxyTVyTCeNev1ukb7kOipMNbYYE5GZR2zljfIRog4sVQ%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "m4a",
          "video_ext": "none",
          "vbr": 0,
          "abr": 48.866,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "139 - audio only (low)"
        },
        {
          "asr": 48000,
          "filesize": 869989,
          "format_id": "249",
          "format_note": "low",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 2.0,
          "has_drm": False,
          "tbr": 55.554,
          "filesize_approx": 869982,
          "width": None,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "none",
          "acodec": "opus",
          "dynamic_range": None,
          "container": "webm_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=249&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=audio%2Fwebm&rqh=1&gir=yes&clen=869989&dur=125.281&lmt=1744772488363707&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5532534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAKFV_PshpJJEteAWLEdgjQMW6RdoAV3_ViHr9WLUJgszAiBilEF9IEtm6p9SbML01EjZPLndq5EtGSOMzbedTFD2Cg%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "webm",
          "video_ext": "none",
          "vbr": 0,
          "abr": 55.554,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "249 - audio only (low)"
        },
        {
          "asr": 44100,
          "filesize": 2029119,
          "format_id": "140",
          "format_note": "medium",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 3.0,
          "has_drm": False,
          "tbr": 129.534,
          "filesize_approx": 2029117,
          "width": None,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "m4a",
          "vcodec": "none",
          "acodec": "mp4a.40.2",
          "dynamic_range": None,
          "container": "m4a_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=140&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=2029119&dur=125.318&lmt=1744772028535485&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5532534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhANel_JFfptMWd0HJkKEfXe3Bpp5Aw5kuxJ0wZSNEntppAiBOXqeezSy1CxpuWTiYA5gfMhGHzovftLlw-zb-iBxXtA%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "m4a",
          "video_ext": "none",
          "vbr": 0,
          "abr": 129.534,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "140 - audio only (medium)"
        },
        {
          "asr": 48000,
          "filesize": 2157598,
          "format_id": "251",
          "format_note": "medium",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 3.0,
          "has_drm": False,
          "tbr": 137.776,
          "filesize_approx": 2157589,
          "width": None,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "none",
          "acodec": "opus",
          "dynamic_range": None,
          "container": "webm_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=audio%2Fwebm&rqh=1&gir=yes&clen=2157598&dur=125.281&lmt=1744772498105829&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5532534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgNW5IAkxAb9ozkqnG4B7HOnDV-9E949gQpEqOej3yVO0CID2urNXgH-GzlMDC0oD5r1Xd-_01QRTStbMViicGwStR&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "webm",
          "video_ext": "none",
          "vbr": 0,
          "abr": 137.776,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "251 - audio only (medium)"
        },
        {
          "format_id": "91",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308066/ei/gog7asqjGrSLlu8PubmLoA0/ip/47.147.88.26/id/619c12cc662dbd68/itag/91/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D765910%3Bdur%3D125.387%3Bgir%3Dyes%3Bitag%3D139%3Blmt%3D1744772028521410/sgovp/clen%3D860922%3Bdur%3D125.258%3Bgir%3Dyes%3Bitag%3D160%3Blmt%3D1744775415343276/rqh/1/hls_chunk_host/rr1---sn-a5mekn6k.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/402/met/1782286466,/mh/TV/mm/31,29/mn/sn-a5mekn6k,sn-a5mlrnll/ms/au,rdu/mv/m/mvi/1/pl/12/rms/au,au/initcwndbps/3750000/bui/ARmQxEUNzaIumqBOnNkHLhg-YrXPdXh-AkY7o-Xeng27qUb7ijfJITw3XQCSQE6IvvzeOULJd1ftLpNm/spc/SQ-umlGRvtBDE0KpGIo2tnD6N3qd7qRUOjet39gx0oeYzDb3NKEl6EabtFyapVElP-TMKHbj/vprv/1/ns/VLAX1wE0fzIm9Fad-RZ1PFwW/playlist_type/CLEAN/dover/11/txp/5535534/mt/1782285909/fvip/4/keepalive/yes/fexp/51565116,51565682,51987687/n/frLTt21veyP0UQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRAIgdGmflO4Vfa7UIiTb2xOuoh3m_zTGChBPpnOLJNkE-NMCIAMwwJ6pqzFrG6071PZRhKua91X6n7vxMFie_aLUdi19/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIhALD4b4o0jHKun5kK1oaK3O877JOv1g-uIXuYjy_Df7UlAiAVmNczOqtRqhLLrSC5W-dLIeFkUUy4y3OwF18m42Dy4g%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308066/ei/gog7asqjGrSLlu8PubmLoA0/ip/47.147.88.26/id/619c12cc662dbd68/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr1---sn-a5mekn6k.googlevideo.com/cps/402/met/1782286466%2C/mh/TV/mm/31%2C29/mn/sn-a5mekn6k%2Csn-a5mlrnll/ms/au%2Crdu/mv/m/mvi/1/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3750000/bui/ARmQxEUNzaIumqBOnNkHLhg-YrXPdXh-AkY7o-Xeng27qUb7ijfJITw3XQCSQE6IvvzeOULJd1ftLpNm/spc/SQ-umlGRvtBDE0KpGIo2tnD6N3qd7qRUOjet39gx0oeYzDb3NKEl6EabtFyapVElP-TMKHbj/vprv/1/go/1/ns/VLAX1wE0fzIm9Fad-RZ1PFwW/rqh/5/mt/1782285909/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51987687/dover/11/n/frLTt21veyP0UQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRgIhAITp5QBJCzbUWidXDZ6ZEZa6u_-Xm0HkjE08BiefjnCaAiEA1bigj1nOX-Iyaa5l9FN5GnZVifUbn4JnXb4Y7yDjeJE%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIhAN8ZWFZj4YzVWLUJL1GB8Nu9nAdXNou742UamxSmuOakAiBVp0i1UBe89oJqN7oyWnzxQavtZEF1icgXFaC8e9faSQ%3D%3D/file/index.m3u8",
          "tbr": 161.702,
          "ext": "mp4",
          "fps": 30.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 0,
          "has_drm": False,
          "width": 256,
          "height": 144,
          "vcodec": "avc1.4D400C",
          "acodec": "mp4a.40.5",
          "dynamic_range": "SDR",
          "available_at": 1782286467,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "91 - 256x144"
        },
        {
          "asr": None,
          "filesize": 860922,
          "format_id": "160",
          "format_note": "144p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 144,
          "quality": 0.0,
          "has_drm": False,
          "tbr": 54.985,
          "filesize_approx": 860913,
          "width": 256,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d400c",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=160&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=860922&dur=125.258&lmt=1744775415343276&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5535534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAL5sitCyoNSHoMKI5YFDyxOnZcRDsEi3vb-SdVqvevwmAiBViwgg1cYzrF0xvbmWmqUckshJVkpVuvRGNFqjxOW4uA%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 54.985,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "160 - 256x144 (144p)"
        },
        {
          "asr": None,
          "filesize": 1033282,
          "format_id": "278",
          "format_note": "144p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 144,
          "quality": 0.0,
          "has_drm": False,
          "tbr": 65.993,
          "filesize_approx": 1033268,
          "width": 256,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=278&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=1033282&dur=125.258&lmt=1748516373946526&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAIUR61iUy0Fc5h3KgdRu4isZzqSAQdUPKfBpGLjwYOxaAiEA_e2aFLgSN_B41WYtLWe2phLKLUnzf4wfAXBQeBj_z9Y%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 65.993,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "278 - 256x144 (144p)"
        },
        {
          "asr": None,
          "filesize": 925284,
          "format_id": "394",
          "format_note": "144p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 144,
          "quality": 0.0,
          "has_drm": False,
          "tbr": 59.096,
          "filesize_approx": 925280,
          "width": 256,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.00M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=394&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=925284&dur=125.258&lmt=1748514912080545&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgQL2npAEBy4I9YigRIGk1G6V0wkfHYZuXGocwDHxjHFECIFtfq6GMV3RPSRGY9yfZ1etk0fnDr7GmeXTdi76RtD6s&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 59.096,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "394 - 256x144 (144p)"
        },
        {
          "format_id": "92",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308066/ei/gog7asqjGrSLlu8PubmLoA0/ip/47.147.88.26/id/619c12cc662dbd68/itag/92/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D765910%3Bdur%3D125.387%3Bgir%3Dyes%3Bitag%3D139%3Blmt%3D1744772028521410/sgovp/clen%3D1701886%3Bdur%3D125.258%3Bgir%3Dyes%3Bitag%3D133%3Blmt%3D1744775414546145/rqh/1/hls_chunk_host/rr1---sn-a5mekn6k.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/402/met/1782286466,/mh/TV/mm/31,29/mn/sn-a5mekn6k,sn-a5mlrnll/ms/au,rdu/mv/m/mvi/1/pl/12/rms/au,au/initcwndbps/3750000/bui/ARmQxEUNzaIumqBOnNkHLhg-YrXPdXh-AkY7o-Xeng27qUb7ijfJITw3XQCSQE6IvvzeOULJd1ftLpNm/spc/SQ-umlGRvtBDE0KpGIo2tnD6N3qd7qRUOjet39gx0oeYzDb3NKEl6EabtFyapVElP-TMKHbj/vprv/1/ns/VLAX1wE0fzIm9Fad-RZ1PFwW/playlist_type/CLEAN/dover/11/txp/5535534/mt/1782285909/fvip/4/keepalive/yes/fexp/51565116,51565682,51987687/n/frLTt21veyP0UQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRgIhAOCGT8HY9jiTYiNyc_8_p3DPiGGqmsOKlazH18YM6EWEAiEAyRhkTJ63Vi-OMgh9KkiLpzHOFsmpiogV2wYYdj46fjY%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIgT4Aab9keS3SMHosUEyDKULtNm9zfMMtz6iltlziYB2kCIQC0BeSsM1-wmW4Qr9Hnae7l3EV90K0ZWa6jxJUNR9UR9Q%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308066/ei/gog7asqjGrSLlu8PubmLoA0/ip/47.147.88.26/id/619c12cc662dbd68/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr1---sn-a5mekn6k.googlevideo.com/cps/402/met/1782286466%2C/mh/TV/mm/31%2C29/mn/sn-a5mekn6k%2Csn-a5mlrnll/ms/au%2Crdu/mv/m/mvi/1/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3750000/bui/ARmQxEUNzaIumqBOnNkHLhg-YrXPdXh-AkY7o-Xeng27qUb7ijfJITw3XQCSQE6IvvzeOULJd1ftLpNm/spc/SQ-umlGRvtBDE0KpGIo2tnD6N3qd7qRUOjet39gx0oeYzDb3NKEl6EabtFyapVElP-TMKHbj/vprv/1/go/1/ns/VLAX1wE0fzIm9Fad-RZ1PFwW/rqh/5/mt/1782285909/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51987687/dover/11/n/frLTt21veyP0UQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRgIhAITp5QBJCzbUWidXDZ6ZEZa6u_-Xm0HkjE08BiefjnCaAiEA1bigj1nOX-Iyaa5l9FN5GnZVifUbn4JnXb4Y7yDjeJE%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIhAN8ZWFZj4YzVWLUJL1GB8Nu9nAdXNou742UamxSmuOakAiBVp0i1UBe89oJqN7oyWnzxQavtZEF1icgXFaC8e9faSQ%3D%3D/file/index.m3u8",
          "tbr": 232.794,
          "ext": "mp4",
          "fps": 30.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 5,
          "has_drm": False,
          "width": 426,
          "height": 240,
          "vcodec": "avc1.4D4015",
          "acodec": "mp4a.40.5",
          "dynamic_range": "SDR",
          "available_at": 1782286467,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "426x240",
          "aspect_ratio": 1.77,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "92 - 426x240"
        },
        {
          "asr": None,
          "filesize": 1701886,
          "format_id": "133",
          "format_note": "240p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 240,
          "quality": 5.0,
          "has_drm": False,
          "tbr": 108.696,
          "filesize_approx": 1701880,
          "width": 426,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d4015",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=133&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=1701886&dur=125.258&lmt=1744775414546145&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5535534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAOgiKVcUSfDMitw1LSalr3TspKXKyKPFKBUfdQsaMNxRAiB4IlX9aXpmXerDufg42Gakx9pn84FzxcgooscilV2kcg%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 108.696,
          "resolution": "426x240",
          "aspect_ratio": 1.77,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "133 - 426x240 (240p)"
        },
        {
          "asr": None,
          "filesize": 1711718,
          "format_id": "242",
          "format_note": "240p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 240,
          "quality": 5.0,
          "has_drm": False,
          "tbr": 109.324,
          "filesize_approx": 1711713,
          "width": 426,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=242&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=1711718&dur=125.258&lmt=1748516369121547&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhANibI1pf96tVzbD5TlHMNs3j0gdIKUedzZJsxYDDWJgFAiEAhBtF24cISAaUYMiwDYYk5H4V4bIA8V2r3K_77fNA7P0%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 109.324,
          "resolution": "426x240",
          "aspect_ratio": 1.77,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "242 - 426x240 (240p)"
        },
        {
          "asr": None,
          "filesize": 1413272,
          "format_id": "395",
          "format_note": "240p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 240,
          "quality": 5.0,
          "has_drm": False,
          "tbr": 90.263,
          "filesize_approx": 1413270,
          "width": 426,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.00M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=395&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=1413272&dur=125.258&lmt=1748515098607870&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAMeZyBY0syPVkRpMKlQnQhdjVyjYZ9zgFX4wE_Zs7iy8AiEAi1Irbh-UQKO2RyAZzl4-LjeBoJrciZVwo3n0RS3khPU%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 90.263,
          "resolution": "426x240",
          "aspect_ratio": 1.77,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "395 - 426x240 (240p)"
        },
        {
          "format_id": "93",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308066/ei/gog7asqjGrSLlu8PubmLoA0/ip/47.147.88.26/id/619c12cc662dbd68/itag/93/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2029119%3Bdur%3D125.318%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1744772028535485/sgovp/clen%3D3032748%3Bdur%3D125.258%3Bgir%3Dyes%3Bitag%3D134%3Blmt%3D1744775420966347/rqh/1/hls_chunk_host/rr1---sn-a5mekn6k.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/402/met/1782286466,/mh/TV/mm/31,29/mn/sn-a5mekn6k,sn-a5mlrnll/ms/au,rdu/mv/m/mvi/1/pl/12/rms/au,au/initcwndbps/3750000/bui/ARmQxEUNzaIumqBOnNkHLhg-YrXPdXh-AkY7o-Xeng27qUb7ijfJITw3XQCSQE6IvvzeOULJd1ftLpNm/spc/SQ-umlGRvtBDE0KpGIo2tnD6N3qd7qRUOjet39gx0oeYzDb3NKEl6EabtFyapVElP-TMKHbj/vprv/1/ns/VLAX1wE0fzIm9Fad-RZ1PFwW/playlist_type/CLEAN/dover/11/txp/5535534/mt/1782285909/fvip/4/keepalive/yes/fexp/51565116,51565682,51987687/n/frLTt21veyP0UQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRQIgcaMyFOi4q3lpfYkLmyRmzp4MMX5wwP2aZUGnICsnrbsCIQDagg8g5F9EmCBsfBTnUkaaXPZGv7ffxnUhp0zq1-K3rw%3D%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIhAJqPu8-9GwSM3xYc_IdQNFsjxfP-FEIAUK5jnm5r1WF0AiARCa434Ux1UagpM7Xzj77zdbQborjZfVPXkNMPW5ExJQ%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308066/ei/gog7asqjGrSLlu8PubmLoA0/ip/47.147.88.26/id/619c12cc662dbd68/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr1---sn-a5mekn6k.googlevideo.com/cps/402/met/1782286466%2C/mh/TV/mm/31%2C29/mn/sn-a5mekn6k%2Csn-a5mlrnll/ms/au%2Crdu/mv/m/mvi/1/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3750000/bui/ARmQxEUNzaIumqBOnNkHLhg-YrXPdXh-AkY7o-Xeng27qUb7ijfJITw3XQCSQE6IvvzeOULJd1ftLpNm/spc/SQ-umlGRvtBDE0KpGIo2tnD6N3qd7qRUOjet39gx0oeYzDb3NKEl6EabtFyapVElP-TMKHbj/vprv/1/go/1/ns/VLAX1wE0fzIm9Fad-RZ1PFwW/rqh/5/mt/1782285909/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51987687/dover/11/n/frLTt21veyP0UQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRgIhAITp5QBJCzbUWidXDZ6ZEZa6u_-Xm0HkjE08BiefjnCaAiEA1bigj1nOX-Iyaa5l9FN5GnZVifUbn4JnXb4Y7yDjeJE%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIhAN8ZWFZj4YzVWLUJL1GB8Nu9nAdXNou742UamxSmuOakAiBVp0i1UBe89oJqN7oyWnzxQavtZEF1icgXFaC8e9faSQ%3D%3D/file/index.m3u8",
          "tbr": 470.855,
          "ext": "mp4",
          "fps": 30.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 6,
          "has_drm": False,
          "width": 640,
          "height": 360,
          "vcodec": "avc1.4D401E",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286467,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "93 - 640x360"
        },
        {
          "asr": None,
          "filesize": 3032748,
          "format_id": "134",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 193.696,
          "filesize_approx": 3032746,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d401e",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=134&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=3032748&dur=125.258&lmt=1744775420966347&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5535534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgYATrfOTFhItnMCYGzrTr93A3Ou9NG5EAsP5ccs5qgSMCIQCtJime370wpHr-i6f5k-eyOqYSJF5gDoiFgSOf-ZFJ2Q%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 193.696,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "134 - 640x360 (360p)"
        },
        {
          "asr": 44100,
          "filesize": None,
          "format_id": "18",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": 2,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 322.758,
          "filesize_approx": 5055923,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.42001E",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEVQPz1at2bjMBehoKQvTp3h3dBnoTo6TScC0_-EHxpvpQzVVk8hCrmUJti7G4ldABUoS65FkZSO&spc=SQ-umiOhaPSnk53eCSn7k6nAwCBFADvS-hsc9aldjLpUIBDaZmxW&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&cnr=14&ratebypass=yes&dur=125.318&lmt=1744775425034085&mt=1782286149&fvip=2&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5538534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AHEqNM4wRAIgHxinCLsFLBc8DNboFiFLFx8m58jQu-2wZYDUZv7LVwsCIHYx_44VV0YdayT5ZoaxS30VEl2MahNxysLi0dw2wgY1&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "18 - 640x360 (360p)"
        },
        {
          "asr": None,
          "filesize": 3662220,
          "format_id": "243",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 233.899,
          "filesize_approx": 3662215,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=243&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=3662220&dur=125.258&lmt=1748516370282045&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgJ6paxQKRzOpT82nI0gZ9Qh-VsIdHDPuaFFotfr6GEKgCIQDibI8xoywGVSEwx7uUWSI7MCjgiLBqdMeArHZE5bzHyg%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 233.899,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "243 - 640x360 (360p)"
        },
        {
          "asr": None,
          "filesize": 2826408,
          "format_id": "396",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 180.517,
          "filesize_approx": 2826399,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.01M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=396&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=2826408&dur=125.258&lmt=1748516377911831&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgFmSoCOBCm_IjY1Iwhpu8wExztLEKkGfFpVwf5ip4of8CIEDTHim3_qOGBos1iuf1T34i3hgByYl_0fRtJu6MNko-&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 180.517,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "396 - 640x360 (360p)"
        },
        {
          "format_id": "94",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308066/ei/gog7asqjGrSLlu8PubmLoA0/ip/47.147.88.26/id/619c12cc662dbd68/itag/94/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2029119%3Bdur%3D125.318%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1744772028535485/sgovp/clen%3D4745939%3Bdur%3D125.258%3Bgir%3Dyes%3Bitag%3D135%3Blmt%3D1744775426707191/rqh/1/hls_chunk_host/rr1---sn-a5mekn6k.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/402/met/1782286466,/mh/TV/mm/31,29/mn/sn-a5mekn6k,sn-a5mlrnll/ms/au,rdu/mv/m/mvi/1/pl/12/rms/au,au/initcwndbps/3750000/bui/ARmQxEUNzaIumqBOnNkHLhg-YrXPdXh-AkY7o-Xeng27qUb7ijfJITw3XQCSQE6IvvzeOULJd1ftLpNm/spc/SQ-umlGRvtBDE0KpGIo2tnD6N3qd7qRUOjet39gx0oeYzDb3NKEl6EabtFyapVElP-TMKHbj/vprv/1/ns/VLAX1wE0fzIm9Fad-RZ1PFwW/playlist_type/CLEAN/dover/11/txp/5535534/mt/1782285909/fvip/4/keepalive/yes/fexp/51565116,51565682,51987687/n/frLTt21veyP0UQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRQIgNakVP0juwshIzFsFbf1OWUIhor6LWVAHnByMBOexK-QCIQD7KsaiWpOCzOdBQuSpFXea9b8XEcNd2ZSg4KBMV-WJ1w%3D%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIhAMzOYEkCE5I761XfZzEgH4tEmowxP4BQw1SDN45aWywzAiBoSegR-1G1B5h4A78WkJWUr5h-5N5CKntqoNdYwmicHQ%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308066/ei/gog7asqjGrSLlu8PubmLoA0/ip/47.147.88.26/id/619c12cc662dbd68/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr1---sn-a5mekn6k.googlevideo.com/cps/402/met/1782286466%2C/mh/TV/mm/31%2C29/mn/sn-a5mekn6k%2Csn-a5mlrnll/ms/au%2Crdu/mv/m/mvi/1/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3750000/bui/ARmQxEUNzaIumqBOnNkHLhg-YrXPdXh-AkY7o-Xeng27qUb7ijfJITw3XQCSQE6IvvzeOULJd1ftLpNm/spc/SQ-umlGRvtBDE0KpGIo2tnD6N3qd7qRUOjet39gx0oeYzDb3NKEl6EabtFyapVElP-TMKHbj/vprv/1/go/1/ns/VLAX1wE0fzIm9Fad-RZ1PFwW/rqh/5/mt/1782285909/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51987687/dover/11/n/frLTt21veyP0UQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRgIhAITp5QBJCzbUWidXDZ6ZEZa6u_-Xm0HkjE08BiefjnCaAiEA1bigj1nOX-Iyaa5l9FN5GnZVifUbn4JnXb4Y7yDjeJE%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIhAN8ZWFZj4YzVWLUJL1GB8Nu9nAdXNou742UamxSmuOakAiBVp0i1UBe89oJqN7oyWnzxQavtZEF1icgXFaC8e9faSQ%3D%3D/file/index.m3u8",
          "tbr": 823.231,
          "ext": "mp4",
          "fps": 30.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 7,
          "has_drm": False,
          "width": 854,
          "height": 480,
          "vcodec": "avc1.4D401F",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286467,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "854x480",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "94 - 854x480"
        },
        {
          "asr": None,
          "filesize": 4745939,
          "format_id": "135",
          "format_note": "480p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 480,
          "quality": 7.0,
          "has_drm": False,
          "tbr": 303.114,
          "filesize_approx": 4745931,
          "width": 854,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d401f",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=135&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=4745939&dur=125.258&lmt=1744775426707191&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5535534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgW0aZV-dgLmU4xRr4mJOxKVOKTcCEpKhVU7qILJVDayACIQDOy_89zvS-H3EnTUKXnkt7e9417HRwSS9Fy8LHb1RiWQ%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 303.114,
          "resolution": "854x480",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "135 - 854x480 (480p)"
        },
        {
          "asr": None,
          "filesize": 5158671,
          "format_id": "244",
          "format_note": "480p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 480,
          "quality": 7.0,
          "has_drm": False,
          "tbr": 329.474,
          "filesize_approx": 5158656,
          "width": 854,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=244&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=5158671&dur=125.258&lmt=1748516370490119&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAJQKtoHyrQTZLUgUx-M4b2-cqCbXnFeQJ35JHKw9sadFAiEAyg1GCUNH58Z4_H8ugU9nmAwEj2n52vn7T3UU5Q_ovO0%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 329.474,
          "resolution": "854x480",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "244 - 854x480 (480p)"
        },
        {
          "asr": None,
          "filesize": 4689253,
          "format_id": "397",
          "format_note": "480p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 480,
          "quality": 7.0,
          "has_drm": False,
          "tbr": 299.494,
          "filesize_approx": 4689252,
          "width": 854,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.04M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=397&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=4689253&dur=125.258&lmt=1748516564497809&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAPSc3D4qkA8hFdr-IkXvgMY8zahNO1AVMPF86D6nVlDiAiEAzTr978Rw6sAYk5zGn9xPI2RfWuoe0LOU5NwHRa_KCEQ%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 299.494,
          "resolution": "854x480",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "397 - 854x480 (480p)"
        },
        {
          "format_id": "95",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308066/ei/gog7asqjGrSLlu8PubmLoA0/ip/47.147.88.26/id/619c12cc662dbd68/itag/95/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2029119%3Bdur%3D125.318%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1744772028535485/sgovp/clen%3D8320654%3Bdur%3D125.258%3Bgir%3Dyes%3Bitag%3D136%3Blmt%3D1744775415069950/rqh/1/hls_chunk_host/rr1---sn-a5mekn6k.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/402/met/1782286466,/mh/TV/mm/31,29/mn/sn-a5mekn6k,sn-a5mlrnll/ms/au,rdu/mv/m/mvi/1/pl/12/rms/au,au/initcwndbps/3750000/bui/ARmQxEUNzaIumqBOnNkHLhg-YrXPdXh-AkY7o-Xeng27qUb7ijfJITw3XQCSQE6IvvzeOULJd1ftLpNm/spc/SQ-umlGRvtBDE0KpGIo2tnD6N3qd7qRUOjet39gx0oeYzDb3NKEl6EabtFyapVElP-TMKHbj/vprv/1/ns/VLAX1wE0fzIm9Fad-RZ1PFwW/playlist_type/CLEAN/dover/11/txp/5535534/mt/1782285909/fvip/4/keepalive/yes/fexp/51565116,51565682,51987687/n/frLTt21veyP0UQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRQIhAJHA9NIzNfhAvFOakBPaxrhy6s58ce8b9mEpbrwHbaGmAiBUn-s_C2a_u5bBIykQMI1ES6T25EWhVjRYMTj-Go8sCg%3D%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIhAKbsdYAJ6jf6OPziw9m4pvEXGb_WEImQTZ_ZWjLnmmHeAiBXEggoWjc3woxq66NYWiD9vWzwbtD0hPgxFQtvoxWgFw%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308066/ei/gog7asqjGrSLlu8PubmLoA0/ip/47.147.88.26/id/619c12cc662dbd68/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr1---sn-a5mekn6k.googlevideo.com/cps/402/met/1782286466%2C/mh/TV/mm/31%2C29/mn/sn-a5mekn6k%2Csn-a5mlrnll/ms/au%2Crdu/mv/m/mvi/1/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3750000/bui/ARmQxEUNzaIumqBOnNkHLhg-YrXPdXh-AkY7o-Xeng27qUb7ijfJITw3XQCSQE6IvvzeOULJd1ftLpNm/spc/SQ-umlGRvtBDE0KpGIo2tnD6N3qd7qRUOjet39gx0oeYzDb3NKEl6EabtFyapVElP-TMKHbj/vprv/1/go/1/ns/VLAX1wE0fzIm9Fad-RZ1PFwW/rqh/5/mt/1782285909/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51987687/dover/11/n/frLTt21veyP0UQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRgIhAITp5QBJCzbUWidXDZ6ZEZa6u_-Xm0HkjE08BiefjnCaAiEA1bigj1nOX-Iyaa5l9FN5GnZVifUbn4JnXb4Y7yDjeJE%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIhAN8ZWFZj4YzVWLUJL1GB8Nu9nAdXNou742UamxSmuOakAiBVp0i1UBe89oJqN7oyWnzxQavtZEF1icgXFaC8e9faSQ%3D%3D/file/index.m3u8",
          "tbr": 1387.682,
          "ext": "mp4",
          "fps": 30.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 8,
          "has_drm": False,
          "width": 1280,
          "height": 720,
          "vcodec": "avc1.4D401F",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286467,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "95 - 1280x720"
        },
        {
          "asr": None,
          "filesize": 8320654,
          "format_id": "136",
          "format_note": "720p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 720,
          "quality": 8.0,
          "has_drm": False,
          "tbr": 531.424,
          "filesize_approx": 8320638,
          "width": 1280,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d401f",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=136&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=8320654&dur=125.258&lmt=1744775415069950&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5535534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAJRCDjTIwZm1xVLjECzwmTV13z7Cfg53EXfzB8n4Q9pSAiEAxqNZWuuYoqo-EXfw2imR1W3fZ_rLYwjcnuc4r-Zb93Y%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 531.424,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "136 - 1280x720 (720p)"
        },
        {
          "asr": None,
          "filesize": 9367798,
          "format_id": "247",
          "format_note": "720p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 720,
          "quality": 8.0,
          "has_drm": False,
          "tbr": 598.304,
          "filesize_approx": 9367795,
          "width": 1280,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=247&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=9367798&dur=125.258&lmt=1748516369806321&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAOxr2UaVqKx50IUZSvMu4mObHb1G_DPP0TVkDUL30ZwyAiEAkDX-l4_P3g4eEtn1R79zYXb-58qr-EjZpCdhCOoaYs8%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 598.304,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "247 - 1280x720 (720p)"
        },
        {
          "asr": None,
          "filesize": 8942261,
          "format_id": "398",
          "format_note": "720p",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 720,
          "quality": 8.0,
          "has_drm": False,
          "tbr": 571.125,
          "filesize_approx": 8942246,
          "width": 1280,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.05M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=398&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=8942261&dur=125.258&lmt=1748515660362274&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgUGzC9pNMywvFA09t2GC2sGeXhIo4b0eINRBEpC4l8DECIQC5GpHjlCACjrxCIZfcNL4sI8s_j5ECnlDu7PRxH1GCxQ%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 571.125,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "398 - 1280x720 (720p)"
        },
        {
          "asr": None,
          "filesize": 20429106,
          "format_id": "248-sr",
          "format_note": "1080p, AI-upscaled",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 1080,
          "quality": 9.0,
          "has_drm": False,
          "tbr": 1304.769,
          "filesize_approx": 20429094,
          "width": 1920,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=248&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&xtags=sr%3D1&mime=video%2Fwebm&rqh=1&gir=yes&clen=20429106&dur=125.258&lmt=1748701701741565&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cxtags%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhALB8x2yNSwaFHbcSVf5Ooh7vsmwk4CqcRegl7aKYXdOIAiAtgh8jM1E49O4rAinsHC4Lr703GgHovvc_0x7WqgYW_g%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 1304.769,
          "resolution": "1920x1080",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "248-sr - 1920x1080 (1080p, AI-upscaled)"
        },
        {
          "asr": None,
          "filesize": 18576610,
          "format_id": "399-sr",
          "format_note": "1080p, AI-upscaled",
          "source_preference": -1,
          "fps": 30,
          "audio_channels": None,
          "height": 1080,
          "quality": 9.0,
          "has_drm": False,
          "tbr": 1186.454,
          "filesize_approx": 18576606,
          "width": 1920,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.08M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr1---sn-a5mekn6k.googlevideo.com/videoplayback?expire=1782308067&ei=g4g7apmwEa2csfIP5LfFmAk&ip=47.147.88.26&id=o-AKJ2bpynvM6FC2nZC3zYBgPU6psH5BV9xMIShIk1cLgI&itag=399&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=392&met=1782286467%2C&mh=TV&mm=31%2C26&mn=sn-a5mekn6k%2Csn-vgqsrn67&ms=au%2Conr&mv=m&mvi=1&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX-oVuXqh8Sh0UsWbTW14IdmDTMQ8Os659P9WWRMZHUrbr4U8cwoBpHwLyhnATuxNbp-7n42Moa&spc=SQ-umgmoUvGVm5_mISi5q4HdgiUlHKHSqhd-5SBEjpJf&vprv=1&svpuc=1&xtags=sr%3D1&mime=video%2Fmp4&rqh=1&gir=yes&clen=18576610&dur=125.258&lmt=1748702725226637&mt=1782286149&fvip=2&keepalive=yes&fexp=51565116%2C51565682%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cxtags%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAMZz7EF3iijxvO-X57Mtvd_s34QXFX_DPuescveLvaVcAiEAtQa88p-xBJvcKWM7KJ5_fGxVH1gAwb6fHy-CTiNYBVE%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgU_2oqV7s7pdKcZJp5Mfz1o_R4hkuk_00oWEz-zUTKNwCIAY4TP8mNx8kUS28ayOtiYb6sQ6Ph64Tlivxy6kXQrz9",
          "available_at": 1782286467,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 1186.454,
          "resolution": "1920x1080",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "399-sr - 1920x1080 (1080p, AI-upscaled)"
        }
      ],
      "thumbnail": "https://i.ytimg.com/vi/YZwSzGYtvWg/maxresdefault.jpg",
      "average_rating": None,
      "age_limit": 0,
      "webpage_url": "https://www.youtube.com/watch?v=YZwSzGYtvWg",
      "categories": ["Music"],
      "tags": [
        "gawr gura",
        "when I'm gone",
        "senzawa when I'm gone",
        "gura when I'm gone",
        "baby shark",
        "anime vtuber",
        "hololive",
        "hololive english",
        "gura karaoke",
        "gura singing",
        "gura you're gonna miss me",
        "gura a",
        "gura clips",
        "hololive english 2nd gen",
        "hololive auditions",
        "hololive en 2nd gen debut",
        "mori calliope",
        "amelia watson",
        "ninomae inanis",
        "takanashi kiara",
        "gura song",
        "gura collab",
        "gura sad",
        "gura cry",
        "dloow",
        "sashimi hololive",
        "sushi hololive",
        "gavr gurach"
      ],
      "playable_in_embed": True,
      "media_type": "video",
      "_format_sort_fields": [
        "quality",
        "res",
        "fps",
        "hdr:12",
        "source",
        "vcodec",
        "channels",
        "acodec",
        "lang",
        "proto"
      ],
      "automatic_captions": {},
      "subtitles": {},
      "comment_count": 14000,
      "chapters": None,
      "heatmap": [
        { "start_time": 0.0, "end_time": 1.26, "value": 0.01276570600046755 },
        { "start_time": 1.26, "end_time": 2.52, "value": 0.0 },
        { "start_time": 2.52, "end_time": 3.78, "value": 0.04341459793576855 },
        { "start_time": 3.78, "end_time": 5.04, "value": 0.07759743461242018 },
        { "start_time": 5.04, "end_time": 6.3, "value": 0.10570789873026905 },
        { "start_time": 6.3, "end_time": 7.56, "value": 0.10902454040068116 },
        { "start_time": 7.56, "end_time": 8.82, "value": 0.1166327330662224 },
        { "start_time": 8.82, "end_time": 10.08, "value": 0.1261549949976715 },
        {
          "start_time": 10.08,
          "end_time": 11.34,
          "value": 0.12332975962602008
        },
        { "start_time": 11.34, "end_time": 12.6, "value": 0.12351729616480761 },
        { "start_time": 12.6, "end_time": 13.86, "value": 0.12386046070171461 },
        {
          "start_time": 13.86,
          "end_time": 15.12,
          "value": 0.11993748289624664
        },
        {
          "start_time": 15.12,
          "end_time": 16.38,
          "value": 0.12708447896935413
        },
        {
          "start_time": 16.38,
          "end_time": 17.64,
          "value": 0.13504012018883652
        },
        { "start_time": 17.64, "end_time": 18.9, "value": 0.14233779548176542 },
        { "start_time": 18.9, "end_time": 20.16, "value": 0.15069450933047832 },
        {
          "start_time": 20.16,
          "end_time": 21.42,
          "value": 0.15413516590779244
        },
        {
          "start_time": 21.42,
          "end_time": 22.68,
          "value": 0.15876190430466156
        },
        {
          "start_time": 22.68,
          "end_time": 23.94,
          "value": 0.16732055785288022
        },
        { "start_time": 23.94, "end_time": 25.2, "value": 0.17821030756657122 },
        { "start_time": 25.2, "end_time": 26.46, "value": 0.18749458496553767 },
        {
          "start_time": 26.46,
          "end_time": 27.72,
          "value": 0.19811673133932037
        },
        { "start_time": 27.72, "end_time": 28.98, "value": 0.208793683586195 },
        { "start_time": 28.98, "end_time": 30.24, "value": 0.2227209491018152 },
        { "start_time": 30.24, "end_time": 31.5, "value": 0.22929115398492986 },
        { "start_time": 31.5, "end_time": 32.76, "value": 0.22885086044112818 },
        {
          "start_time": 32.76,
          "end_time": 34.02,
          "value": 0.23255446702950322
        },
        {
          "start_time": 34.02,
          "end_time": 35.28,
          "value": 0.24216263088872303
        },
        {
          "start_time": 35.28,
          "end_time": 36.54,
          "value": 0.24796488878728712
        },
        { "start_time": 36.54, "end_time": 37.8, "value": 0.2583371587881993 },
        { "start_time": 37.8, "end_time": 39.06, "value": 0.2659149940226883 },
        { "start_time": 39.06, "end_time": 40.32, "value": 0.2642106200043653 },
        { "start_time": 40.32, "end_time": 41.58, "value": 0.2610014480716199 },
        { "start_time": 41.58, "end_time": 42.84, "value": 0.2626598058380073 },
        { "start_time": 42.84, "end_time": 44.1, "value": 0.2665748803706709 },
        { "start_time": 44.1, "end_time": 45.36, "value": 0.2689641800779174 },
        { "start_time": 45.36, "end_time": 46.62, "value": 0.2696854460492684 },
        { "start_time": 46.62, "end_time": 47.88, "value": 0.2732106011694628 },
        {
          "start_time": 47.88,
          "end_time": 49.14,
          "value": 0.28432511405272076
        },
        { "start_time": 49.14, "end_time": 50.4, "value": 0.2946986397137981 },
        { "start_time": 50.4, "end_time": 51.66, "value": 0.31563123329094867 },
        { "start_time": 51.66, "end_time": 52.92, "value": 0.344894024128618 },
        { "start_time": 52.92, "end_time": 54.18, "value": 0.3782106768783845 },
        {
          "start_time": 54.18,
          "end_time": 55.44,
          "value": 0.39247423773118456
        },
        { "start_time": 55.44, "end_time": 56.7, "value": 0.41002127605356353 },
        { "start_time": 56.7, "end_time": 57.96, "value": 0.4282264280272212 },
        {
          "start_time": 57.96,
          "end_time": 59.22,
          "value": 0.44923229306812806
        },
        { "start_time": 59.22, "end_time": 60.48, "value": 0.458472031462412 },
        {
          "start_time": 60.48,
          "end_time": 61.74,
          "value": 0.45709833924170684
        },
        { "start_time": 61.74, "end_time": 63.0, "value": 0.4521377429656256 },
        { "start_time": 63.0, "end_time": 64.26, "value": 0.4499133040518307 },
        { "start_time": 64.26, "end_time": 65.52, "value": 0.4526925970339091 },
        {
          "start_time": 65.52,
          "end_time": 66.78,
          "value": 0.45657642778716856
        },
        {
          "start_time": 66.78,
          "end_time": 68.04,
          "value": 0.46992749301169723
        },
        { "start_time": 68.04, "end_time": 69.3, "value": 0.4783814835920301 },
        { "start_time": 69.3, "end_time": 70.56, "value": 0.49201041902487647 },
        { "start_time": 70.56, "end_time": 71.82, "value": 0.5036481728852006 },
        { "start_time": 71.82, "end_time": 73.08, "value": 0.5157005900494841 },
        { "start_time": 73.08, "end_time": 74.34, "value": 0.5193724358219164 },
        { "start_time": 74.34, "end_time": 75.6, "value": 0.5149892954970918 },
        { "start_time": 75.6, "end_time": 76.86, "value": 0.5036261619011286 },
        { "start_time": 76.86, "end_time": 78.12, "value": 0.5042263674600839 },
        { "start_time": 78.12, "end_time": 79.38, "value": 0.5027086436321965 },
        { "start_time": 79.38, "end_time": 80.64, "value": 0.5022456743430589 },
        { "start_time": 80.64, "end_time": 81.9, "value": 0.5044582952788286 },
        { "start_time": 81.9, "end_time": 83.16, "value": 0.5175858529939554 },
        { "start_time": 83.16, "end_time": 84.42, "value": 0.5248958633014482 },
        { "start_time": 84.42, "end_time": 85.68, "value": 0.5283786214254771 },
        { "start_time": 85.68, "end_time": 86.94, "value": 0.5340103311286649 },
        { "start_time": 86.94, "end_time": 88.2, "value": 0.5417354479142931 },
        { "start_time": 88.2, "end_time": 89.46, "value": 0.5501344848968087 },
        { "start_time": 89.46, "end_time": 90.72, "value": 0.5570496270135342 },
        { "start_time": 90.72, "end_time": 91.98, "value": 0.565461368322427 },
        { "start_time": 91.98, "end_time": 93.24, "value": 0.5760192544406976 },
        { "start_time": 93.24, "end_time": 94.5, "value": 0.5649224685244775 },
        { "start_time": 94.5, "end_time": 95.76, "value": 0.563618059199945 },
        { "start_time": 95.76, "end_time": 97.02, "value": 0.5681255837434849 },
        { "start_time": 97.02, "end_time": 98.28, "value": 0.5727208567738619 },
        { "start_time": 98.28, "end_time": 99.54, "value": 0.5787644230112282 },
        { "start_time": 99.54, "end_time": 100.8, "value": 0.5866913317716368 },
        {
          "start_time": 100.8,
          "end_time": 102.06,
          "value": 0.5911096305810862
        },
        { "start_time": 102.06, "end_time": 103.32, "value": 0.59507751670305 },
        {
          "start_time": 103.32,
          "end_time": 104.58,
          "value": 0.5931576861728549
        },
        {
          "start_time": 104.58,
          "end_time": 105.84,
          "value": 0.5896195312768329
        },
        {
          "start_time": 105.84,
          "end_time": 107.1,
          "value": 0.5888026135458403
        },
        {
          "start_time": 107.1,
          "end_time": 108.36,
          "value": 0.5899836727247345
        },
        {
          "start_time": 108.36,
          "end_time": 109.62,
          "value": 0.5911830497695679
        },
        {
          "start_time": 109.62,
          "end_time": 110.88,
          "value": 0.5917769031653346
        },
        {
          "start_time": 110.88,
          "end_time": 112.14,
          "value": 0.6001066572516776
        },
        {
          "start_time": 112.14,
          "end_time": 113.4,
          "value": 0.6262232068895858
        },
        {
          "start_time": 113.4,
          "end_time": 114.66,
          "value": 0.6575489735162806
        },
        {
          "start_time": 114.66,
          "end_time": 115.92,
          "value": 0.6828548098616595
        },
        {
          "start_time": 115.92,
          "end_time": 117.18,
          "value": 0.7115758941315984
        },
        {
          "start_time": 117.18,
          "end_time": 118.44,
          "value": 0.7486410617862357
        },
        {
          "start_time": 118.44,
          "end_time": 119.7,
          "value": 0.7910986250890503
        },
        {
          "start_time": 119.7,
          "end_time": 120.96,
          "value": 0.8398454208474303
        },
        {
          "start_time": 120.96,
          "end_time": 122.22,
          "value": 0.8883156759200204
        },
        {
          "start_time": 122.22,
          "end_time": 123.48,
          "value": 0.9352563891866978
        },
        {
          "start_time": 123.48,
          "end_time": 124.74,
          "value": 0.9765492907551282
        },
        { "start_time": 124.74, "end_time": 126.0, "value": 1.0 }
      ],
      "like_count": 193432,
      "channel_follower_count": 135000,
      "creators": None,
      "upload_date": "20210213",
      "__post_extractor": None,
      "original_url": "YZwSzGYtvWg",
      "webpage_url_basename": "watch",
      "webpage_url_domain": "youtube.com",
      "extractor": "youtube",
      "extractor_key": "Youtube",
      "display_id": "YZwSzGYtvWg",
      "fulltitle": "Gawr Gura - When I'm Gone",
      "duration_string": "2:05",
      "release_year": None,
      "is_live": False,
      "was_live": False,
      "requested_subtitles": None,
      "_has_drm": None,
      "epoch": 1782286468
    },
    {
    'playlist_count':               1,
    'playlist_title':               '',
    'playlist_channel_id':          '',
    'playlist_webpage_url':         '',
    'n_entries':                    1,
    'playlist_autonumber':          1,
    'playlist':                     '',
    'playlist_channel':             '',
    'playlist_id':                  '',
    'playlist_uploader':            '',
    'playlist_uploader_id':         '',
    'playlist_index':               1,
      "_type": "url",
      "ie_key": "Youtube",
      "id": "7lVS5Ugo47s",
      "url": "https://www.youtube.com/watch?v=7lVS5Ugo47s",
      "title": "When I'm Gone - Gura x Senzawa Cover Duet",
      "description": "Amazing how those two individual VTubers \"\ud83d\ude09\" are so on spot!\nSame voice, different body: @SamekoSaba You're welcome :3  \n\nSource clips:\nhttps://www.youtube.com/watch?v=cP3eChqUphA\nhttps://www.youtube.com/watch?v=EoA5PaApyC0\n\nOriginal song: Cups - Anna Kendrick\nCover by: Gawr Gura & Senzawa\n\nThumbnail:\nGura: https://www.reddit.com/r/Hololive/comments/j3hpo5/fanart_gawrgura_by_me/\n\n0:00 Gura talks\n0:34 Singing\n2:26 Senzawa talks",
      "duration": 155,
      "channel_id": "UCzBjh5e90GSIFxweeb85ddQ",
      "channel": "marsini",
      "channel_url": "https://www.youtube.com/channel/UCzBjh5e90GSIFxweeb85ddQ",
      "uploader": "marsini",
      "uploader_id": "@marsini",
      "uploader_url": "https://www.youtube.com/@marsini",
      "thumbnails": [
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/3.jpg",
          "preference": -37,
          "id": "0"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/3.webp",
          "preference": -36,
          "id": "1"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/2.jpg",
          "preference": -35,
          "id": "2"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/2.webp",
          "preference": -34,
          "id": "3"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/1.jpg",
          "preference": -33,
          "id": "4"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/1.webp",
          "preference": -32,
          "id": "5"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/mq3.jpg",
          "preference": -31,
          "id": "6"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/mq3.webp",
          "preference": -30,
          "id": "7"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/mq2.jpg",
          "preference": -29,
          "id": "8"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/mq2.webp",
          "preference": -28,
          "id": "9"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/mq1.jpg",
          "preference": -27,
          "id": "10"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/mq1.webp",
          "preference": -26,
          "id": "11"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hq3.jpg",
          "preference": -25,
          "id": "12"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/hq3.webp",
          "preference": -24,
          "id": "13"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hq2.jpg",
          "preference": -23,
          "id": "14"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/hq2.webp",
          "preference": -22,
          "id": "15"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hq1.jpg",
          "preference": -21,
          "id": "16"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/hq1.webp",
          "preference": -20,
          "id": "17"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/sd3.jpg",
          "preference": -19,
          "id": "18"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/sd3.webp",
          "preference": -18,
          "id": "19"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/sd2.jpg",
          "preference": -17,
          "id": "20"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/sd2.webp",
          "preference": -16,
          "id": "21"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/sd1.jpg",
          "preference": -15,
          "id": "22"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/sd1.webp",
          "preference": -14,
          "id": "23"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/default.jpg",
          "height": 90,
          "width": 120,
          "preference": -13,
          "id": "24",
          "resolution": "120x90"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/default.webp",
          "preference": -12,
          "id": "25"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/mqdefault.jpg",
          "height": 180,
          "width": 320,
          "preference": -11,
          "id": "26",
          "resolution": "320x180"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/mqdefault.webp",
          "preference": -10,
          "id": "27"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/0.jpg",
          "preference": -9,
          "id": "28"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/0.webp",
          "preference": -8,
          "id": "29"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hqdefault.jpg?sqp=-oaymwEiCKgBEF5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4CLCkzEAFvZHAl3rjk7Dw-6RdLrkhgA",
          "height": 94,
          "width": 168,
          "preference": -7,
          "id": "30",
          "resolution": "168x94"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hqdefault.jpg?sqp=-oaymwEiCMQBEG5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4CLAKqyCivFSl0WoHo708E6_kvS7b6w",
          "height": 110,
          "width": 196,
          "preference": -7,
          "id": "31",
          "resolution": "196x110"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hqdefault.jpg?sqp=-oaymwEjCPYBEIoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLDT-sChDUCnqFkw80S4GqLmARicEw",
          "height": 138,
          "width": 246,
          "preference": -7,
          "id": "32",
          "resolution": "246x138"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hqdefault.jpg?sqp=-oaymwEjCNACELwBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLA8uuhF8JVh3tACUk_DpqPdUla9DQ",
          "height": 188,
          "width": 336,
          "preference": -7,
          "id": "33",
          "resolution": "336x188"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hqdefault.jpg",
          "height": 360,
          "width": 480,
          "preference": -7,
          "id": "34",
          "resolution": "480x360"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/hqdefault.webp",
          "preference": -6,
          "id": "35"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/sddefault.jpg",
          "height": 480,
          "width": 640,
          "preference": -5,
          "id": "36",
          "resolution": "640x480"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/sddefault.webp",
          "preference": -4,
          "id": "37"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/hq720.jpg",
          "preference": -3,
          "id": "38"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/hq720.webp",
          "preference": -2,
          "id": "39"
        },
        {
          "url": "https://i.ytimg.com/vi/7lVS5Ugo47s/maxresdefault.jpg",
          "height": 1080,
          "width": 1920,
          "preference": -1,
          "id": "40",
          "resolution": "1920x1080"
        },
        {
          "url": "https://i.ytimg.com/vi_webp/7lVS5Ugo47s/maxresdefault.webp",
          "preference": 0,
          "id": "41"
        }
      ],
      "timestamp": 1618720941,
      "release_timestamp": None,
      "availability": "public",
      "view_count": 1821516,
      "live_status": "not_live",
      "channel_is_verified": None,
      "__x_forwarded_for_ip": None,
      "playlist": None,
      "playlist_id": "PLXOfMLBzXbbVV8P-wQyZ9MAKxFsGy5v0b",
      "playlist_index": None,
      "playlist_uploader": "Some Random User",
      "playlist_uploader_id": "@somerandomuser8005",
      "playlist_channel": "Some Random User",
      "formats": [
        {
          "format_id": "sb2",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L0/default.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLDfjLTwZbhYgE5At-BfKGTC562rOQ",
          "width": 48,
          "height": 27,
          "fps": 0.6451612903225806,
          "rows": 10,
          "columns": 10,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L0/default.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLDfjLTwZbhYgE5At-BfKGTC562rOQ",
              "duration": 155.0
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "48x27",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb2 - 48x27 (storyboard)"
        },
        {
          "format_id": "sb1",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L1/M$M.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLD6IPGBx5vJqZCH5xsdvbEVa9Zgaw",
          "width": 80,
          "height": 45,
          "fps": 0.5096774193548387,
          "rows": 10,
          "columns": 10,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L1/M0.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLD6IPGBx5vJqZCH5xsdvbEVa9Zgaw",
              "duration": 155.0
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "80x45",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb1 - 80x45 (storyboard)"
        },
        {
          "format_id": "sb0",
          "format_note": "storyboard",
          "ext": "mhtml",
          "protocol": "mhtml",
          "acodec": "none",
          "vcodec": "none",
          "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L2/M$M.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLBkyf25PeVl7hlEW6gioFZfoIm8vQ",
          "width": 160,
          "height": 90,
          "fps": 0.5096774193548387,
          "rows": 5,
          "columns": 5,
          "fragments": [
            {
              "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L2/M0.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLBkyf25PeVl7hlEW6gioFZfoIm8vQ",
              "duration": 49.050632911392405
            },
            {
              "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L2/M1.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLBkyf25PeVl7hlEW6gioFZfoIm8vQ",
              "duration": 49.050632911392405
            },
            {
              "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L2/M2.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLBkyf25PeVl7hlEW6gioFZfoIm8vQ",
              "duration": 49.050632911392405
            },
            {
              "url": "https://i.ytimg.com/sb/7lVS5Ugo47s/storyboard3_L2/M3.jpg?sqp=-oaymwGhAUg48quKqQOYAYgBAZUBAAAEQpgBMqABPKgBBLIBQBANDBAVHyYtDg4PEhcrLCkPDhAVHyoyKQ8RFBgmPTgtERQeKjFLRzYVHCkuOUdNPyUuNz1HUlFFM0BCQ0xERkO6AUARERUjRENDQxETFi9DQ0NDFRYpQ0NDQ0MjL0NDQ0NDQ0RDQ0NDQ0JCQ0NDQ0NCQkJDQ0NDQkJCQkNDQ0JCQkJCovOX_wMGCKnC7oMG&sigh=rs$AOn4CLBkyf25PeVl7hlEW6gioFZfoIm8vQ",
              "duration": 7.848101265822777
            }
          ],
          "audio_ext": "none",
          "video_ext": "none",
          "vbr": 0,
          "abr": 0,
          "tbr": None,
          "resolution": "160x90",
          "aspect_ratio": 1.78,
          "filesize_approx": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "sb0 - 160x90 (storyboard)"
        },
        {
          "asr": 22050,
          "filesize": 944004,
          "format_id": "139",
          "format_note": "low",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 2.0,
          "has_drm": False,
          "tbr": 48.849,
          "filesize_approx": 943994,
          "width": None,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "m4a",
          "vcodec": "none",
          "acodec": "mp4a.40.5",
          "dynamic_range": None,
          "container": "m4a_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=139&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=944004&dur=154.598&lmt=1620800567370438&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAJj7_UPMuB-lFXDvqLiclyl6aFYbtvo1WyiJT89DVT7GAiA8l_SWZviTnGvt2TwbuIiulAUARPyrWLkjlY2t79pz3Q%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "m4a",
          "video_ext": "none",
          "vbr": 0,
          "abr": 48.849,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "139 - audio only (low)"
        },
        {
          "asr": 48000,
          "filesize": 1009704,
          "format_id": "249",
          "format_note": "low",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 2.0,
          "has_drm": False,
          "tbr": 52.275,
          "filesize_approx": 1009698,
          "width": None,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "none",
          "acodec": "opus",
          "dynamic_range": None,
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=249&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=audio%2Fwebm&rqh=1&gir=yes&clen=1009704&dur=154.521&lmt=1620800559724748&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAM2WYwrhgYYyAvDxpk3_iG7Re_Lj_pcwTv7IchlnMEHwAiBiOCGrccVDQ4rmJBPVVnM0GKzeL4DCSKJ-n1KCzHRCOw%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "webm",
          "video_ext": "none",
          "vbr": 0,
          "abr": 52.275,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "249 - audio only (low)"
        },
        {
          "asr": 44100,
          "filesize": 2502029,
          "format_id": "140",
          "format_note": "medium",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 3.0,
          "has_drm": False,
          "tbr": 129.511,
          "filesize_approx": 2502023,
          "width": None,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "m4a",
          "vcodec": "none",
          "acodec": "mp4a.40.2",
          "dynamic_range": None,
          "container": "m4a_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=140&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=2502029&dur=154.552&lmt=1620800567228956&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhALp6ptDtjnVaKzlU9ecf6n9TrY-0DXRlkpKboX8m22g0AiEAlMfSFBoyQeNvzGYxligF666gDaTynAtF8PcBUsWOYAc%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "m4a",
          "video_ext": "none",
          "vbr": 0,
          "abr": 129.511,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "140 - audio only (medium)"
        },
        {
          "asr": 48000,
          "filesize": 2553372,
          "format_id": "251",
          "format_note": "medium",
          "source_preference": -1,
          "fps": None,
          "audio_channels": 2,
          "height": None,
          "quality": 3.0,
          "has_drm": False,
          "tbr": 132.195,
          "filesize_approx": 2553362,
          "width": None,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "none",
          "acodec": "opus",
          "dynamic_range": None,
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=audio%2Fwebm&rqh=1&gir=yes&clen=2553372&dur=154.521&lmt=1620800559725924&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgG6NlTnYk5JGl_x2TdVe5BTbEkm4P6gfLeA0oNH8K4zACIBmK2sPEidMW_l0sqvRDvZySi5Jj43l46An3xGd7_Arc&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "audio_ext": "webm",
          "video_ext": "none",
          "vbr": 0,
          "abr": 132.195,
          "resolution": "audio only",
          "aspect_ratio": None,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "251 - audio only (medium)"
        },
        {
          "format_id": "91",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/itag/91/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D944004%3Bdur%3D154.598%3Bgir%3Dyes%3Bitag%3D139%3Blmt%3D1620800567370438/sgovp/clen%3D1418233%3Bdur%3D154.487%3Bgir%3Dyes%3Bitag%3D160%3Blmt%3D1620811969833604/rqh/1/hls_chunk_host/rr3---sn-qja5mc-5h.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/412/met/1782286468,/mh/A-/mm/31,26/mn/sn-qja5mc-5h,sn-vgqsknd7/ms/au,onr/mv/m/mvi/3/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/playlist_type/CLEAN/dover/11/txp/5535434/mt/1782286149/fvip/4/keepalive/yes/fexp/51565116,51565682,51946837,51987687/n/6IWcqr32jOxDdQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRQIgG6DxON34tVjHO2t4AbrXZ8AN75I1tbpBmIyv5ometA8CIQCV4OfAtl5xkgbySm1mW4FgoYMuOcy1dNLck6VRQSXU6A%3D%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIgIqCG79ltJ1Hs6ymxq082WzSz6ig4Rpn9ZOQQ_bdDqBkCIQCUYsEhayYqMIvrBRg9ZfA36jjco_5kElbN3TqlCDok1w%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-qja5mc-5h.googlevideo.com/cps/412/met/1782286468%2C/mh/A-/mm/31%2C26/mn/sn-qja5mc-5h%2Csn-vgqsknd7/ms/au%2Conr/mv/m/mvi/3/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/go/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/rqh/5/mt/1782286149/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51946837%2C51987687/dover/11/n/6IWcqr32jOxDdQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRQIhAPzFMxvQaPDsdntboHZHd2MuWEuoAslD6KGRhNknC_8MAiAmEiiOMgQWVqW9od5dQ56S5nirOlYyNxN9dbPfrudW8w%3D%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgXXbfb4X6AW6Nd0P99hEp12DVWFQNpKd0yGjJlTRCtl0CIQDnfCGcHu7muhwzP3RI4eR0XCHBMHRK5uyEQ69AojjSvQ%3D%3D/file/index.m3u8",
          "tbr": 166.518,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 0,
          "has_drm": False,
          "width": 256,
          "height": 144,
          "vcodec": "avc1.4D400C",
          "acodec": "mp4a.40.5",
          "dynamic_range": "SDR",
          "available_at": 1782286470,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "91 - 256x144"
        },
        {
          "asr": None,
          "filesize": 1418233,
          "format_id": "160",
          "format_note": "144p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 144,
          "quality": 0.0,
          "has_drm": False,
          "tbr": 73.442,
          "filesize_approx": 1418229,
          "width": 256,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d400c",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=160&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=1418233&dur=154.487&lmt=1620811969833604&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAPVzdtSNCGsIbvpgS2JvqpIYPljL5JKbGHkRPn5sPVYAAiEAvz7o6-RuFe2sGk3_WN5eLu0XGgGzFFETEBQITZ7a_H0%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 73.442,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "160 - 256x144 (144p)"
        },
        {
          "asr": None,
          "filesize": 1760602,
          "format_id": "278",
          "format_note": "144p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 144,
          "quality": 0.0,
          "has_drm": False,
          "tbr": 91.171,
          "filesize_approx": 1760591,
          "width": 256,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=278&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=1760602&dur=154.487&lmt=1663550537598295&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAOGtk0JZnO8ujMXy6ibFyWQxcxUIic0yY6ip20E0hEfwAiBnr9GdMkUHlfCe7njRk5s-VA547ruz8rWPBgBhZ3y_6g%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 91.171,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "278 - 256x144 (144p)"
        },
        {
          "asr": None,
          "filesize": 1076585,
          "format_id": "394",
          "format_note": "144p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 144,
          "quality": 0.0,
          "has_drm": False,
          "tbr": 55.75,
          "filesize_approx": 1076581,
          "width": 256,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.00M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=394&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=1076585&dur=154.487&lmt=1744923181763504&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgV5fiD94OIzwgnon1M3oQdIhwAc_7bDoj_VB2tcEPDSwCIE3_qM3T0yM2ifcmuMvQ9QALOTUal6v1AQeOhxiYel7U&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 55.75,
          "resolution": "256x144",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "394 - 256x144 (144p)"
        },
        {
          "format_id": "92",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/itag/92/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D944004%3Bdur%3D154.598%3Bgir%3Dyes%3Bitag%3D139%3Blmt%3D1620800567370438/sgovp/clen%3D2145254%3Bdur%3D154.487%3Bgir%3Dyes%3Bitag%3D133%3Blmt%3D1620811967507984/rqh/1/hls_chunk_host/rr3---sn-qja5mc-5h.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/412/met/1782286468,/mh/A-/mm/31,26/mn/sn-qja5mc-5h,sn-vgqsknd7/ms/au,onr/mv/m/mvi/3/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/playlist_type/CLEAN/dover/11/txp/5535434/mt/1782286149/fvip/4/keepalive/yes/fexp/51565116,51565682,51946837,51987687/n/6IWcqr32jOxDdQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRgIhALjEPabWba3YJbqhptF8wX-dwRSVGg1yLAhB2qQeoVvaAiEAx96XWk2bYOQSgnvt1RXP7qWvWtiDq0QROFG72ZgSdHc%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIgCl374sBf8z3Xt8ANfK11_c3loxdqn2_91am9ja2uk5ICIQD6yre3LmWyN0U0rGcYE0KD8wnROH39t4XwyaYjywuWfQ%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-qja5mc-5h.googlevideo.com/cps/412/met/1782286468%2C/mh/A-/mm/31%2C26/mn/sn-qja5mc-5h%2Csn-vgqsknd7/ms/au%2Conr/mv/m/mvi/3/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/go/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/rqh/5/mt/1782286149/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51946837%2C51987687/dover/11/n/6IWcqr32jOxDdQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRQIhAPzFMxvQaPDsdntboHZHd2MuWEuoAslD6KGRhNknC_8MAiAmEiiOMgQWVqW9od5dQ56S5nirOlYyNxN9dbPfrudW8w%3D%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgXXbfb4X6AW6Nd0P99hEp12DVWFQNpKd0yGjJlTRCtl0CIQDnfCGcHu7muhwzP3RI4eR0XCHBMHRK5uyEQ69AojjSvQ%3D%3D/file/index.m3u8",
          "tbr": 223.165,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 5,
          "has_drm": False,
          "width": 426,
          "height": 240,
          "vcodec": "avc1.4D4015",
          "acodec": "mp4a.40.5",
          "dynamic_range": "SDR",
          "available_at": 1782286470,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "426x240",
          "aspect_ratio": 1.77,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "92 - 426x240"
        },
        {
          "asr": None,
          "filesize": 2145254,
          "format_id": "133",
          "format_note": "240p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 240,
          "quality": 5.0,
          "has_drm": False,
          "tbr": 111.09,
          "filesize_approx": 2145245,
          "width": 426,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d4015",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=133&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=2145254&dur=154.487&lmt=1620811967507984&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAK7ixwH2xU6RqYpz7hEfzVXiz46WBSapv5fvNQnFbK9aAiAYeHFvRTU2ofn8Fk7gz9LlWqcDdHnI7jjQOO7wUUFEkA%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 111.09,
          "resolution": "426x240",
          "aspect_ratio": 1.77,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "133 - 426x240 (240p)"
        },
        {
          "asr": None,
          "filesize": 2665562,
          "format_id": "242",
          "format_note": "240p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 240,
          "quality": 5.0,
          "has_drm": False,
          "tbr": 138.034,
          "filesize_approx": 2665557,
          "width": 426,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=242&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=2665562&dur=154.487&lmt=1663550467055869&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgKKGdi1bD0UiqYQmrYwqUKTafqD18gM3F4ZkiVnuQ8QUCIEsD2Qj_TJEWhZyTAH5Ceq_SzN32tY6r1-_f487KJed0&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 138.034,
          "resolution": "426x240",
          "aspect_ratio": 1.77,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "242 - 426x240 (240p)"
        },
        {
          "asr": None,
          "filesize": 2078733,
          "format_id": "395",
          "format_note": "240p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 240,
          "quality": 5.0,
          "has_drm": False,
          "tbr": 107.645,
          "filesize_approx": 2078719,
          "width": 426,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.00M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=395&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=2078733&dur=154.487&lmt=1744924110140620&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAMpUMFPHJd4VYutca06B8PRSLgEsP0mnHtSQFM3xN9I_AiEAt_oh-mVHfldk0NU4wwDsQRnDQOcJvVU6YShRXn1akIs%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 107.645,
          "resolution": "426x240",
          "aspect_ratio": 1.77,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "395 - 426x240 (240p)"
        },
        {
          "format_id": "93",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/itag/93/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2502029%3Bdur%3D154.552%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1620800567228956/sgovp/clen%3D3683992%3Bdur%3D154.487%3Bgir%3Dyes%3Bitag%3D134%3Blmt%3D1620811972662483/rqh/1/hls_chunk_host/rr3---sn-qja5mc-5h.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/412/met/1782286468,/mh/A-/mm/31,26/mn/sn-qja5mc-5h,sn-vgqsknd7/ms/au,onr/mv/m/mvi/3/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/playlist_type/CLEAN/dover/11/txp/5535434/mt/1782286149/fvip/4/keepalive/yes/fexp/51565116,51565682,51946837,51987687/n/6IWcqr32jOxDdQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRAIgfvwxCVm9fgBXEcIQoukiLZZAaRiyXN5vqpIBYUH7iboCIEDk-UUB_oMIjCVgKRJD4lc3fDG0Kd4tCEQcfsSZqm80/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRAIgZcxJ8hhrO4m-qQ0A-cT4jCisDTGXXKr0f7uItFGY9VkCIEGmWJ_7Ey3yiR8ahwV7qIJgKT19IREUkalyqdXpJ2GU/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-qja5mc-5h.googlevideo.com/cps/412/met/1782286468%2C/mh/A-/mm/31%2C26/mn/sn-qja5mc-5h%2Csn-vgqsknd7/ms/au%2Conr/mv/m/mvi/3/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/go/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/rqh/5/mt/1782286149/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51946837%2C51987687/dover/11/n/6IWcqr32jOxDdQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRQIhAPzFMxvQaPDsdntboHZHd2MuWEuoAslD6KGRhNknC_8MAiAmEiiOMgQWVqW9od5dQ56S5nirOlYyNxN9dbPfrudW8w%3D%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgXXbfb4X6AW6Nd0P99hEp12DVWFQNpKd0yGjJlTRCtl0CIQDnfCGcHu7muhwzP3RI4eR0XCHBMHRK5uyEQ69AojjSvQ%3D%3D/file/index.m3u8",
          "tbr": 438.822,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 6,
          "has_drm": False,
          "width": 640,
          "height": 360,
          "vcodec": "avc1.4D401E",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286470,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "93 - 640x360"
        },
        {
          "asr": None,
          "filesize": 3683992,
          "format_id": "134",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 190.772,
          "filesize_approx": 3683974,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d401e",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=134&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=3683992&dur=154.487&lmt=1620811972662483&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhALWZCL95ByhS1WjDvupJ4uvCaI1HyVKk0ISMqBW2E2PeAiEA52teWQMi30YsGQrvxM_82yKSnI_87IxZS6q4XJDQ6Vs%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 190.772,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "134 - 640x360 (360p)"
        },
        {
          "asr": 44100,
          "filesize": None,
          "format_id": "18",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": 2,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 320.006,
          "filesize_approx": 6182195,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.42001E",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEXPuyxfqeFMGWm5O45_1km1Z_cGOsfAgKbbc81OLyLmcs1ikwl_xzrWKRvNq_Y7WTCH9R0ZiLqC&spc=SQ-umu_XbF7uiTgaOScEnCsDNy9LTqCV9wnehhaCuHREe4eDr_qL&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&cnr=14&ratebypass=yes&dur=154.552&lmt=1665182629204497&mt=1782286149&fvip=3&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5538434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AHEqNM4wRgIhAPzBRUaVoCTiOOlLU4pKN_QkyTxLHIjiwC74Bd8J52qUAiEArvu8J5pHsL24IQP8_Xg7U3G-lxqFVLG8g1hxIudgOsQ%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "18 - 640x360 (360p)"
        },
        {
          "asr": None,
          "filesize": 4371515,
          "format_id": "243",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 226.375,
          "filesize_approx": 4371499,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=243&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=4371515&dur=154.487&lmt=1663550493681665&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgUCkw1A_Po2tV-445JUPyZtwiILHY9DsTWJZC7CsxDEUCIQC34RIoWhxsJNbZ9NQFimfPR99AQsfFeuVCITSaQm5r4Q%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 226.375,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "243 - 640x360 (360p)"
        },
        {
          "asr": None,
          "filesize": 3431033,
          "format_id": "396",
          "format_note": "360p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 360,
          "quality": 6.0,
          "has_drm": False,
          "tbr": 177.673,
          "filesize_approx": 3431021,
          "width": 640,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.01M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=396&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=3431033&dur=154.487&lmt=1744923802257142&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAJvs2Z6CFoC09eiEymKvjLpsRHC2xtyCb_m59mx9JfisAiBe7_rv-vvh1xkACry1mBZJFyAYlp4voFWJw9IwDU_ykw%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 177.673,
          "resolution": "640x360",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "396 - 640x360 (360p)"
        },
        {
          "format_id": "94",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/itag/94/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2502029%3Bdur%3D154.552%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1620800567228956/sgovp/clen%3D5295775%3Bdur%3D154.487%3Bgir%3Dyes%3Bitag%3D135%3Blmt%3D1620811977389502/rqh/1/hls_chunk_host/rr3---sn-qja5mc-5h.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/412/met/1782286468,/mh/A-/mm/31,26/mn/sn-qja5mc-5h,sn-vgqsknd7/ms/au,onr/mv/m/mvi/3/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/playlist_type/CLEAN/dover/11/txp/5535434/mt/1782286149/fvip/4/keepalive/yes/fexp/51565116,51565682,51946837,51987687/n/6IWcqr32jOxDdQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRQIgA9AlUtZW_kr4SkXgSQUvgUntJxHQrYLPl7_hd2B_jr0CIQCX3Pyc5HIBKRg_4XpMJvPPw4tX3rB7u2LcV1Q9lXyMPw%3D%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIhAPkvJoz02hrEFcM896VfuUDTBRZpsIP-2JaNU-qxuR-wAiBxgRMdCekswC9lQbzAwhiER5FbL3d2F0uIIWiokPid8w%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-qja5mc-5h.googlevideo.com/cps/412/met/1782286468%2C/mh/A-/mm/31%2C26/mn/sn-qja5mc-5h%2Csn-vgqsknd7/ms/au%2Conr/mv/m/mvi/3/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/go/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/rqh/5/mt/1782286149/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51946837%2C51987687/dover/11/n/6IWcqr32jOxDdQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRQIhAPzFMxvQaPDsdntboHZHd2MuWEuoAslD6KGRhNknC_8MAiAmEiiOMgQWVqW9od5dQ56S5nirOlYyNxN9dbPfrudW8w%3D%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgXXbfb4X6AW6Nd0P99hEp12DVWFQNpKd0yGjJlTRCtl0CIQDnfCGcHu7muhwzP3RI4eR0XCHBMHRK5uyEQ69AojjSvQ%3D%3D/file/index.m3u8",
          "tbr": 564.378,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 7,
          "has_drm": False,
          "width": 854,
          "height": 480,
          "vcodec": "avc1.4D401E",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286470,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "854x480",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "94 - 854x480"
        },
        {
          "asr": None,
          "filesize": 5295775,
          "format_id": "135",
          "format_note": "480p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 480,
          "quality": 7.0,
          "has_drm": False,
          "tbr": 274.237,
          "filesize_approx": 5295756,
          "width": 854,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d401e",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=135&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=5295775&dur=154.487&lmt=1620811977389502&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgHlm6VikpOJOS6e4gGK1Emyx4ShotqwVfoOEM2j3O_jICIExK170o5VP7dNKjtQaJeYzJLN8NLigy3_reAnMpLBgX&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 274.237,
          "resolution": "854x480",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "135 - 854x480 (480p)"
        },
        {
          "asr": None,
          "filesize": 6173279,
          "format_id": "244",
          "format_note": "480p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 480,
          "quality": 7.0,
          "has_drm": False,
          "tbr": 319.678,
          "filesize_approx": 6173261,
          "width": 854,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=244&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=6173279&dur=154.487&lmt=1663550493738090&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgYs8cxF39Oki6RYmoiLq5Mig7qI8yGx8xw5esBboJ558CIQCliOu67A8cuiE06yWYoOjeZU_NkbxgRB3l01tuEKbRVQ%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 319.678,
          "resolution": "854x480",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "244 - 854x480 (480p)"
        },
        {
          "asr": None,
          "filesize": 5597111,
          "format_id": "397",
          "format_note": "480p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 480,
          "quality": 7.0,
          "has_drm": False,
          "tbr": 289.842,
          "filesize_approx": 5597102,
          "width": 854,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.04M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=397&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=5597111&dur=154.487&lmt=1744926219410447&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRAIgDTuZo6FD_jYepAk6CDh1DYkaaL40L8TDYsBJOPkuujUCIDmEbr_RbxwsVVIOuHzWvzt7cDF4gXfM4wE7aPJ1Ruqp&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 289.842,
          "resolution": "854x480",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "397 - 854x480 (480p)"
        },
        {
          "format_id": "95",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/itag/95/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2502029%3Bdur%3D154.552%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1620800567228956/sgovp/clen%3D8614765%3Bdur%3D154.487%3Bgir%3Dyes%3Bitag%3D136%3Blmt%3D1620811967459677/rqh/1/hls_chunk_host/rr3---sn-qja5mc-5h.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/412/met/1782286468,/mh/A-/mm/31,26/mn/sn-qja5mc-5h,sn-vgqsknd7/ms/au,onr/mv/m/mvi/3/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/playlist_type/CLEAN/dover/11/txp/5535434/mt/1782286149/fvip/4/keepalive/yes/fexp/51565116,51565682,51946837,51987687/n/6IWcqr32jOxDdQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRgIhAJel4ICS2kiKnpsxvZ0W4LWRfXA6mxJBNcrOSoVz0gvyAiEAkC9u8iNWPvBxOzi9ZuZ1Yi_sPcjQR7wKa-BHQ_-x32k%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRQIhAOXE4CXsRwFxOdWBZdKOizankGdJ5W3WuyiZcBYcpPt7AiAh7VfurX5x1pXMqwj3c6nBZIrpjKxlOcf9x9acqeB48w%3D%3D/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-qja5mc-5h.googlevideo.com/cps/412/met/1782286468%2C/mh/A-/mm/31%2C26/mn/sn-qja5mc-5h%2Csn-vgqsknd7/ms/au%2Conr/mv/m/mvi/3/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/go/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/rqh/5/mt/1782286149/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51946837%2C51987687/dover/11/n/6IWcqr32jOxDdQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRQIhAPzFMxvQaPDsdntboHZHd2MuWEuoAslD6KGRhNknC_8MAiAmEiiOMgQWVqW9od5dQ56S5nirOlYyNxN9dbPfrudW8w%3D%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgXXbfb4X6AW6Nd0P99hEp12DVWFQNpKd0yGjJlTRCtl0CIQDnfCGcHu7muhwzP3RI4eR0XCHBMHRK5uyEQ69AojjSvQ%3D%3D/file/index.m3u8",
          "tbr": 835.965,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 8,
          "has_drm": False,
          "width": 1280,
          "height": 720,
          "vcodec": "avc1.4D401F",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286470,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "95 - 1280x720"
        },
        {
          "asr": None,
          "filesize": 8614765,
          "format_id": "136",
          "format_note": "720p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 720,
          "quality": 8.0,
          "has_drm": False,
          "tbr": 446.109,
          "filesize_approx": 8614755,
          "width": 1280,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.4d401f",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=136&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=8614765&dur=154.487&lmt=1620811967459677&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAMF8zAtDCip1fAh9-zwIiSvKOjSWh6o_gBahuhfE4tsdAiAU7GaK8xkGpQihjKMozU1jeDnY9O4vcrGb7vxtvfRyew%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 446.109,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "136 - 1280x720 (720p)"
        },
        {
          "asr": None,
          "filesize": 9558929,
          "format_id": "247",
          "format_note": "720p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 720,
          "quality": 8.0,
          "has_drm": False,
          "tbr": 495.002,
          "filesize_approx": 9558921,
          "width": 1280,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=247&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=9558929&dur=154.487&lmt=1663550493701245&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgDKn74xNNY9RFybUrxfU7ZdyxBabVGZL42DIM3Oy6fYACIQC8mMROC8sRC3MKPRa7hQb0ZXThYd-FLNzZCbJRBX4Qiw%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 495.002,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "247 - 1280x720 (720p)"
        },
        {
          "asr": None,
          "filesize": 9646191,
          "format_id": "398",
          "format_note": "720p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 720,
          "quality": 8.0,
          "has_drm": False,
          "tbr": 499.521,
          "filesize_approx": 9646187,
          "width": 1280,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.05M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=398&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=9646191&dur=154.487&lmt=1744925226812899&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhALVZDtSf0KLv_Ck9KGDJUBu6Kc-MhLe_-UO8ug25KsTWAiB3u23OkaKcI0nn5ZGuM5LQ_uCUClos8nOwsCIW2KfV_Q%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 499.521,
          "resolution": "1280x720",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "398 - 1280x720 (720p)"
        },
        {
          "format_id": "96",
          "format_index": None,
          "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/itag/96/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/sgoap/clen%3D2502029%3Bdur%3D154.552%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1620800567228956/sgovp/clen%3D27917372%3Bdur%3D154.487%3Bgir%3Dyes%3Bitag%3D137%3Blmt%3D1620811960251957/rqh/1/hls_chunk_host/rr3---sn-qja5mc-5h.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/cps/412/met/1782286468,/mh/A-/mm/31,26/mn/sn-qja5mc-5h,sn-vgqsknd7/ms/au,onr/mv/m/mvi/3/pl/12/rms/au,au/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/playlist_type/CLEAN/dover/11/txp/5535434/mt/1782286149/fvip/4/keepalive/yes/fexp/51565116,51565682,51946837,51987687/n/6IWcqr32jOxDdQ/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,sgoap,sgovp,rqh,xpc,bui,spc,vprv,ns,playlist_type/sig/AHEqNM4wRQIhAN2BBdObEsPkXjnzXHJjLzXb5k23AsmX5_vco2zBl-akAiBwot6g-xr66Nu6SGni1DtXwUu_2Exzbh2uWTUUw0_aLg%3D%3D/lsparams/hls_chunk_host,cps,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRAIgU0w2mAmSA7WVW-bjZS5z14yujyugkUT_dn5C8lQRNV8CIA7hQKEfVl5r4r9kM6LfK_8FTf3oF0-9cxhZUa5UPMj9/playlist/index.m3u8",
          "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1782308068/ei/hIg7avWzM4aTsfIPzbma2AQ/ip/47.147.88.26/id/ee5552e54828e3bb/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-qja5mc-5h.googlevideo.com/cps/412/met/1782286468%2C/mh/A-/mm/31%2C26/mn/sn-qja5mc-5h%2Csn-vgqsknd7/ms/au%2Conr/mv/m/mvi/3/pl/12/rms/au%2Cau/hfr/1/tts_caps/1/maudio/1/initcwndbps/3635000/bui/ARmQxEWXNbcFUuEBnqzx94dETKwzPOfbxfuJnuoKQM91wKAruSSftk-BPRh1XCJ4IiOTrAh-CA0EZvoi/spc/SQ-umsRxFQMlR9UGvO5afsyJBhD2yedEb9V6BOH_lgiaQ56MA0pWhsOqj3PJCa_I_AddBTiR/vprv/1/go/1/ns/we88I3Ng0M0cLYNcC_SnlrIW/rqh/5/mt/1782286149/fvip/4/nvgoi/1/ncsapi/1/keepalive/yes/fexp/51565116%2C51565682%2C51946837%2C51987687/dover/11/n/6IWcqr32jOxDdQ/itag/0/playlist_type/CLEAN/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Cns%2Crqh%2Citag%2Cplaylist_type/sig/AHEqNM4wRQIhAPzFMxvQaPDsdntboHZHd2MuWEuoAslD6KGRhNknC_8MAiAmEiiOMgQWVqW9od5dQ56S5nirOlYyNxN9dbPfrudW8w%3D%3D/lsparams/playback_host%2Ccps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgXXbfb4X6AW6Nd0P99hEp12DVWFQNpKd0yGjJlTRCtl0CIQDnfCGcHu7muhwzP3RI4eR0XCHBMHRK5uyEQ69AojjSvQ%3D%3D/file/index.m3u8",
          "tbr": 2333.993,
          "ext": "mp4",
          "fps": 24.0,
          "protocol": "m3u8_native",
          "preference": None,
          "quality": 9,
          "has_drm": False,
          "width": 1920,
          "height": 1080,
          "vcodec": "avc1.640028",
          "acodec": "mp4a.40.2",
          "dynamic_range": "SDR",
          "available_at": 1782286470,
          "source_preference": -2,
          "video_ext": "mp4",
          "audio_ext": "none",
          "vbr": None,
          "abr": None,
          "resolution": "1920x1080",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "96 - 1920x1080"
        },
        {
          "asr": None,
          "filesize": 27917372,
          "format_id": "137",
          "format_note": "1080p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 1080,
          "quality": 9.0,
          "has_drm": False,
          "tbr": 1445.681,
          "filesize_approx": 27917365,
          "width": 1920,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "avc1.640028",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=137&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=27917372&dur=154.487&lmt=1620811960251957&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhANLbrHHvRiQOIdEX1QR291Tb_cGFrQm_tJn-TBNBmUhaAiEAy4mT4tWZGeGmnIJtpvg0wCtaQSTR1dxHIq2okyEA3CI%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 1445.681,
          "resolution": "1920x1080",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "137 - 1920x1080 (1080p)"
        },
        {
          "asr": None,
          "filesize": 27733188,
          "format_id": "248",
          "format_note": "1080p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 1080,
          "quality": 9.0,
          "has_drm": False,
          "tbr": 1436.143,
          "filesize_approx": 27733177,
          "width": 1920,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "webm",
          "vcodec": "vp9",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "webm_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=248&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fwebm&rqh=1&gir=yes&clen=27733188&dur=154.487&lmt=1663548451242854&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5535434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRgIhAPa_9DKqCxjSEpkjUOYUBzc4JZC6W3dhgADzAEEB7YvXAiEA5zyL7jRMR9eP4PAAqK7RvdAGw5xgv9QrC08hKOwX5CE%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "webm",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 1436.143,
          "resolution": "1920x1080",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "248 - 1920x1080 (1080p)"
        },
        {
          "asr": None,
          "filesize": 16699919,
          "format_id": "399",
          "format_note": "1080p",
          "source_preference": -1,
          "fps": 24,
          "audio_channels": None,
          "height": 1080,
          "quality": 9.0,
          "has_drm": False,
          "tbr": 864.793,
          "filesize_approx": 16699909,
          "width": 1920,
          "language": None,
          "language_preference": -1,
          "preference": None,
          "ext": "mp4",
          "vcodec": "av01.0.08M.08",
          "acodec": "none",
          "dynamic_range": "SDR",
          "container": "mp4_dash",
          "url": "https://rr3---sn-qja5mc-5h.googlevideo.com/videoplayback?expire=1782308069&ei=hYg7arGuJeCLsfIP--3FEA&ip=47.147.88.26&id=o-AKVEuctRu42FYxEOkXaUC3YjAaYudS1tq4vCAz8cGMW7&itag=399&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=334&met=1782286469%2C&mh=A-&mm=31%2C26&mn=sn-qja5mc-5h%2Csn-ojvgq5-cv&ms=au%2Conr&mv=m&mvi=3&pl=12&rms=au%2Cau&initcwndbps=3615000&bui=ARmQxEX8F4J1cL9uiXM4bBglyE9KrH-6hJyVLv732wpyP4TR7PtjbiOtA74wdk7ENFd1Ilajlt6jJRK3&spc=SQ-umsXeVlvcgToiESZGpAMedSorUjqVpwW8lp-bulxP&vprv=1&svpuc=1&mime=video%2Fmp4&rqh=1&gir=yes&clen=16699919&dur=154.487&lmt=1744928093943735&mt=1782286149&fvip=3&keepalive=yes&fexp=51565116%2C51565682%2C51946837%2C51987687&c=ANDROID_VR&txp=5537534&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIhAJkmkViGatyMqvhrd3uHTFUKi8mOSHFIPdmmqE6GVz8eAiBtU1XQpgkRbCn-sZiLQCop3Vv1-qbxH8Bka3lMb-OE7A%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRAIgZbPbLILAubtzmip5E3glJ1OsqUhmSZZWE8jSPb6Yj0wCIGkI0qx1HOL6TtWmZAYckdHqDDHcaqtgX8rWlDTmqKf4",
          "available_at": 1782286470,
          "downloader_options": { "http_chunk_size": 10485760 },
          "protocol": "https",
          "video_ext": "mp4",
          "audio_ext": "none",
          "abr": 0,
          "vbr": 864.793,
          "resolution": "1920x1080",
          "aspect_ratio": 1.78,
          "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
          },
          "format": "399 - 1920x1080 (1080p)"
        }
      ],
      "thumbnail": "https://i.ytimg.com/vi/7lVS5Ugo47s/maxresdefault.jpg",
      "average_rating": None,
      "age_limit": 0,
      "webpage_url": "https://www.youtube.com/watch?v=7lVS5Ugo47s",
      "categories": ["Music"],
      "tags": [],
      "playable_in_embed": True,
      "media_type": "video",
      "_format_sort_fields": [
        "quality",
        "res",
        "fps",
        "hdr:12",
        "source",
        "vcodec",
        "channels",
        "acodec",
        "lang",
        "proto"
      ],
      "automatic_captions": {},
      "subtitles": {},
      "comment_count": 3700,
      "chapters": [
        { "start_time": 0.0, "title": "Gura talks", "end_time": 34.0 },
        { "start_time": 34.0, "title": "Singing", "end_time": 146.0 },
        { "start_time": 146.0, "title": "Senzawa talks", "end_time": 155 }
      ],
      "heatmap": [
        { "start_time": 0.0, "end_time": 1.55, "value": 0.44198208885178764 },
        { "start_time": 1.55, "end_time": 3.1, "value": 0.04496327492997547 },
        { "start_time": 3.1, "end_time": 4.65, "value": 0.09446166645306969 },
        { "start_time": 4.65, "end_time": 6.2, "value": 0.08504487286424549 },
        { "start_time": 6.2, "end_time": 7.75, "value": 0.04237902925423101 },
        { "start_time": 7.75, "end_time": 9.3, "value": 0.022186115352034207 },
        { "start_time": 9.3, "end_time": 10.85, "value": 0.011618731227283794 },
        { "start_time": 10.85, "end_time": 12.4, "value": 0.0 },
        {
          "start_time": 12.4,
          "end_time": 13.95,
          "value": 0.0014062402871010036
        },
        {
          "start_time": 13.95,
          "end_time": 15.5,
          "value": 0.016484659265045297
        },
        {
          "start_time": 15.5,
          "end_time": 17.05,
          "value": 0.029073992937467305
        },
        {
          "start_time": 17.05,
          "end_time": 18.6,
          "value": 0.054831205335246984
        },
        { "start_time": 18.6, "end_time": 20.15, "value": 0.07199606959339523 },
        { "start_time": 20.15, "end_time": 21.7, "value": 0.07734171588979863 },
        { "start_time": 21.7, "end_time": 23.25, "value": 0.07534576462190752 },
        { "start_time": 23.25, "end_time": 24.8, "value": 0.07821490811357981 },
        { "start_time": 24.8, "end_time": 26.35, "value": 0.08516686479244623 },
        { "start_time": 26.35, "end_time": 27.9, "value": 0.10529778279670494 },
        { "start_time": 27.9, "end_time": 29.45, "value": 0.10516787472562232 },
        { "start_time": 29.45, "end_time": 31.0, "value": 0.1317992792810209 },
        { "start_time": 31.0, "end_time": 32.55, "value": 0.13706834731101958 },
        { "start_time": 32.55, "end_time": 34.1, "value": 0.5809295618273258 },
        { "start_time": 34.1, "end_time": 35.65, "value": 0.5765790163550845 },
        { "start_time": 35.65, "end_time": 37.2, "value": 0.3206435340861613 },
        { "start_time": 37.2, "end_time": 38.75, "value": 0.3400711652912299 },
        { "start_time": 38.75, "end_time": 40.3, "value": 0.2905122777709542 },
        { "start_time": 40.3, "end_time": 41.85, "value": 0.2578456058824108 },
        { "start_time": 41.85, "end_time": 43.4, "value": 0.25771644776170644 },
        { "start_time": 43.4, "end_time": 44.95, "value": 0.23544567134474603 },
        { "start_time": 44.95, "end_time": 46.5, "value": 0.21682473676325084 },
        { "start_time": 46.5, "end_time": 48.05, "value": 0.21583230242932258 },
        { "start_time": 48.05, "end_time": 49.6, "value": 0.19835995851607818 },
        { "start_time": 49.6, "end_time": 51.15, "value": 0.19818646999523531 },
        { "start_time": 51.15, "end_time": 52.7, "value": 0.19268091761261796 },
        { "start_time": 52.7, "end_time": 54.25, "value": 0.18770158041209606 },
        { "start_time": 54.25, "end_time": 55.8, "value": 0.1872382777339566 },
        { "start_time": 55.8, "end_time": 57.35, "value": 0.1999346043270137 },
        { "start_time": 57.35, "end_time": 58.9, "value": 0.2016064103758468 },
        { "start_time": 58.9, "end_time": 60.45, "value": 0.20600028631438885 },
        { "start_time": 60.45, "end_time": 62.0, "value": 0.21415383015490475 },
        { "start_time": 62.0, "end_time": 63.55, "value": 0.21594537828080376 },
        { "start_time": 63.55, "end_time": 65.1, "value": 0.2202282615633599 },
        { "start_time": 65.1, "end_time": 66.65, "value": 0.22438157008611265 },
        { "start_time": 66.65, "end_time": 68.2, "value": 0.2379761705767135 },
        { "start_time": 68.2, "end_time": 69.75, "value": 0.24607371812231757 },
        { "start_time": 69.75, "end_time": 71.3, "value": 0.2515073585964395 },
        { "start_time": 71.3, "end_time": 72.85, "value": 0.2694421719096253 },
        { "start_time": 72.85, "end_time": 74.4, "value": 0.2890406251453029 },
        { "start_time": 74.4, "end_time": 75.95, "value": 0.3017026206765986 },
        { "start_time": 75.95, "end_time": 77.5, "value": 0.34010657961464885 },
        { "start_time": 77.5, "end_time": 79.05, "value": 0.383706111445626 },
        { "start_time": 79.05, "end_time": 80.6, "value": 0.42452257742279387 },
        { "start_time": 80.6, "end_time": 82.15, "value": 0.4573275734922206 },
        { "start_time": 82.15, "end_time": 83.7, "value": 0.48643714740874644 },
        { "start_time": 83.7, "end_time": 85.25, "value": 0.4777140579198343 },
        { "start_time": 85.25, "end_time": 86.8, "value": 0.4549915613916879 },
        { "start_time": 86.8, "end_time": 88.35, "value": 0.47099116941762353 },
        { "start_time": 88.35, "end_time": 89.9, "value": 0.46586217545272424 },
        { "start_time": 89.9, "end_time": 91.45, "value": 0.4774880728725116 },
        { "start_time": 91.45, "end_time": 93.0, "value": 0.5103643975556951 },
        { "start_time": 93.0, "end_time": 94.55, "value": 0.5530822377252705 },
        { "start_time": 94.55, "end_time": 96.1, "value": 0.5535510400395174 },
        { "start_time": 96.1, "end_time": 97.65, "value": 0.5127255746578101 },
        { "start_time": 97.65, "end_time": 99.2, "value": 0.46719758709298737 },
        { "start_time": 99.2, "end_time": 100.75, "value": 0.4390292842290269 },
        {
          "start_time": 100.75,
          "end_time": 102.3,
          "value": 0.42253112585717245
        },
        {
          "start_time": 102.3,
          "end_time": 103.85,
          "value": 0.40677200191920637
        },
        {
          "start_time": 103.85,
          "end_time": 105.4,
          "value": 0.4053181814469943
        },
        {
          "start_time": 105.4,
          "end_time": 106.95,
          "value": 0.4084929713817269
        },
        { "start_time": 106.95, "end_time": 108.5, "value": 0.412193559859456 },
        {
          "start_time": 108.5,
          "end_time": 110.05,
          "value": 0.42204465804512603
        },
        {
          "start_time": 110.05,
          "end_time": 111.6,
          "value": 0.42926126387970664
        },
        {
          "start_time": 111.6,
          "end_time": 113.15,
          "value": 0.42909152511075516
        },
        {
          "start_time": 113.15,
          "end_time": 114.7,
          "value": 0.42799476434642575
        },
        {
          "start_time": 114.7,
          "end_time": 116.25,
          "value": 0.4402459537260618
        },
        { "start_time": 116.25, "end_time": 117.8, "value": 0.447525222081139 },
        {
          "start_time": 117.8,
          "end_time": 119.35,
          "value": 0.46057502528582694
        },
        {
          "start_time": 119.35,
          "end_time": 120.9,
          "value": 0.5155098904289166
        },
        {
          "start_time": 120.9,
          "end_time": 122.45,
          "value": 0.5435981985858602
        },
        {
          "start_time": 122.45,
          "end_time": 124.0,
          "value": 0.5793251679847183
        },
        {
          "start_time": 124.0,
          "end_time": 125.55,
          "value": 0.7637802965370458
        },
        {
          "start_time": 125.55,
          "end_time": 127.1,
          "value": 0.7819024307891628
        },
        {
          "start_time": 127.1,
          "end_time": 128.65,
          "value": 0.7689662867306947
        },
        {
          "start_time": 128.65,
          "end_time": 130.2,
          "value": 0.7264412671361579
        },
        {
          "start_time": 130.2,
          "end_time": 131.75,
          "value": 0.6753889784292606
        },
        { "start_time": 131.75, "end_time": 133.3, "value": 0.619417848519023 },
        {
          "start_time": 133.3,
          "end_time": 134.85,
          "value": 0.5906655842938392
        },
        {
          "start_time": 134.85,
          "end_time": 136.4,
          "value": 0.5912622114836735
        },
        {
          "start_time": 136.4,
          "end_time": 137.95,
          "value": 0.5850311237739769
        },
        {
          "start_time": 137.95,
          "end_time": 139.5,
          "value": 0.5897046478757989
        },
        { "start_time": 139.5, "end_time": 141.05, "value": 0.641570382759674 },
        {
          "start_time": 141.05,
          "end_time": 142.6,
          "value": 0.6715450661014596
        },
        {
          "start_time": 142.6,
          "end_time": 144.15,
          "value": 0.7153704996519397
        },
        {
          "start_time": 144.15,
          "end_time": 145.7,
          "value": 0.7864486299823161
        },
        { "start_time": 145.7, "end_time": 147.25, "value": 1.0 },
        {
          "start_time": 147.25,
          "end_time": 148.8,
          "value": 0.9256469196954802
        },
        {
          "start_time": 148.8,
          "end_time": 150.35,
          "value": 0.9099634574179009
        },
        {
          "start_time": 150.35,
          "end_time": 151.9,
          "value": 0.8516904798132524
        },
        {
          "start_time": 151.9,
          "end_time": 153.45,
          "value": 0.7471827280761589
        },
        { "start_time": 153.45, "end_time": 155.0, "value": 0.6347133364675704 }
      ],
      "like_count": 56935,
      "channel_follower_count": 1820,
      "creators": None,
      "upload_date": "20210418",
      "__post_extractor": None,
      "original_url": "7lVS5Ugo47s",
      "webpage_url_basename": "watch",
      "webpage_url_domain": "youtube.com",
      "extractor": "youtube",
      "extractor_key": "Youtube",
      "display_id": "7lVS5Ugo47s",
      "fulltitle": "When I'm Gone - Gura x Senzawa Cover Duet",
      "duration_string": "2:35",
      "release_year": None,
      "is_live": False,
      "was_live": False,
      "requested_subtitles": None,
      "_has_drm": None,
      "epoch": 1782286471
    }
  ],
  "extractor_key": "YoutubeTab",
  "extractor": "youtube:tab",
  "webpage_url": "https://www.youtube.com/playlist?list=PLXOfMLBzXbbVV8P-wQyZ9MAKxFsGy5v0b",
  "original_url": "https://www.youtube.com/watch?v=cP3eChqUphA&list=PLXOfMLBzXbbVV8P-wQyZ9MAKxFsGy5v0b&pp=sAgC",
  "webpage_url_basename": "playlist",
  "webpage_url_domain": "youtube.com",
  "release_year": None,
  "epoch": 1782286437
}
