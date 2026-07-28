__all__ = [
    'reorder_v_infodict', 'reorder_pl_infodict',
]

"""
This is coupled to `pldl_type` and `pldl_type_extensions`

Reordering was done using Claude
"""

from typing import Any
from pldl.pldl_types import *
from pldl.utils.utils import dict_reorder_keys


V_START = [
    # identity
    'id',
    'display_id',
    'title',
    'fulltitle',
    'alt_title',
    'description',

    # status / type
    'media_type',
    'live_status',
    'is_live',
    'was_live',
    'availability',
    'age_limit',
    'playable_in_embed',

    # people / channel
    'channel',
    'channel_id',
    'channel_url',
    'channel_follower_count',
    'uploader',
    'uploader_id',
    'uploader_url',
    'creators',
    'creator',
    'artists',
    'artist',
    'album',
    'track',

    # stats
    'view_count',
    'like_count',
    'comment_count',
    'average_rating',

    # time
    'upload_date',
    'timestamp',
    'release_timestamp',
    'release_date',
    'release_year',
    'epoch',

    # categorization
    'categories',
    'tags',

    # duration
    'duration',
    'duration_string',

    # media assets
    'thumbnail',
    'thumbnails',
    'chapters',
    'heatmap',

    # subtitles / captions
    'subtitles',
    'automatic_captions',
    'requested_subtitles',

    # urls / extractor
    'webpage_url',
    'webpage_url_basename',
    'webpage_url_domain',
    'original_url',
    'url',
    'extractor',
    'extractor_key',

    # format info
    'formats',
    'requested_formats',
    'requested_downloads',
    'format',
    'format_id',
    'format_note',
    '_format_sort_fields',
    'ext',
    'video_ext',
    'audio_ext',
    'protocol',
    'language',
    'tbr',
    'vbr',
    'abr',
    'asr',
    'filesize',
    'filesize_approx',
    'width',
    'height',
    'resolution',
    'aspect_ratio',
    'stretched_ratio',
    'fps',
    'dynamic_range',
    'vcodec',
    'acodec',
    'audio_channels',
    'cookies',
    'http_headers',

    # drm
    '_has_drm',

    # playlist
    'playlist',
    'playlist_index',
    'playlist_count',
    'playlist_id',
    'playlist_title',
    'playlist_uploader',
    'playlist_uploader_id',
    'playlist_channel',
    'playlist_channel_id',
    'playlist_webpage_url',
    'n_entries',
    '__last_playlist_index',
    'playlist_autonumber',
]

V_END = [
    # custom fields
    'info_level',
    'yt_unavailable_msg',
    'wa_unavailable_msg',
    'unavailable_msgs',
    'playlist_epoch',
]


PL_START = [
    # identity
    'id',
    'title',
    'description',
    'tags',

    # status
    'availability',
    '_type',

    # channel / uploader
    'channel',
    'channel_id',
    'channel_url',
    'channel_follower_count',
    'uploader',
    'uploader_id',
    'uploader_url',

    # stats
    'view_count',
    'playlist_count',

    # time
    'modified_date',
    'release_year',
    'epoch',

    # media assets
    'thumbnails',

    # contents
    'entries',

    # urls / extractor
    'webpage_url',
    'webpage_url_basename',
    'webpage_url_domain',
    'original_url',
    'extractor',
    'extractor_key',
]

PL_END = [
    # custom fields
    'info_level',
    'merge_timeline',
]


def reorder_v_infodict(v_info: V_InfoDict) -> None:
    dict_reorder_keys(v_info, V_START, V_END) # type: ignore

def reorder_pl_infodict(pl_info: PL_InfoDict, reorder_v_infos: bool = True):
    if reorder_v_infos:
        for v_info in pl_info['entries']:
            reorder_v_infodict(v_info)
    dict_reorder_keys(pl_info, PL_START, PL_END) # type: ignore
