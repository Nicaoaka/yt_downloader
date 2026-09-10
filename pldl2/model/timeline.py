"""
What the record learned about a video, and when.

A `VideoTimeline` is an append-only, chronological log of what merging discovered. Each
`MergeTimelineEntry` says what one instant contributed: fields whose value improved, the level
the record reached, and any unavailability an extractor reported.

Entries are ordered by `(epoch, info_level)` -- chronological, with the level as a
deterministic tiebreak for two extractions in the same second. **Not** by merge priority: this
records when things happened, while merge priority decides which value wins a field. Sorting
history by priority makes a newer, poorer extraction appear before an older, richer one and the
reading order stops matching the order of events.

Several entries may share an epoch, since two things can happen in one second. Identical
entries collapse, which is why everything here is hashable.

Deliberate edits are **not** here; they are a separate log on the roster (see
`model/manipulations.py`). Merging and manipulating answer different questions, and the vast
majority of entries would carry an empty field for the one they are not.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'FieldUpdate', 'MergeTimelineEntry', 'VideoTimeline', 'PlaylistTimeline',
]

from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass

from pldl2.model.epoch import Epoch
from pldl2.model.errors import UnavailableInfo
from pldl2.model.infodicts import V_ID
from pldl2.model.levels import V_InfoLevel


@dataclass(frozen=True, slots=True, kw_only=True)
class FieldUpdate:
    """One field of the merged infodict taking a new value.

    A named pair rather than a mapping entry: the timeline deduplicates entries, so everything
    on one must be hashable, and a bare `tuple[str, str]` reads badly at every use site.
    """

    field: str
    value: str

    def render(self) -> str:
        return f'{self.field}={self.value}'


@dataclass(frozen=True, slots=True, kw_only=True)
class MergeTimelineEntry:
    """What one instant contributed to what is known about one video."""

    epoch: Epoch
    info_level: V_InfoLevel | None = None
    """The level the record had reached after this instant."""
    prev_info_level: V_InfoLevel | None = None
    """The level it had before. Only set when this instant changed it."""
    unavailable_msgs: tuple[UnavailableInfo, ...] = ()
    updates: tuple[FieldUpdate, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.epoch, Epoch):
            object.__setattr__(self, 'epoch', Epoch(self.epoch))

    @property
    def is_better_info(self) -> bool:
        """True when this instant raised the level."""
        return (self.prev_info_level is not None
                and self.info_level is not None
                and self.info_level > self.prev_info_level)

    def render_better_info(self) -> str | None:
        """`FLAT -> EXTRACT`, or None when the level did not move.

        Output only; nothing parses it back, so the format is free to change.
        """
        if not self.is_better_info:
            return None
        return f'{self.prev_info_level.name} -> {self.info_level.name}'  # type: ignore[union-attr]

    def is_empty(self) -> bool:
        """True when the entry records nothing and should not be kept.

        A refresh that teaches nothing new produces one of these, and dropping it is correct:
        the timeline records what changed, not that a session ran.
        """
        return not (self.updates or self.unavailable_msgs or self.is_better_info)

    @property
    def sort_key(self) -> tuple:
        """Chronological, with level then content as deterministic tiebreaks.

        Without the tiebreaks two entries in the same second would sort by input order, which
        varies with the hash seed and makes the written file differ between runs.
        """
        return (
            int(self.epoch),
            -1 if self.info_level is None else int(self.info_level),
            tuple(u.field for u in self.updates),
            tuple(m.extractor for m in self.unavailable_msgs),
        )


@dataclass(frozen=True, slots=True)
class VideoTimeline:
    """One video's ordered, deduplicated log. Every operation returns a new timeline."""

    entries: tuple[MergeTimelineEntry, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, 'entries', _normalized(self.entries))

    def __iter__(self) -> Iterator[MergeTimelineEntry]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def __getitem__(self, index: int) -> MergeTimelineEntry:
        return self.entries[index]

    def add(self, entry: MergeTimelineEntry) -> VideoTimeline:
        """Append one entry.

        Nothing is replaced. An entry sharing an epoch with an existing one is simply another
        entry, because two distinct things can happen in the same second. An entry identical
        to one already present collapses into it.
        """
        return VideoTimeline((*self.entries, entry))

    def extend(self, entries: Iterable[MergeTimelineEntry]) -> VideoTimeline:
        return VideoTimeline((*self.entries, *entries))

    def at_epoch(self, epoch: int) -> tuple[MergeTimelineEntry, ...]:
        """Every entry recorded at exactly this epoch."""
        return tuple(e for e in self.entries if e.epoch == epoch)

    def levels(self) -> tuple[V_InfoLevel, ...]:
        """Recorded levels, oldest first, skipping entries that record none."""
        return tuple(e.info_level for e in self.entries if e.info_level is not None)


type PlaylistTimeline = Mapping[V_ID, VideoTimeline]


def _normalized(entries: Iterable[MergeTimelineEntry]) -> tuple[MergeTimelineEntry, ...]:
    """Deduplicate, then order. Identical entries collapse; distinct ones all survive."""
    return tuple(sorted(set(entries), key=lambda e: e.sort_key))
