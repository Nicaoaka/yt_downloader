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
stale, and nothing may depend on it for correctness.

**This module holds context; it does not decide it.** Choosing which of two values for a field
wins is the merge's job and follows the merge's policy, so it lives in merge/ with the field
resolvers. Deciding it here would be a second implementation of the same thing, and a second
one always drifts -- this one had already drifted into preferring a rich old source over a fresh
one, which freezes a title the uploader has since changed. `with_video_context()` and
`with_playlist_context()` take an already-resolved value and store it.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'VideoContext', 'PlaylistContext',
    'RosterEntry', 'Roster',
    'apply_flat_extraction',
    'VIDEO_CONTEXT_SOURCES', 'PLAYLIST_CONTEXT_SOURCES',
]

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from typing import NotRequired, TypedDict

from pldl2.model.epoch import EPOCH_ZERO, Epoch
from pldl2.model.errors import UnavailableInfo
from pldl2.model.infodicts import PL_ID, V_ID
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
    unavailable_infos: tuple[UnavailableInfo, ...] = ()

    context: VideoContext = field(default_factory=VideoContext)

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

    def with_video_context(self, v_id: V_ID, context: VideoContext) -> Roster:
        """Store already-resolved context for one video. Replaces rather than merges.

        Merging two candidate values is policy and belongs to merge/; this only records the
        answer. Returns the roster unchanged when the id is unknown.
        """
        entry = self.get(v_id)
        if entry is None:
            return self
        return self.with_entry(replace(entry, context=dict(context)))  # type: ignore[arg-type]

    def with_playlist_context(self, context: PlaylistContext) -> Roster:
        """Store already-resolved context for the playlist. Replaces rather than merges."""
        return replace(self, context=dict(context))  # type: ignore[arg-type]


# ---- context ----

VIDEO_CONTEXT_SOURCES: Mapping[str, tuple[str, ...]] = {
    'title': ('title',),
    'uploader': ('uploader', 'channel', 'creator'),
    'duration': ('duration',),
    'webpage_url': ('webpage_url', 'url'),
}
"""Which infodict keys can supply each context field, first match winning.

Several yt-dlp keys carry the same fact -- `uploader`, `channel` and `creator` all name the
author -- and which one appears depends on the extractor and the level. A flat entry has no
`webpage_url` at all; its `url` is the watch page.
"""

PLAYLIST_CONTEXT_SOURCES: Mapping[str, tuple[str, ...]] = {
    'title': ('title',),
    'uploader': ('uploader', 'channel', 'creator'),
    'description': ('description',),
    'webpage_url': ('webpage_url',),
}

def apply_flat_extraction(
    roster: Roster,
    present_ids: Sequence[V_ID],
    epoch: int,
    *,
    order: Sequence[V_ID] | None = None,
) -> Roster:
    """Fold one flat extraction into the roster. **The only writer of `in_playlist`.**

    - ids in `present_ids` get `in_playlist=True` and `last_seen=epoch`
    - ids absent from it get `in_playlist=False` and **keep their row and their last_seen**
    - ids not yet known are added, with `first_seen=last_seen=epoch`

    Context is deliberately not touched here. Which value wins a field follows the merge's
    policy, so merge/ resolves it and hands the answer to `with_video_context()`.

    `order` is the reconciled playlist order, computed by merge/ordering across every snapshot
    seen so far. It is passed in rather than computed here because reconciling disagreeing
    orders is an L1 concern. When omitted, existing order is preserved and genuinely new ids
    are appended in `present_ids` order -- correct for a first run and for an append-only
    playlist, and the caller is expected to supply `order` otherwise.

    Removing a video is *not* expressible here: an id vanishing from `present_ids` flips the
    flag and never drops the row. Dropping a row is edit/'s job, on an explicit request only.
    """
    epoch = Epoch(epoch)
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
    return updated
