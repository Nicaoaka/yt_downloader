"""
Membership and order. **The one authoritative document.**

The roster answers "which videos belong to this playlist, in what order" without reading
anything else, so a record whose captures have all been pruned still knows what it contains.
It lives at a fixed path and is the only file that must not be hand-edited; everything else in
a playlist folder can be deleted or corrupted and the record survives.

Two invariants live here and nowhere else:

  - **A video that vanishes from YouTube keeps its row forever** and flips `in_playlist` to
    False. Automatic, and the reason nothing is ever lost.
  - **A video removed through the API loses its row.** That is a deliberate manual act, so it
    is honored and permanent. The removal is recorded on the timeline and the raw captures
    stay on disk, so the record is rebuildable.

`in_playlist` is written by exactly one operation, `fold_flat()`, and derived nowhere else.

Beyond membership, entries carry a little context (`title`, `uploader`, `duration`) so a
playlist can be listed without loading any captures. These are **best-effort and may be
stale**; nothing may depend on them for correctness.
"""
from __future__ import annotations

__all__ = ['RosterEntry', 'Roster', 'fold_flat']  # noqa: RUF022

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from typing import Any

from pldl2.model.epoch import Epoch
from pldl2.model.infodicts import PL_ID, V_ID, UnavailableMsg
from pldl2.model.schema import SCHEMA_VERSION
from pldl2.model.timeline import PlaylistTimeline


@dataclass(frozen=True, slots=True, kw_only=True)
class RosterEntry:
    """One video's membership record. Order is positional, given by `Roster.entries`."""

    id: V_ID
    in_playlist: bool = True
    """Present in the most recent flat extraction. False means gone from YouTube, not removed."""
    first_seen: Epoch = Epoch(0)
    last_seen: Epoch = Epoch(0)
    """The last flat extraction that still listed this video."""
    unavailable_msgs: tuple[UnavailableMsg, ...] = ()

    # ---- best-effort context ----
    # Last known values, kept so a playlist can be listed with no captures on disk. They go
    # stale when a video is renamed upstream and are never authoritative for anything.
    title: str | None = None
    uploader: str | None = None
    duration: int | None = None

    def __post_init__(self) -> None:
        for name in ('first_seen', 'last_seen'):
            value = getattr(self, name)
            if not isinstance(value, Epoch):
                object.__setattr__(self, name, Epoch(value))


@dataclass(frozen=True, slots=True, kw_only=True)
class Roster:
    """Membership, order and the merge timeline for one playlist.

    Frozen: every mutation returns a new Roster, which is what lets a commit be atomic -- the
    version on disk is either the old one or the new one, never half applied.
    """

    id: PL_ID
    updated: Epoch = Epoch(0)
    entries: tuple[RosterEntry, ...] = ()
    timeline: PlaylistTimeline = field(default_factory=dict)
    schema_version: int = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.updated, Epoch):
            object.__setattr__(self, 'updated', Epoch(self.updated))

    # ---- queries ----

    def __len__(self) -> int:
        return len(self.entries)

    def __contains__(self, v_id: object) -> bool:
        return any(e.id == v_id for e in self.entries)

    def ids(self, *, in_playlist: bool | None = None) -> tuple[V_ID, ...]:
        """Video ids in playlist order.

        Setting `in_playlist` to:
            `True` returns the videos that are still in the YouTube playlist,
            `False` returns videos in the record that are not found in the YouTube playlist,
            `None` (default) returns all ids in the record.
        """
        return tuple(e.id for e in self.entries
                     if in_playlist is None or e.in_playlist is in_playlist)

    def get(self, v_id: V_ID) -> RosterEntry | None:
        for entry in self.entries:
            if entry.id == v_id:
                return entry
        return None

    def index_of(self, v_id: V_ID) -> int | None:
        """Index of a video in the record. Standard 0-indexed, `None` when absent.

        User-facing 1-based positions, including negatives, are edit/'s vocabulary; this is
        the internal index the entries tuple actually uses.
        """
        for i, entry in enumerate(self.entries):
            if entry.id == v_id:
                return i
        return None

    # ---- mutation ----

    def with_entries(self, entries: Iterable[RosterEntry], *,
                     updated: int | None = None) -> Roster:
        """A copy carrying a new entry sequence."""
        return replace(self, entries=tuple(entries),
                       updated=self.updated if updated is None else Epoch(updated))

    def with_timeline(self, timeline: PlaylistTimeline) -> Roster:
        return replace(self, timeline=dict(timeline))


def _context(info: Mapping[str, Any] | None) -> dict[str, Any]:
    """Best-effort context out of a flat entry. Absent keys stay absent, never None-ing a
    value that is already known."""
    if not info:
        return {}
    found = {
        'title': info.get('title'),
        'uploader': info.get('uploader') or info.get('channel') or info.get('creator'),
        'duration': info.get('duration'),
    }
    return {k: v for k, v in found.items() if v is not None}


def fold_flat(
    roster: Roster,
    present_ids: Sequence[V_ID],
    epoch: int,
    *,
    infos: Mapping[V_ID, Mapping[str, Any]] | None = None,
    order: Sequence[V_ID] | None = None,
) -> Roster:
    """Fold one flat extraction into the roster. **The only writer of `in_playlist`.**

    - ids in `present_ids` get `in_playlist=True` and `last_seen=epoch`
    - ids absent from it get `in_playlist=False` and **keep their row and their last_seen**
    - ids not yet known are added, with `first_seen=last_seen=epoch`

    `infos` maps an id to its flat entry, and supplies the best-effort context fields. A key
    missing from an entry leaves the previously known value alone rather than clearing it.

    `order` is the reconciled playlist order, computed by merge/ordering across every snapshot
    seen so far. It is passed in rather than computed here because reconciling disagreeing
    orders is an L1 concern. When omitted, existing order is preserved and genuinely new ids
    are appended in `present_ids` order -- correct for a first run and for an append-only
    playlist, and the caller is expected to supply `order` otherwise.

    Removing a video is *not* expressible here: an id vanishing from `present_ids` flips the
    flag and never drops the row. Dropping a row is edit/'s job, on an explicit request only.
    """
    epoch = Epoch(epoch)
    infos = infos or {}
    present = set(present_ids)
    by_id = {e.id: e for e in roster.entries}

    folded: dict[V_ID, RosterEntry] = {}
    for v_id, entry in by_id.items():
        if v_id in present:
            folded[v_id] = replace(
                entry,
                in_playlist=True,
                last_seen=Epoch(max(entry.last_seen, epoch)),
                first_seen=entry.first_seen or epoch,
                **_context(infos.get(v_id)),
            )
        else:
            folded[v_id] = replace(entry, in_playlist=False)

    for v_id in present_ids:
        if v_id not in folded:
            folded[v_id] = RosterEntry(
                id=v_id,
                in_playlist=True,
                first_seen=epoch,
                last_seen=epoch,
                **_context(infos.get(v_id)),
            )

    if order is None:
        sequence = [e.id for e in roster.entries] + [i for i in present_ids if i not in by_id]
    else:
        # Anything the reconciled order omits is still ours to keep -- never drop a row.
        sequence = list(order) + [v_id for v_id in folded if v_id not in set(order)]

    seen: set[V_ID] = set()
    entries: list[RosterEntry] = []
    for v_id in sequence:
        if v_id in folded and v_id not in seen:
            entries.append(folded[v_id])
            seen.add(v_id)
    return roster.with_entries(entries, updated=max(roster.updated, epoch))
