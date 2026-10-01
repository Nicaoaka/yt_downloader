"""
The vocabulary: types, levels, epochs, ranking, timeline, errors.

**Imports nothing from pldl outside this package.** No I/O, printing, or network responsibilities
prevents cycles with other subpackages.
"""
from __future__ import annotations

from pldl.model.epoch import (
    EPOCH_ZERO,
    Epoch,
    from_iso,
    from_v1_readable_epoch,
    get_epoch,
    get_latest_epoch,
    to_file_stamp,
    to_iso,
    to_v1_readable_epoch,
)
from pldl.model.errors import ErrorClass, UnavailableInfo
from pldl.model.infodicts import (
    NO_VALUE,
    PL_ID,
    V_ID,
    ANY_InfoDict,
    PL_InfoDict,
    V_InfoDict,
    YT_DLP_InfoDict,
)
from pldl.model.levels import (
    PL_InfoLevel,
    Rank,
    V_InfoLevel,
    coerce_v_level,
    derive_v_info_level,
    rank,
)
from pldl.model.playlists import Capture, MergePlaylist
from pldl.model.roster import (
    PLAYLIST_CONTEXT_SOURCES,
    VIDEO_CONTEXT_SOURCES,
    PlaylistContext,
    Roster,
    RosterEntry,
    VideoContext,
)
from pldl.model.schema import LEGACY_SCHEMA_VERSION, SCHEMA_VERSION
from pldl.model.timeline import (
    FieldUpdate,
    MergeTimelineEntry,
    PlaylistTimeline,
    VideoTimeline,
)
from pldl.model.videos import VideoEntry

__all__ = [  # noqa: RUF022 - grouped by concept, which is how these are looked up
    # schema
    'SCHEMA_VERSION', 'LEGACY_SCHEMA_VERSION',

    # infodicts + aliases
    'V_ID', 'PL_ID',
    'YT_DLP_InfoDict', 'V_InfoDict', 'PL_InfoDict', 'ANY_InfoDict',
    'NO_VALUE',

    # levels + ranking
    'V_InfoLevel', 'PL_InfoLevel',
    'coerce_v_level', 'derive_v_info_level',
    'Rank', 'rank',

    # time
    'Epoch', 'EPOCH_ZERO', 'get_epoch', 'get_latest_epoch',
    'to_iso', 'from_iso', 'to_file_stamp',
    'to_v1_readable_epoch', 'from_v1_readable_epoch',

    # timeline
    'FieldUpdate', 'MergeTimelineEntry', 'VideoTimeline', 'PlaylistTimeline',

    # envelopes
    'VideoEntry', 'Capture', 'MergePlaylist',

    # roster
    'Roster', 'RosterEntry', 'VideoContext', 'PlaylistContext',
    'VIDEO_CONTEXT_SOURCES', 'PLAYLIST_CONTEXT_SOURCES',

    # errors
    'ErrorClass', 'UnavailableInfo',
]
