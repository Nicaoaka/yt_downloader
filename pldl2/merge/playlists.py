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
also what the caller can hand back to `roster.apply_flat_extraction(order=...)`.

# ---- playlist-level fields ----

A flat extraction's `Capture.playlist` is the playlist's own payload (title, uploader,
description, `playlist_count`, ...); a per-video batch has none. `pl_resolve` folds those
payloads with the same updater machinery as a video's, into `MergePlaylist.playlist`.
Defaulting it to "the first pl_info wins" keeps current behavior while making the policy
visible and overridable, rather than a hardcoded index.

# ---- the roster's context ----

    fold_flat_extraction(roster, capture, *, resolve, epoch) -> Roster

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
