"""
L0. The vocabulary: types, levels, epochs, ranking, timeline, kinds, errors.

**Imports nothing from pldl2 outside this package.** No I/O, printing, or network responsibilities
prevents cycles with other subpackages.

The `InfoKind` constants are deliberately not re-exported here, because `ROSTER` means nothing
on its own. Reach them through the module:

    from pldl2.model import kinds
    kinds.ROSTER, kinds.RAW_FLAT
"""
from __future__ import annotations

from pldl2.model.downloads import DL_Action, DL_Result
from pldl2.model.epoch import (
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
from pldl2.model.errors import (
    Classification,
    ErrorClass,
    Issue,
    Severity,
    UnavailableInfo,
    classify,
)
from pldl2.model.infodicts import (
    NO_VALUE,
    PL_ID,
    V_ID,
    ANY_InfoDict,
    PL_InfoDict,
    V_InfoDict,
    YT_DLP_DownloadArchive,
    YT_DLP_DownloadArchive_IDs,
    YT_DLP_InfoDict,
)
from pldl2.model.kinds import (
    KINDS,
    PLDL_OWNED,
    USER_OWNED,
    InfoKind,
    KindName,
    Owner,
    PayloadShape,
)
from pldl2.model.levels import (
    PL_InfoLevel,
    Rank,
    V_InfoLevel,
    coerce_pl_level,
    coerce_v_level,
    derive_pl_info_level,
    derive_v_info_level,
    info_rank,
    pl_level_mismatch,
    rank,
    v_level_mismatch,
)
from pldl2.model.manipulations import Manipulation, ManipulationKind, ManipulationLog
from pldl2.model.metadata import (
    ARCHIVE_FILENAME,
    METADATA_FILENAME,
    PLAYLISTS_INDEX_FILENAME,
    ROSTER_FILENAME,
    Metadata,
    Paths,
    SessionLog,
    VideoLog,
)
from pldl2.model.playlists import Capture, MergePlaylist
from pldl2.model.roster import (
    PLAYLIST_CONTEXT_SOURCES,
    VIDEO_CONTEXT_SOURCES,
    PlaylistContext,
    Roster,
    RosterEntry,
    VideoContext,
)
from pldl2.model.schema import LEGACY_SCHEMA_VERSION, SCHEMA_VERSION
from pldl2.model.timeline import (
    FieldUpdate,
    MergeTimelineEntry,
    PlaylistTimeline,
    VideoTimeline,
)
from pldl2.model.videos import VideoEntry

__all__ = [  # noqa: RUF022 - grouped by concept, which is how these are looked up
    # schema
    'SCHEMA_VERSION', 'LEGACY_SCHEMA_VERSION',

    # infodicts + aliases
    'V_ID', 'PL_ID',
    'YT_DLP_InfoDict', 'V_InfoDict', 'PL_InfoDict', 'ANY_InfoDict',
    'YT_DLP_DownloadArchive', 'YT_DLP_DownloadArchive_IDs',
    'NO_VALUE',

    # download control
    'DL_Action', 'DL_Result',

    # levels + ranking
    'V_InfoLevel', 'PL_InfoLevel',
    'coerce_v_level', 'coerce_pl_level',
    'derive_v_info_level', 'derive_pl_info_level',
    'v_level_mismatch', 'pl_level_mismatch',
    'Rank', 'rank', 'info_rank',

    # time
    'Epoch', 'EPOCH_ZERO', 'get_epoch', 'get_latest_epoch',
    'to_iso', 'from_iso', 'to_file_stamp',
    'to_v1_readable_epoch', 'from_v1_readable_epoch',

    # timeline
    'FieldUpdate', 'MergeTimelineEntry', 'VideoTimeline', 'PlaylistTimeline',

    # manipulations
    'Manipulation', 'ManipulationKind', 'ManipulationLog',

    # envelopes
    'VideoEntry', 'Capture', 'MergePlaylist',

    # roster
    'Roster', 'RosterEntry', 'VideoContext', 'PlaylistContext',
    'VIDEO_CONTEXT_SOURCES', 'PLAYLIST_CONTEXT_SOURCES',

    # metadata
    'Metadata', 'Paths', 'SessionLog', 'VideoLog',
    'ROSTER_FILENAME', 'METADATA_FILENAME', 'ARCHIVE_FILENAME', 'PLAYLISTS_INDEX_FILENAME',

    # kinds
    'InfoKind', 'KindName', 'Owner', 'PayloadShape',
    'KINDS', 'USER_OWNED', 'PLDL_OWNED',

    # errors
    'ErrorClass', 'Classification', 'classify', 'UnavailableInfo', 'Issue', 'Severity',
]
