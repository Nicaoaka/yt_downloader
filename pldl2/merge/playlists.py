"""
Fold playlist-level infodicts, and drive `videos.py` across the entries.

    merge_pl_infos(
        roster: Roster,
        captures: Sequence[Capture],
        *,
        resolve: FieldResolver = COMMON_UPDATER,
        record: TimelineFilter = ...,
        pl_resolve: FieldResolver = PL_UPDATER,
        previous: MergeDocument | None = None,
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

`pl_resolve` handles the playlist's own fields (title, uploader, description) with the same
resolver machinery as a video's. Defaulting it to "the first pl_info wins" keeps current
behavior while making the policy visible and overridable, rather than a hardcoded index.

# ---- the roster's context ----

    fold_flat_extraction(roster, capture, *, resolve, epoch) -> Roster

Updating the roster is a merge, so it belongs here and not in `model/roster.py`. It runs the
same resolver over the same candidate values as any other field, then hands the answer to
`roster.with_video_context()` / `with_playlist_context()`, which only store it.

The rule this must not reinvent: **latest wins, subject to the per-field resolver.** A recent
flat extraction should take the title over an older full download, because the uploader may
have renamed the video and the flat extraction is the fresher fact. Preferring the richer
source instead freezes a title that has since changed -- and it is the same mistake as ordering
the merge's inputs by level.

Cases where a fresh source is *worse* are per-field problems with per-field answers -- a
placeholder title on a removed video, a `None` where the extractor simply did not look. That is
`latest_not_none` and its neighbours in updaters.py, not a different ordering.

`model.roster.VIDEO_CONTEXT_SOURCES` says which infodict keys can supply each context field;
`context_from_info` reads them out. Both are data about what context *is*, so they stay in L0.

# ---- shape ----

The merged document carries an envelope, like a capture does, so `merge_timeline` and
`info_level` cannot collide with yt-dlp's namespace. A projection flattens it to the inline
v1 shape for anything that wants a plain infodict -- that is a dict merge at the boundary, not
a second code path with its own rules.
"""
