"""
The merge timeline: what the record learned about a video, and when.

Two structural changes from v1, each closing a confirmed defect.

**better_info is structured.** v1 stored the string "FLAT -> EXTRACT" and display.py:234
regexed it back into an enum to render it -- the old code self-documents this as
`# this is very fragile, but it'll work`. Here the levels are fields; the string is produced
by `BetterInfo.render()` for the human reading the file and is **never parsed back**.

**A timeline is an ordered sequence, not a dict keyed by a local-time string.** v1 keyed
entries by `to_readable_epoch(...)`, which is not injective across the DST fall-back hour, so
two distinct extractions an hour apart silently merged into one entry in a file that is never
rewritten (issue-1 #17). Entries now carry a canonical int `epoch` plus a readable `at`, and
the container is a tuple ordered by epoch. The collision is not handled better -- it cannot
occur.

**Entries are immutable once written.** `MergeTimelineEntry` is frozen, which is the type-level
half of issue-1 #6: v1's `_merge_v_infos` unconditionally stamped *today's* merged info_level
onto pre-existing entries (merge_infos.py:92), so a month-old FLAT entry read EXTRACT after
the next merge, entries reordered under the level-first sort key, and the flat step vanished
from the rendered strip. The behavioural half -- stamping only the entry being folded now --
belongs to merge/, and this type makes violating it require an explicit `replace()`.
"""
from __future__ import annotations

__all__ = [
    'BetterInfo', 'MergeTimelineEntry',
    'VideoTimeline', 'PlaylistTimeline',
    'entry_for', 'upsert', 'ordered',
]

from collections.abc import Mapping
from dataclasses import dataclass, field, replace

from pldl2.model.epoch import to_iso
from pldl2.model.infodicts import V_ID
from pldl2.model.levels import V_InfoLevel


@dataclass(frozen=True, slots=True, kw_only=True)
class BetterInfo:
    """A level promotion recorded at one epoch."""
    from_level: V_InfoLevel
    to_level: V_InfoLevel

    def render(self) -> str:
        """The human-readable form written alongside the structured fields.

        Output only. Nothing reads this back -- that is the entire point.
        """
        return f'{self.from_level.name} -> {self.to_level.name}'


@dataclass(frozen=True, slots=True, kw_only=True)
class MergeTimelineEntry:
    """What one merge pass learned about one video at one instant.

    `updates` maps a field name to its new value, rendered as a string. Manual edits go here
    too, under the **same** key: v1's `_add_update_to_merge_timeline` wrote a singular
    `'update'` string while every reader looked for the plural `'updates'` dict, so its dedup
    guard never fired and two edits in the same second overwrote each other (issue-1 #11).
    """
    epoch: int
    info_level: V_InfoLevel | None = None
    better_info: BetterInfo | None = None
    unavailable: tuple[str, ...] = ()
    updates: Mapping[str, str] = field(default_factory=dict)

    @property
    def at(self) -> str:
        """Readable local time with its offset. Derived, never stored separately in memory."""
        return to_iso(self.epoch)

    def is_empty(self) -> bool:
        """True when the entry records nothing and should not be kept."""
        return not (self.updates or self.unavailable or self.better_info)


type VideoTimeline = tuple[MergeTimelineEntry, ...]
type PlaylistTimeline = Mapping[V_ID, VideoTimeline]


def ordered(timeline: VideoTimeline) -> VideoTimeline:
    """Entries oldest-first. The canonical on-disk and in-memory order."""
    return tuple(sorted(timeline, key=lambda e: e.epoch))


def entry_for(timeline: VideoTimeline, epoch: int) -> MergeTimelineEntry | None:
    """The entry at exactly this epoch, if any."""
    for entry in timeline:
        if entry.epoch == epoch:
            return entry
    return None


def upsert(timeline: VideoTimeline, entry: MergeTimelineEntry) -> VideoTimeline:
    """Return a new timeline with `entry` inserted, or merged into the one at its epoch.

    Merging unions `updates` and `unavailable` rather than replacing them, so two edits in
    the same second accumulate. Existing `info_level` and `better_info` are **kept** unless
    the incoming entry supplies them: an older entry's recorded level is history and must not
    move (issue-1 #6).
    """
    existing = entry_for(timeline, entry.epoch)
    if existing is None:
        return ordered((*timeline, entry))

    merged = replace(
        existing,
        info_level=existing.info_level if existing.info_level is not None else entry.info_level,
        better_info=existing.better_info if existing.better_info is not None else entry.better_info,
        unavailable=existing.unavailable + tuple(
            m for m in entry.unavailable if m not in existing.unavailable),
        updates={**existing.updates, **entry.updates},
    )
    return ordered(tuple(e for e in timeline if e.epoch != entry.epoch) + (merged,))
