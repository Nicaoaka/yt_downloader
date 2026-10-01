"""
Fold playlist-level infodicts, and drive `videos.py` across the entries.

    merge_pl_infos(
        roster: Roster,
        captures: Sequence[Capture],
        *,
        resolve: MergeUpdaterMap = COMMON_UPDATER,
        record: TimelineFilter = ...,
        pl_resolve: MergeUpdaterMap = PL_UPDATER,
        previous: MergePlaylist | None = None,
    ) -> MergeReport

# ---- pure ----

Returns a `MergeReport` -- the merged document, the ids it omitted, and any warnings -- and
writes nothing. What to persist, and where, is the caller's decision. A merge that dumps a
file into the working directory as a side effect cannot be tested and cannot be composed.

# ---- membership comes from the roster, and only the roster ----

The roster decides which videos are in the playlist and in what order; the captures only
supply values. Taking the union of the previous merge's ids with the current ones instead is
what makes a video you deliberately removed reappear at the next merge.

Ids in `captures` that the roster does not know are **reported and skipped**, never indexed
blindly. A capture can legitimately hold an id the roster has since dropped -- that is what a
removal followed by a merge looks like -- so this is an ordinary case, not an error, and it
belongs in `MergeReport.omitted` rather than in an exception.

# ---- order ----

`ordering.merge_ordered_lists` reconciles the orders every snapshot proposes, newest first, so
the newest wins a disagreement. The result is the order the merged document presents, and it is
also what the caller applies with `Roster.with_order()`.

# ---- playlist-level fields ----

A flat extraction's `Capture.playlist` is the playlist's own payload (title, uploader,
description, `playlist_count`, ...); a per-video batch has none. `pl_resolve` folds those
payloads with the same updater machinery as a video's, into `MergePlaylist.playlist`.
Defaulting it to "the first pl_info wins" keeps current behavior while making the policy
visible and overridable, rather than a hardcoded index.

# ---- the roster's context ----

    update_roster(roster, captures, *, updater_map=ROSTER_UPDATER) -> Roster

Updating the roster is a merge, so it belongs here and not in `model/roster.py`. It runs the
same updaters over the same candidates as any other field, then hands the answer to
`roster.with_video_context()` / `with_playlist_context()`, which only store it.

The rule this must not reinvent: **latest wins, subject to the per-field resolver.** A recent
flat extraction should take the title over an older full download, because the uploader may
have renamed the video and the flat extraction is the fresher fact. Preferring the richer
source instead freezes a title that has since changed -- and it is the same mistake as ordering
the merge's inputs by level.

Cases where a fresh source is *worse* are per-field problems with per-field answers -- a
placeholder title on a removed video, a `None` where the extractor simply did not look, a flat
extraction's four thumbnails against a full extraction's forty-five. That is `latest_not_none`,
`richest` and their neighbors in updaters.py, not a different ordering.

`model.roster.VIDEO_CONTEXT_SOURCES` and `PLAYLIST_CONTEXT_SOURCES` say which payload keys can
supply each context field. They are data about what context *is*, so they stay in L0; reading
a value out through them is the fold's job, here.

# ---- shape ----

The result is a `MergePlaylist`: a `Capture` after folding, plus the `PL_InfoLevel` reached
and the per-video timeline. `merge_timeline` and `info_level` therefore never enter the
payload. A projection flattens it to the inline v1 shape for anything that wants a plain
infodict -- that is a dict merge at the boundary, not a second code path with its own rules.
"""
from __future__ import annotations

__all__ = ['MergeReport', 'merge_pl_infos', 'update_roster']

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from itertools import chain
from typing import Any

from pldl.merge.ordering import merge_ordered_lists
from pldl.merge.updaters import (
    COMMON_TIMELINE_KEYS,
    COMMON_UPDATER,
    PL_UPDATER,
    ROSTER_UPDATER,
    Candidate,
    MergeUpdaterMap,
    TimelineUpdateFilter,
    apply_updater,
    unwrap_candidates,
)
from pldl.merge.videos import merge_v_infos
from pldl.model import (
    NO_VALUE,
    PLAYLIST_CONTEXT_SOURCES,
    V_ID,
    VIDEO_CONTEXT_SOURCES,
    Capture,
    Epoch,
    MergePlaylist,
    PL_InfoLevel,
    PlaylistTimeline,
    Rank,
    Roster,
    V_InfoLevel,
    VideoEntry,
)

