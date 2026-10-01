"""
Fold every infodict known for one video into one merged info, plus its timeline.

    merge_v_infos(
        v_entries: Sequence[VideoEntry],
        *,
        merge_updater_map: MergeUpdaterMap = COMMON_UPDATER,
        tl_update_filter: TimelineUpdateFilter = COMMON_TIMELINE_KEYS.__contains__,
        init_v_entry: VideoEntry | None = None,        # a previous merge to continue from
        init_v_timeline: VideoTimeline | None = None,  # ...and its timeline
        sort_key: Callable[[VideoEntry], Any] | None = chronological,
    ) -> tuple[VideoEntry, VideoTimeline]

# ---- the fold ----

The working state is `merged: dict[str, Candidate]` -- one value per key, each carrying the
`Rank` of the source that supplied it. Inputs are folded **oldest first** by default: the
final values do not depend on the order, but the timeline records only values that were
current at some point, so any other order loses intermediate states. `sort_key=None` folds
them as given, for a caller that has already decided.

Per input, per key:

1.  `changed = apply_updater(merged, key, Candidate(value, rank), table[key])`. The updater is
    a binary operator over the current and incoming candidates; `apply_updater` owns the get,
    the write and the "did it change" comparison, and is the only thing that touches `merged`.
    A key the input lacks arrives as `NO_VALUE`, distinct from `None`: absent means "this
    extractor did not say", `None` means "it said nothing is there".
2.  If it changed and `tl_update_filter(key)`, a `FieldUpdate` goes on this instant's entry.

The fold has no business logic of its own. v1 computed a per-key `is_latest` here for the
updaters; that number is now the current candidate's rank, stored where it is used.

Iterate keys **sorted**. The set union of two dicts' keys iterates in hash order, which varies
between processes, and that is enough to make two runs over identical inputs write different
bytes. "Same inputs, byte-identical output" is a test.

# ---- what the fold owns rather than the updater ----

The table sees `VideoEntry.data` and nothing else. The envelope fields are merged
structurally by the fold and are not configurable: `id` is the grouping key, `playlist_epoch`
is the newest seen, and the two below have rules of their own.

- **Level** only ever rises. Every entry records the level the record had reached after its
  instant; when that instant raised it, `prev_info_level` says from where, and that is what
  `is_better_info` reads.
- **Unavailability** accumulates. Every report is kept -- YouTube saying "private" and a
  mirror saying "not archived" are two facts, not a conflict -- deduplicated on content. A
  report is placed on the timeline at *its own* epoch, which is when the failure happened, not
  when the capture that carries it was written.

# ---- the timeline ----

One entry per instant that contributed something. An entry that ends up empty is dropped: a
refresh that taught nothing new should leave no trace, since the timeline records change and
not that a session ran.

**Entries already on the timeline are read-only.** Stamp only the entry for the instant being
folded now. Reaching back to restamp older entries with the current level rewrites history in
every file it touches, and it is the single most damaging thing this fold can get wrong.
"""
from __future__ import annotations

__all__ = ['merge_v_infos', 'chronological', 'REMOVED']  # noqa: RUF022

from collections.abc import Callable, Sequence
from typing import Any, Final

from pldl.merge.updaters import (
    COMMON_TIMELINE_KEYS,
    COMMON_UPDATER,
    NO_VALUE,
    Candidate,
    MergeUpdaterMap,
    TimelineUpdateFilter,
    apply_updater,
    unwrap_candidates,
    wrap_candidates,
)
from pldl.downloader import Rank, UnavailableInfo, V_InfoLevel, VideoEntry
from pldl.model import Epoch
from pldl.roster import FieldUpdate, MergeTimelineEntry, VideoTimeline

REMOVED: Final = '<removed>'
"""How a `FieldUpdate` renders a key the winning source lacked. `str(None)` is taken."""


