"""
L0. The vocabulary: types, levels, epochs, ranking, timeline, kinds, errors.

**Imports nothing from pldl2 outside this package.** No I/O, no printing, no network. Sitting
below everything is what keeps it free of the cycles that a shared concept with no home tends
to create.

Two shapes, split at the envelope boundary. **TypedDict for the yt-dlp payload** -- foreign
data with hundreds of optional keys whose shape changes between releases, where an unknown key
must flow through untouched. **Frozen dataclasses for pldl's own structures** -- ours to
define, so they get defaults, invariants, `replace()`, real equality, and a field-name typo
that is an error rather than a silently created dict key.

The `InfoKind` constants are deliberately not re-exported here, because `ROSTER` means nothing
on its own. Reach them through the module:

    from pldl2.model import kinds
    kinds.ROSTER, kinds.RAW_FLAT
"""
from __future__ import annotations

from pldl2.model.envelope import Capture, VideoEntry
from pldl2.model.epoch import (
    Epoch,
    epoch_now,
    from_iso,
    get_epoch,
    get_latest_epoch,
    to_file_stamp,
    to_iso,
    v1_from_readable_epoch,
    v1_to_readable_epoch,
)
from pldl2.model.errors import Classification, ErrorClass, Issue, Severity, classify
from pldl2.model.infodicts import (
    ANY_InfoDict,
    DL_Action,
    DL_Result,
    DownloadInfo,
    ID_DownloadInfo,
    NO_VALUE,
    PL_ID,
    PL_DownloadInfo,
    PL_InfoDict,
    UnavailableMsg,
    V_ID,
    V_InfoDict,
    YT_DLP_DownloadArchive,
    YT_DLP_DownloadArchive_IDs,
    YT_DLP_InfoDict,
)
from pldl2.model.kinds import (
    KINDS,
    PATH_TEMPLATE_KEYS,
    InfoKind,
    KindName,
    Owner,
    PayloadShape,
    by_name,
    pldl_owned,
    user_owned,
)
from pldl2.model.levels import (
    PL_InfoLevel,
    V_InfoLevel,
    coerce_pl_level,
    coerce_v_level,
    derive_pl_info_level,
    derive_v_info_level,
    pl_level_mismatch,
    rank,
    rank_of,
    v_level_mismatch,
)
from pldl2.model.metadata import (
    ARCHIVE_FILENAME,
    METADATA_FILENAME,
    PLAYLISTS_INDEX_FILENAME,
    ROSTER_FILENAME,
    HistoryEntry,
    HistoryVideo,
    Metadata,
    Paths,
)
from pldl2.model.roster import Roster, RosterEntry, fold_flat
from pldl2.model.schema import LEGACY_SCHEMA_VERSION, SCHEMA_VERSION
from pldl2.model.timeline import (
    BetterInfo,
    FieldUpdate,
    Manipulation,
    ManipulationKind,
    MergeTimelineEntry,
    PlaylistTimeline,
    VideoTimeline,
)

__all__ = [  # noqa: RUF022 - grouped by concept, which is how these are looked up
    # schema
    'SCHEMA_VERSION', 'LEGACY_SCHEMA_VERSION',

    # infodicts + aliases
    'V_ID', 'PL_ID',
    'YT_DLP_InfoDict', 'V_InfoDict', 'PL_InfoDict', 'ANY_InfoDict',
    'YT_DLP_DownloadArchive', 'YT_DLP_DownloadArchive_IDs',
    'UnavailableMsg', 'NO_VALUE',

    # download control
    'DL_Action', 'DL_Result', 'DownloadInfo', 'PL_DownloadInfo', 'ID_DownloadInfo',

    # levels + ranking
    'V_InfoLevel', 'PL_InfoLevel',
    'coerce_v_level', 'coerce_pl_level',
    'derive_v_info_level', 'derive_pl_info_level',
    'v_level_mismatch', 'pl_level_mismatch',
    'rank', 'rank_of',

    # time
    'Epoch', 'epoch_now', 'get_epoch', 'get_latest_epoch',
    'to_iso', 'from_iso', 'to_file_stamp',
    'v1_to_readable_epoch', 'v1_from_readable_epoch',

    # timeline
    'BetterInfo', 'FieldUpdate', 'Manipulation', 'ManipulationKind',
    'MergeTimelineEntry', 'VideoTimeline', 'PlaylistTimeline',

    # envelope
    'VideoEntry', 'Capture',

    # roster
    'Roster', 'RosterEntry', 'fold_flat',

    # metadata
    'Metadata', 'Paths', 'HistoryEntry', 'HistoryVideo',
    'ROSTER_FILENAME', 'METADATA_FILENAME', 'ARCHIVE_FILENAME', 'PLAYLISTS_INDEX_FILENAME',

    # kinds
    'InfoKind', 'KindName', 'Owner', 'PayloadShape',
    'KINDS', 'PATH_TEMPLATE_KEYS', 'by_name', 'user_owned', 'pldl_owned',

    # errors
    'ErrorClass', 'Classification', 'classify', 'Issue', 'Severity',
]
