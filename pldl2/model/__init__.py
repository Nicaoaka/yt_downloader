"""
L0. The vocabulary: types, levels, epochs, ranking, timeline, kinds, errors.

**Imports nothing from pldl2 outside this package, and nothing from pldl at all.** No I/O, no
printing, no network. That constraint is the reason both of v1's import cycles are impossible
to reintroduce here:

  - `config -> playlist_dl -> config` existed because `PlaylistDL_Config.__post_init__` reached
    into the orchestrator to borrow a validator. Validation is data-shaped now, and lives
    below everything that could want it.
  - `merge_infos <-> reorder_infodict_keys` existed because both needed the private
    `_merge_v_sort_key` and each imported the other lazily to get at it. It is `rank()` in
    levels.py now, and everyone imports it normally.

Two shapes, split at the envelope boundary. **TypedDict for the yt-dlp payload** -- foreign
data with ~140 optional keys whose shape changes between releases, where an unknown key must
flow through untouched. **Frozen dataclasses for pldl's own structures** -- ours to define, so
we get defaults, invariants, `replace()`, real equality, and a field-name typo that is an
error instead of a silently created dict key.
"""
from __future__ import annotations

from pldl2.model.envelope import Capture, VideoEntry
from pldl2.model.epoch import (
    epoch_now,
    from_iso,
    from_legacy_key,
    get_epoch,
    get_latest_epoch,
    to_file_stamp,
    to_iso,
    to_legacy_key,
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
from pldl2.model.kinds import KINDS, InfoKind, Owner, PayloadShape, by_name, pldl_owned, user_owned
from pldl2.model.levels import (
    PL_InfoLevel,
    V_InfoLevel,
    coerce_pl_level,
    coerce_v_level,
    derive_pl_info_level,
    derive_v_info_level,
    level_mismatch,
    pl_level_mismatch,
    rank,
    rank_of,
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
    MergeTimelineEntry,
    PlaylistTimeline,
    VideoTimeline,
    entry_for,
    ordered,
    upsert,
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
    'level_mismatch', 'pl_level_mismatch',
    'rank', 'rank_of',

    # time
    'epoch_now', 'get_epoch', 'get_latest_epoch',
    'to_iso', 'from_iso', 'to_file_stamp',
    'to_legacy_key', 'from_legacy_key',

    # timeline
    'BetterInfo', 'MergeTimelineEntry', 'VideoTimeline', 'PlaylistTimeline',
    'entry_for', 'upsert', 'ordered',

    # envelope
    'VideoEntry', 'Capture',

    # roster
    'Roster', 'RosterEntry', 'fold_flat',

    # metadata
    'Metadata', 'Paths', 'HistoryEntry', 'HistoryVideo',
    'ROSTER_FILENAME', 'METADATA_FILENAME', 'ARCHIVE_FILENAME', 'PLAYLISTS_INDEX_FILENAME',

    # kinds
    'InfoKind', 'Owner', 'PayloadShape', 'KINDS', 'by_name', 'user_owned', 'pldl_owned',

    # errors
    'ErrorClass', 'Classification', 'classify', 'Issue', 'Severity',
]