type _Payloads = Iterable[tuple[Mapping[str, Any], Rank]]


@dataclass(slots=True, kw_only=True)
class MergeReport:
    """A merge's product, plus what it could not place. Nothing is written here."""

    merged: MergePlaylist
    omitted: Mapping[V_ID, int] = field(default_factory=dict)
    """Ids present in the captures that the roster does not know, and how many entries each
    contributed. An ordinary case -- a removal followed by a merge looks exactly like this --
    so it is reported rather than raised."""
    warnings: tuple[str, ...] = ()


# ---- folding payloads ----

def _fold(payloads: _Payloads, updater_map: MergeUpdaterMap,
          keys: Sequence[str] | None = None) -> dict[str, Any]:
    """Fold payloads into one, by the table. `keys` restricts it to a whitelist.

    Same machinery as the per-video fold, minus the timeline: a `Candidate` per key carrying
    the rank of the source that supplied it, so the result does not depend on fold order.
    """
    merged: dict[str, Candidate] = {}
    for payload, rank in payloads:
        for key in keys if keys is not None else sorted(merged.keys() | payload.keys()):
            apply_updater(merged, key, Candidate(payload.get(key, NO_VALUE), rank),
                          updater_map[key])
    return unwrap_candidates(merged)


def _context(values: Mapping[str, Any], sources: Mapping[str, tuple[str, ...]]) -> dict[str, Any]:
    """Read the context fields out of a merged payload, first source key that has a value."""
    found: dict[str, Any] = {}
    for target, keys in sources.items():
        for key in keys:
            value = values.get(key)
            if value is not None:
                found[target] = value
                break
    return found


def _source_keys(sources: Mapping[str, tuple[str, ...]]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(chain.from_iterable(sources.values())))


# ---- the roster ----

def update_roster(roster: Roster, captures: Sequence[Capture], *,
                  updater_map: MergeUpdaterMap = ROSTER_UPDATER) -> Roster:
    """Fold a session's captures into the roster: membership, then order, then context.

    **Only a flat extraction may decide membership.** A per-video batch holds whatever this
    session happened to extract, so treating it as a listing would flip every video it does
    not mention to `in_playlist=False`. `Capture.playlist` is the discriminator: `wrap_flat`
    fills it, a per-video batch leaves it `None`.

    Context comes from every capture, flat or not -- a full extraction knows a title a flat
    one cannot see for a dead video -- and follows the merge's policy, which is why it is
    resolved here and only stored by the roster.

    **Context is resolved across the captures given, then replaces what was stored.** Within
    one call the result does not depend on the order, but a later call wins over an earlier
    one even if its captures are older, because the roster stores a context value without the
    rank of the source that supplied it. Pass a session's captures together. Nothing may
    depend on context for correctness -- that is why it is allowed to be best-effort here
    rather than carrying per-field provenance on disk.
    """
    flats = sorted((c for c in captures if c.playlist is not None), key=lambda c: c.epoch)

    for capture in flats:
        roster = roster.with_flat_extraction(capture.ids(), capture.epoch)

    if flats:
        # Newest snapshot first: it wins a disagreement. The roster's current order is the
        # accumulated result of every earlier snapshot, so it goes last and breaks ties.
        roster = roster.with_order(merge_ordered_lists(
            [*(c.ids() for c in reversed(flats)), roster.ids()]))

    known = set(roster.ids())
    v_payloads: dict[V_ID, list[tuple[Mapping[str, Any], Rank]]] = {}
    pl_payloads: list[tuple[Mapping[str, Any], Rank]] = []
    for capture in captures:
        if capture.playlist is not None:
            pl_payloads.append((capture.playlist, Rank(capture.epoch, V_InfoLevel.FLAT)))
        for entry in capture.videos:
            if entry.id in known:
                v_payloads.setdefault(entry.id, []).append((entry.data, entry.rank))

    v_keys = _source_keys(VIDEO_CONTEXT_SOURCES)
    for v_id, payloads in v_payloads.items():
        context = _context(_fold(payloads, updater_map, v_keys), VIDEO_CONTEXT_SOURCES)
        if context:
            roster = roster.with_video_context(v_id, context)  # type: ignore[arg-type]

    if pl_payloads:
        context = _context(_fold(pl_payloads, updater_map, _source_keys(PLAYLIST_CONTEXT_SOURCES)),
                           PLAYLIST_CONTEXT_SOURCES)
        if context:
            roster = roster.with_playlist_context(context)  # type: ignore[arg-type]

    return roster