def chronological(entry: VideoEntry) -> Rank:
    """The default fold order: `model.rank`, oldest first."""
    return entry.rank


def _render(value: Any) -> str:
    return REMOVED if value is NO_VALUE else str(value)


def _unavailable_sort_key(info: UnavailableInfo) -> tuple:
    return (int(info.epoch) if info.epoch is not None else -1, info.extractor, info.msg or '')


def merge_v_infos(
    v_entries: Sequence[VideoEntry],
    *,
    merge_updater_map: MergeUpdaterMap = COMMON_UPDATER,
    tl_update_filter: TimelineUpdateFilter = COMMON_TIMELINE_KEYS.__contains__,
    init_v_entry: VideoEntry | None = None,
    init_v_timeline: VideoTimeline | None = None,
    sort_key: Callable[[VideoEntry], Any] | None = chronological,
) -> tuple[VideoEntry, VideoTimeline]:
    """Fold `v_entries` -- all for one video -- into one entry and its timeline.

    With `init_v_entry`, continues a previous merge: its values seed the fold at its own rank,
    its level is the floor, and `init_v_timeline` is returned with new entries appended and
    old ones untouched. Given no new entries, the previous merge comes back as it was.
    """
    timeline = init_v_timeline if init_v_timeline is not None else VideoTimeline()

    if not v_entries:
        if init_v_entry is not None:
            return init_v_entry, timeline
        raise ValueError('Expected at least one v_entry')

    v_ids = sorted({e.id for e in (*v_entries, init_v_entry) if e is not None})
    if len(v_ids) > 1:
        raise ValueError(f'Found multiple video ids: {v_ids}')
    v_id = v_ids[0]

    if sort_key is not None:
        v_entries = sorted(v_entries, key=sort_key)

    # ---- the accumulator: plain mutable state, one frozen VideoEntry at the end ----
    merged: dict[str, Candidate] = {}
    level = V_InfoLevel.NONE
    unavailable: set[UnavailableInfo] = set()
    playlist_epoch: Epoch | None = None
    if init_v_entry is not None:
        merged = wrap_candidates(dict(init_v_entry.data), init_v_entry.rank)
        level = init_v_entry.info_level
        unavailable = set(init_v_entry.unavailable_infos)
        playlist_epoch = init_v_entry.playlist_epoch

    timeline_entries: list[MergeTimelineEntry] = []
    for src in v_entries:
        rank = src.rank

        updates: list[FieldUpdate] = []
        for key in sorted(merged.keys() | src.data.keys()):
            incoming = Candidate(src.data.get(key, NO_VALUE), rank)
            if apply_updater(merged, key, incoming, merge_updater_map[key]) and tl_update_filter(key):
                updates.append(FieldUpdate(field=key, value=_render(merged[key].value)))

        prev_level, level = level, max(level, src.info_level)
        timeline_entries.append(MergeTimelineEntry(
            epoch=src.epoch,
            info_level=level,
            prev_info_level=prev_level if level > prev_level else None,
            updates=tuple(updates),
        ))

        # A report sits at the moment it happened, which need not be this capture's epoch.
        for info in src.unavailable_infos:
            unavailable.add(info)
            timeline_entries.append(MergeTimelineEntry(
                epoch=info.epoch if info.epoch is not None else src.epoch,
                unavailable_infos=(info,),
            ))

        # weirdly excluded from MergeTimelineEntry. (it could technically be derived)
        if src.playlist_epoch is not None:
            playlist_epoch = (src.playlist_epoch if playlist_epoch is None
                              else max(playlist_epoch, src.playlist_epoch))

    timeline = timeline.extend(e for e in timeline_entries if not e.is_empty())

    return VideoEntry(
        id=v_id,
        info_level=level,
        data=unwrap_candidates(merged),
        unavailable_infos=tuple(sorted(unavailable, key=_unavailable_sort_key)),
        playlist_epoch=playlist_epoch,
    ), timeline
