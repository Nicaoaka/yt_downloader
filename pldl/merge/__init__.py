"""
Fold many infodicts into one. Pure: no I/O, no printing, no network.

A merge answers three separate questions, and keeping them apart is what the stage is for:

| Question                                  | Mechanism                                    |
|-------------------------------------------|----------------------------------------------|
| In what order did things happen?          | `rank(epoch, level)` -- chronological        |
| Which value wins a field?                 | a **field resolver**, per field              |
| Which of those changes is worth recording?| a **timeline filter**, per field             |

They cannot be collapsed into one rule. Only a per-field rule can say "a view count only ever
goes up" or "never overwrite a title with nothing". And a single global "richer source wins"
ordering would empty the timeline: if an old full extraction outranks every later refresh,
almost no field registers as changed, and a record whose purpose is showing change over time
stops showing any. Folding chronologically produces the opposite problem -- a timeline
saturated with every `view_count` tick -- and that is exactly what the timeline filter is for.

    ordering.py   reconcile disagreeing snapshot orders into one playlist order
    updaters.py   the merge updaters and timeline filters, and the tables that pick one
    videos.py     fold per-video infodicts into one video's merged info + timeline
    playlists.py  MergePlaylist; fold playlist-level infodicts, drive videos.py across the
                  entries, and resolve the roster's context -- which is a merge, so it lives here

Everything here takes values and returns values. `merge_pl_infos` returns a `MergeReport`
rather than writing anything; what to persist is the caller's decision.
"""
from __future__ import annotations

from pldl.merge.ordering import merge_ordered_lists
from pldl.merge.playlists import (
    MergePlaylist,
    MergeReport,
    PL_InfoLevel,
    merge_pl_infos,
    update_roster,
)
from pldl.merge.updaters import (
    COMMON_TIMELINE_KEYS,
    COMMON_UPDATER,
    NO_VALUE,
    PL_UPDATER,
    ROSTER_UPDATER,
    Candidate,
    MergeUpdater,
    MergeUpdaterMap,
    TimelineUpdateFilter,
    fill_absent,
    keep,
    latest,
    latest_not_none,
    maximum,
    richest_latest,
    richest_latest_not_none,
)
from pldl.merge.videos import merge_v_infos

__all__ = [  # noqa: RUF022
    'merge_v_infos', 'merge_pl_infos', 'update_roster', 'merge_ordered_lists',
    'MergePlaylist', 'MergeReport', 'PL_InfoLevel',
    'NO_VALUE', 'Candidate', 'MergeUpdater', 'MergeUpdaterMap', 'TimelineUpdateFilter',
    'keep', 'latest', 'latest_not_none', 'fill_absent', 'maximum',
    'richest_latest', 'richest_latest_not_none',
    'COMMON_UPDATER', 'ROSTER_UPDATER', 'PL_UPDATER', 'COMMON_TIMELINE_KEYS',
]
