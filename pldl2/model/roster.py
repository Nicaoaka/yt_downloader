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
    is honored and permanent. The removal is recorded in `manipulations` and the raw captures
    stay on disk, so the record is rebuildable.

`in_playlist` is written by exactly one operation, `apply_flat_extraction()`, and derived
nowhere else.

Beyond membership, the roster and its entries carry **context**: last-known title, uploader and
the like, so a playlist can be listed with nothing else on disk. Context is best-effort, may be
stale, and nothing may depend on it for correctness. It is written by `update_context()` under
a rank guard, so a richer source is never overwritten by a poorer one -- which is what lets a
mirror's full extraction fill in a title that a flat extraction of a dead video cannot see.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'VideoContext', 'PlaylistContext',
    'RosterEntry', 'Roster',
    'apply_flat_extraction', 'update_context', 'context_from_info',
    'VIDEO_CONTEXT_SOURCES', 'PLAYLIST_CONTEXT_SOURCES',
]

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from typing import Any, NotRequired, TypedDict

from pldl2.model.epoch import EPOCH_ZERO, Epoch
from pldl2.model.errors import UnavailableInfo
from pldl2.model.infodicts import PL_ID, V_ID
from pldl2.model.levels import V_InfoLevel, rank
from pldl2.model.manipulations import ManipulationLog
from pldl2.model.schema import SCHEMA_VERSION
from pldl2.model.timeline import PlaylistTimeline


class VideoContext(TypedDict, total=False):
    """Last-known descriptive fields for one video.

    A loose TypedDict so extending it costs one line and no migration: a reader that does not
    know a key ignores it, and an absent key simply means unknown. Never authoritative.
    """

    title: NotRequired[str]
    uploader: NotRequired[str]
    duration: NotRequired[int]
    webpage_url: NotRequired[str]


class PlaylistContext(TypedDict, total=False):
    """Last-known descriptive fields for the playlist itself."""

    title: NotRequired[str]
    uploader: NotRequired[str]
    description: NotRequired[str]
    webpage_url: NotRequired[str]


@dataclass(frozen=True, slots=True, kw_only=True)
class RosterEntry:
    """One video's membership record. Order is positional, given by `Roster.entries`."""

    id: V_ID
    in_playlist: bool = True
    """Present in the most recent flat extraction. False means gone from YouTube, not removed."""
    first_seen: Epoch = EPOCH_ZERO
    last_seen: Epoch = EPOCH_ZERO
    """The last flat extraction that still listed this video."""
    unavailable_msgs: tuple[UnavailableInfo, ...] = ()

    context: VideoContext = field(default_factory=VideoContext)
    context_rank: int = 0
    """The rank of the source that last wrote `context`. See `update_context`."""

    def __post_init__(self) -> None:
        for name in ('first_seen', 'last_seen'):
            value = getattr(self, name)
            if not isinstance(value, Epoch):
                object.__setattr__(self, name, Epoch(value))


@dataclass(frozen=True, slots=True, kw_only=True)
class Roster:
    """Membership, order, context, timeline and edit log for one playlist.

    Frozen: every mutation returns a new Roster, which is what lets a commit be atomic -- the
    version on disk is either the old one or the new one, never half applied.
    """

    id: PL_ID
    entries: tuple[RosterEntry, ...] = ()
    first_seen: Epoch = EPOCH_ZERO
    """When this playlist was first recorded."""
    last_updated: Epoch = EPOCH_ZERO
    """The most recent flat extraction. **Only** a flat extraction moves this, so it always
    answers "how current is membership"; a context update from another source leaves it be."""

    context: PlaylistContext = field(default_factory=PlaylistContext)
    context_rank: int = 0
    timeline: PlaylistTimeline = field(default_factory=dict)
    manipulations: ManipulationLog = field(default_factory=ManipulationLog)
    schema_version: int = SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name in ('first_seen', 'last_updated'):
            value = getattr(self, name)
            if not isinstance(value, Epoch):
                object.__setattr__(self, name, Epoch(value))

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

        Note: User-facing 1-based, negative-supporting 'positions' belong in edit/.
        """
        for i, entry in enumerate(self.entries):
            if entry.id == v_id:
                return i
        return None

    # ---- mutation ----

    def with_entries(self, entries: Iterable[RosterEntry], *,
                     last_updated: int | None = None) -> Roster:
        """A copy carrying a new entry sequence."""
        return replace(self, entries=tuple(entries),
                       last_updated=(self.last_updated if last_updated is None
                                     else Epoch(last_updated)))

    def with_entry(self, entry: RosterEntry) -> Roster:
        """A copy with one entry replaced in place, preserving order."""
        return self.with_entries(e if e.id != entry.id else entry for e in self.entries)

    def with_timeline(self, timeline: PlaylistTimeline) -> Roster:
        return replace(self, timeline=dict(timeline))


# ---- context ----

VIDEO_CONTEXT_SOURCES: Mapping[str, tuple[str, ...]] = {
    'title': ('title',),
    'uploader': ('uploader', 'channel', 'creator'),
    'duration': ('duration',),
    'webpage_url': ('webpage_url',),
}
"""Which infodict keys can supply each context field, first match winning.

