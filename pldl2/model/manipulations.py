"""
Deliberate edits to a playlist's membership and order.

Kept apart from the merge timeline because the two answer different questions. A timeline
entry means the upstream data changed; a manipulation means *you* changed the record. Folding
them into one list leaves a reader unable to tell a title change on YouTube from an edit made
here, and would put an empty field on nearly every entry of whichever kind it is not.

The log is chronological and lives on the `Roster` rather than on an entry, so that removing a
video does not remove the evidence that it was removed.
"""
from __future__ import annotations

__all__ = ['ManipulationKind', 'Manipulation', 'ManipulationLog']  # noqa: RUF022

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from enum import StrEnum, auto

from pldl2.model.epoch import Epoch
from pldl2.model.infodicts import V_ID


class ManipulationKind(StrEnum):
    REMOVE = auto()
    INSERT = auto()
    REPLACE = auto()
    MOVE = auto()


@dataclass(frozen=True, slots=True, kw_only=True)
class Manipulation:
    """One edit, recorded permanently.

    Manipulations are honored and not undone by a later refresh, so this log is the only
    record that a removed video was ever a member.
    """

    epoch: Epoch
    kind: ManipulationKind
    v_id: V_ID
    detail: str = ''
    """Free-form specifics, e.g. `to=1` or `from=b to=c`."""

    def __post_init__(self) -> None:
        if not isinstance(self.epoch, Epoch):
            object.__setattr__(self, 'epoch', Epoch(self.epoch))

    def render(self) -> str:
        return f'<{self.kind.upper()} {self.v_id}{" " + self.detail if self.detail else ""}>'

    @property
    def sort_key(self) -> tuple:
        return (int(self.epoch), self.v_id, str(self.kind), self.detail)


@dataclass(frozen=True, slots=True)
class ManipulationLog:
    """Chronological, deduplicated. Every operation returns a new log."""

    entries: tuple[Manipulation, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, 'entries', tuple(sorted(set(self.entries), key=lambda m: m.sort_key)))

    def __iter__(self) -> Iterator[Manipulation]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def add(self, manipulation: Manipulation) -> ManipulationLog:
        return ManipulationLog((*self.entries, manipulation))

    def extend(self, manipulations: Iterable[Manipulation]) -> ManipulationLog:
        return ManipulationLog((*self.entries, *manipulations))

    def for_video(self, v_id: V_ID) -> tuple[Manipulation, ...]:
        """Every edit made to one video, oldest first."""
        return tuple(m for m in self.entries if m.v_id == v_id)
