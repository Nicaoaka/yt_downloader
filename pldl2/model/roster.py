"""
The roster: membership and order. **The one authoritative document.**

Replaces v1's `_merge_flat`, renamed because that name sat one word from `merge_info` while
describing something completely different -- and because it stopped being "a merged flat
infodict" the moment it grew fields (`in_playlist`, `first_seen`, `last_seen`) that no flat
extraction has.

It is the only file in a playlist folder that must not be hand-edited, which is what the `_`
in `_roster.json` means: not "pldl wrote it" (pldl writes almost everything) but **"pldl
depends on this"**. Everything under flat/, v_infos/, merges/ and Videos/ may be pruned or
corrupted between runs and the record survives; corrupting the roster is the one
unrecoverable act.

Two invariants live here and nowhere else:

  - **A video that vanishes from YouTube keeps its row forever** and flips `in_playlist` to
    False. This is the "never lose a video" promise, and it is automatic.
  - **A video removed through the API loses its row** (decision 9). That is a deliberate
    manual act, so it is honoured and permanent; the removal is recorded as a timeline event
    and the raw captures stay on disk, so the record is rebuildable if you change your mind.

`in_playlist` replaces v1's `latest_flat_info` pointer. The question that pointer answered --
"is this video still in the playlist on YouTube?" -- belongs on the entry, not in a pointer to
a file the user is now free to delete. It is set by exactly one operation, `fold_flat()`, and
is never derived anywhere else.
"""
from __future__ import annotations

__all__ = ['RosterEntry', 'Roster', 'fold_flat']

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace

from pldl2.model.epoch import to_iso
from pldl2.model.infodicts import PL_ID, UnavailableMsg, V_ID
from pldl2.model.schema import SCHEMA_VERSION
from pldl2.model.timeline import PlaylistTimeline


@dataclass(frozen=True, slots=True, kw_only=True)
class RosterEntry:
    """One video's membership record. Order is positional, given by Roster.entries."""

    id: V_ID
    title: str | None = None
    in_playlist: bool = True
    """Present in the most recent flat extraction. False means gone from YouTube, not removed."""
    first_seen: int = 0
    last_seen: int = 0
    """The last flat extraction that still listed this video."""
    unavailable_msgs: tuple[UnavailableMsg, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class Roster:
    """Membership, order and the merge timeline for one playlist.

    Frozen: every mutation returns a new Roster. That is what makes an atomic commit possible
    -- the version on disk is either the old one or the new one, never a half-applied edit.
    """

    id: PL_ID
    updated: int = 0
    entries: tuple[RosterEntry, ...] = ()
    timeline: PlaylistTimeline = field(default_factory=dict)
    schema_version: int = SCHEMA_VERSION

    # ----------------------------------------------------------------- queries --

    @property
    def at(self) -> str:
        return to_iso(self.updated)

    def __len__(self) -> int:
        return len(self.entries)

    def __contains__(self, v_id: object) -> bool:
        return any(e.id == v_id for e in self.entries)

    def ids(self, *, in_playlist: bool | None = None) -> tuple[V_ID, ...]:
        """Video ids in playlist order.

        `in_playlist=True` is "still on YouTube right now", `False` is "gone but kept in the
        record", `None` (default) is everything. A filter, not a cross-file join -- which is
        why answering it no longer requires the newest flat capture to still exist.
        """
        return tuple(e.id for e in self.entries
                     if in_playlist is None or e.in_playlist is in_playlist)

    def get(self, v_id: V_ID) -> RosterEntry | None:
        for entry in self.entries:
            if entry.id == v_id:
                return entry
        return None

    def index_of(self, v_id: V_ID) -> int | None:
        """Positional index, or None. Never a falsy 0/None conflation.

        v1's `remove_videos` gated on `if merge_i := (... index ...)`, so index 0 is falsy and
        the first video in the playlist could never be removed (issue-1 #9, confirmed).
        Returning an explicit Optional is what makes that mistake hard to repeat.
        """
        for i, entry in enumerate(self.entries):
            if entry.id == v_id:
                return i
        return None

    # ---------------------------------------------------------------- mutation --

    def with_entries(self, entries: Iterable[RosterEntry], *, updated: int | None = None) -> Roster:
        """A copy carrying a new entry sequence."""
        return replace(self, entries=tuple(entries),
                       updated=self.updated if updated is None else updated)

    def with_timeline(self, timeline: PlaylistTimeline) -> Roster:
        return replace(self, timeline=dict(timeline))


def fold_flat(
    roster: Roster,
    present_ids: Sequence[V_ID],
    epoch: int,
    *,
    titles: Mapping[V_ID, str | None] | None = None,
    order: Sequence[V_ID] | None = None,
) -> Roster:
    """Fold one flat extraction into the roster. **The only writer of `in_playlist`.**

    - ids in `present_ids` get `in_playlist=True` and `last_seen=epoch`
    - ids absent from it get `in_playlist=False` and **keep their row and their last_seen**
    - ids not yet known are added, with `first_seen=last_seen=epoch`

    `order` is the reconciled playlist order, computed by merge/ordering from every snapshot
    seen so far. It is passed in rather than computed here because reconciling disagreeing
    orders is an L1 concern and L0 imports nothing. When omitted, existing order is preserved
    and genuinely new ids are appended in `present_ids` order -- correct for a first run and
    for an append-only playlist, and the caller is expected to supply `order` otherwise.

    Removing a video is *not* expressible here: an id vanishing from `present_ids` flips the
    flag and never drops the row. Dropping a row is edit/'s job, and only on an explicit
    request.
    """
    titles = titles or {}
    present = set(present_ids)
    by_id = {e.id: e for e in roster.entries}

    folded: dict[V_ID, RosterEntry] = {}
    for v_id, entry in by_id.items():
        if v_id in present:
            folded[v_id] = replace(
                entry,
                in_playlist=True,
                last_seen=max(entry.last_seen, epoch),
                first_seen=entry.first_seen or epoch,
                title=titles.get(v_id, entry.title) or entry.title,
            )
        else:
            folded[v_id] = replace(entry, in_playlist=False)

    for v_id in present_ids:
        if v_id not in folded:
            folded[v_id] = RosterEntry(
                id=v_id,
                title=titles.get(v_id),
                in_playlist=True,
                first_seen=epoch,
                last_seen=epoch,
            )

    if order is None:
        sequence = [e.id for e in roster.entries] + [i for i in present_ids if i not in by_id]
    else:
        # Anything the reconciled order omits is still ours to keep -- never drop a row.
        sequence = list(order) + [i for i in folded if i not in set(order)]

    seen: set[V_ID] = set()
    entries = [folded[i] for i in sequence if i in folded and not (i in seen or seen.add(i))]
    return roster.with_entries(entries, updated=max(roster.updated, epoch))