Several yt-dlp keys carry the same fact -- `uploader`, `channel` and `creator` all name the
author -- and which one appears depends on the extractor and the level.
"""

PLAYLIST_CONTEXT_SOURCES: Mapping[str, tuple[str, ...]] = {
    'title': ('title',),
    'uploader': ('uploader', 'channel', 'creator'),
    'description': ('description',),
    'webpage_url': ('webpage_url',),
}


def context_from_info(info: Mapping[str, Any] | None, *,
                      sources: Mapping[str, tuple[str, ...]] | None = None) -> dict[str, Any]:
    """Pull context fields out of an infodict, skipping anything absent or None."""
    if not info:
        return {}
    found: dict[str, Any] = {}
    for target, keys in (sources or VIDEO_CONTEXT_SOURCES).items():
        for key in keys:
            value = info.get(key)
            if value is not None:
                found[target] = value
                break
    return found


def _merge_context(current: Mapping[str, Any], current_rank: int,
                   incoming: Mapping[str, Any], source_rank: int) -> tuple[dict, int]:
    """Best-value merge: a source at least as good wins, a poorer one only fills gaps."""
    if source_rank >= current_rank:
        return {**current, **incoming}, source_rank
    return {**incoming, **current}, current_rank


def update_context(
    roster: Roster,
    v_id: V_ID,
    info: Mapping[str, Any],
    *,
    level: V_InfoLevel,
    epoch: int,
) -> Roster:
    """Merge context for one video, letting the better source win.

    Context is **best-value, not latest**: the source's `rank(level, epoch)` is compared with
    the rank that last wrote this entry's context.

      - a source that ranks at least as high overwrites the fields it supplies
      - a poorer source only fills fields that are still unknown

    That second rule is what matters for a dead video. A flat extraction of a removed video
    carries almost nothing, but a full extraction from a mirror carries its title and author --
    and because that extraction outranks the flat one, the good values stick instead of being
    flattened away on the next refresh.

    Does not touch `last_updated`, which tracks membership rather than description.
    """
    entry = roster.get(v_id)
    if entry is None:
        return roster

    incoming = context_from_info(info)
    if not incoming:
        return roster

    merged, new_rank = _merge_context(
        entry.context, entry.context_rank, incoming, rank(level, epoch))
    return roster.with_entry(replace(entry, context=merged, context_rank=new_rank))


def apply_flat_extraction(
    roster: Roster,
    present_ids: Sequence[V_ID],
    epoch: int,
    *,
    infos: Mapping[V_ID, Mapping[str, Any]] | None = None,
    playlist_info: Mapping[str, Any] | None = None,
    order: Sequence[V_ID] | None = None,
) -> Roster:
    """Fold one flat extraction into the roster. **The only writer of `in_playlist`.**

    - ids in `present_ids` get `in_playlist=True` and `last_seen=epoch`
    - ids absent from it get `in_playlist=False` and **keep their row and their last_seen**
    - ids not yet known are added, with `first_seen=last_seen=epoch`

    `infos` maps an id to its flat entry and `playlist_info` is the playlist's own infodict.
    Both feed the context merge at FLAT rank, so a value already known from a richer source is
    not flattened away.

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
            )
        else:
            folded[v_id] = replace(entry, in_playlist=False)

    for v_id in present_ids:
        if v_id not in folded:
            folded[v_id] = RosterEntry(
                id=v_id, in_playlist=True, first_seen=epoch, last_seen=epoch)

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

    updated = roster.with_entries(entries, last_updated=max(roster.last_updated, epoch))
    if not updated.first_seen:
        updated = replace(updated, first_seen=epoch)

    for v_id in present_ids:
        if info := infos.get(v_id):
            updated = update_context(updated, v_id, info, level=V_InfoLevel.FLAT, epoch=epoch)

    if incoming := context_from_info(playlist_info, sources=PLAYLIST_CONTEXT_SOURCES):
        merged, new_rank = _merge_context(
            updated.context, updated.context_rank, incoming, rank(V_InfoLevel.FLAT, epoch))
        updated = replace(updated, context=merged, context_rank=new_rank)

    return updated
