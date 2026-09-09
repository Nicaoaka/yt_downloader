"""
What the record learned about a video, and when.

A `VideoTimeline` is an append-only, chronological log. Each `MergeTimelineEntry` says what
one instant contributed: fields whose value improved, a level promotion, unavailability
reported by an extractor, and manipulations made through the API.

Entries are ordered by `(epoch, info_level)` -- chronological, with the level as a
deterministic tiebreak for the rare case of two extractions in the same second. **Not** by
merge priority: this records when things happened, while merge priority decides which value
wins a field. Sorting history by priority makes a newer, poorer extraction appear before an
older, richer one, and the reading order stops matching the order of events.

Several entries may share an epoch, since two different things can happen in one second.
Identical entries collapse, which is why everything here is hashable.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'BetterInfo', 'FieldUpdate', 'Manipulation', 'ManipulationKind',
    'MergeTimelineEntry', 'VideoTimeline', 'PlaylistTimeline',
]

from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
from enum import StrEnum, auto

from pldl2.model.epoch import Epoch
from pldl2.model.infodicts import V_ID
from pldl2.model.levels import V_InfoLevel


@dataclass(frozen=True, slots=True, kw_only=True)
class BetterInfo:
    """A level promotion recorded at one epoch."""

    from_level: V_InfoLevel
    to_level: V_InfoLevel

    def render(self) -> str:
        """The human-readable form, written alongside the structured fields.

        Free to change format because nothing parses it back.
        """
        return f'{self.from_level.name} -> {self.to_level.name}'


@dataclass(frozen=True, slots=True, kw_only=True)
class FieldUpdate:
    """One field of the merged infodict taking a new value."""

    field: str
    value: str

    def render(self) -> str:
        return f'{self.field}={self.value}'


class ManipulationKind(StrEnum):
    REMOVE = auto()
    INSERT = auto()
    REPLACE = auto()
    MOVE = auto()


@dataclass(frozen=True, slots=True, kw_only=True)
class Manipulation:
    """A membership or order change made deliberately through the API.

    Kept separate from `FieldUpdate` because the two answer different questions. An update
    means YouTube's data changed; a manipulation means *you* changed the record. Merging them
    into one bag leaves a reader unable to tell a title change upstream from an edit here.
    """

    kind: ManipulationKind
    detail: str = ''
    """Free-form specifics, e.g. `to=1` or `from=b to=c`."""

    def render(self) -> str:
        return f'<{self.kind.upper()}{" " + self.detail if self.detail else ""}>'


@dataclass(frozen=True, slots=True, kw_only=True)
class MergeTimelineEntry:
    """What one instant contributed to what is known about one video."""

    epoch: Epoch
    info_level: V_InfoLevel | None = None
    better_info: BetterInfo | None = None
    unavailable: tuple[str, ...] = ()
    updates: tuple[FieldUpdate, ...] = ()
    manipulations: tuple[Manipulation, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.epoch, Epoch):
            object.__setattr__(self, 'epoch', Epoch(self.epoch))

    def is_empty(self) -> bool:
        """True when the entry records nothing and should not be kept.

        A refresh that teaches nothing new produces one of these, and dropping it is correct:
        the timeline records what changed, not that a session ran.
        """
        return not (self.updates or self.unavailable or self.better_info or self.manipulations)

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
            self.unavailable,
            tuple(m.kind for m in self.manipulations),
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