# ---- the merge ----

def merge_pl_infos(
    roster: Roster,
    captures: Sequence[Capture],
    *,
    timeline_filter: TimelineUpdateFilter = COMMON_TIMELINE_KEYS.__contains__,
    v_updater_map: MergeUpdaterMap = COMMON_UPDATER,
    pl_updater_map: MergeUpdaterMap = PL_UPDATER,
    previous: MergePlaylist | None = None,
) -> MergeReport:
    """Fold every capture into one merged playlist, in the roster's order.

    Membership and order come from the roster alone; the captures only supply values. Ids the
    roster does not know are reported in `MergeReport.omitted`, never indexed blindly.

    `previous` continues an earlier merge, so pruned captures do not cost their values.
    Timelines are seeded from `roster.timeline`, not from `previous`: the roster is the
    durable document and the merges are regenerable, so history must not live only in a file
    the user is invited to delete. The returned timeline is what the caller stores back with
    `roster.with_timeline()`.
    """
    order = roster.ids()
    by_id: dict[V_ID, list[VideoEntry]] = {v_id: [] for v_id in order}
    omitted: Counter[V_ID] = Counter()
    for capture in captures:
        for entry in capture.videos:
            if entry.id in by_id:
                by_id[entry.id].append(entry)
            else:
                omitted[entry.id] += 1

    videos: list[VideoEntry] = []
    timeline: dict[V_ID, Any] = {}
    for v_id in order:
        sources, seed = by_id[v_id], previous.get(v_id) if previous else None
        if not sources and seed is None:
            # The roster knows this video but nothing has ever described it. Keep the row so
            # `videos` stays aligned with the roster's order and membership.
            videos.append(VideoEntry(id=v_id, info_level=V_InfoLevel.NONE, data={'id': v_id}))
            continue
        entry, v_timeline = merge_v_infos(
            sources,
            merge_updater_map=v_updater_map,
            tl_update_filter=timeline_filter,
            init_v_entry=seed,
            init_v_timeline=roster.timeline.get(v_id),
        )
        videos.append(entry)
        if len(v_timeline):
            timeline[v_id] = v_timeline

    # The previous merge is one more payload at its own rank, not a second pass.
    pl_payloads = [(c.playlist, Rank(c.epoch, V_InfoLevel.FLAT))
                   for c in captures if c.playlist is not None]
    if previous is not None:
        pl_payloads.append((previous.playlist, Rank(previous.epoch, V_InfoLevel.FLAT)))

    epochs = [c.epoch for c in captures] + ([previous.epoch] if previous else [])

    merged = MergePlaylist(
        id=roster.id,
        epoch=Epoch(max(epochs, default=roster.last_updated)),
        info_level=_pl_level(videos, timeline),
        playlist=_fold(pl_payloads, pl_updater_map),
        videos=tuple(videos),
        timeline=timeline,
    )
    return MergeReport(merged=merged, omitted=dict(omitted))


def _pl_level(videos: Sequence[VideoEntry], timeline: PlaylistTimeline) -> PL_InfoLevel:
    """Mirrors `derive_pl_info_level`, but reads the declared levels rather than sniffing
    content -- a merged entry carries its level on the envelope."""
    has_extracts = any(v.info_level >= V_InfoLevel.EXTRACT for v in videos)
    match has_extracts, bool(timeline):
        case False, False: return PL_InfoLevel.FLAT
        case False, True:  return PL_InfoLevel.MERGE_FLAT
        case True, False:  return PL_InfoLevel.NORMAL
        case _:            return PL_InfoLevel.MERGE
