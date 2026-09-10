"""
Fold every infodict known for one video into one merged info, plus its timeline.

    merge_v_infos(
        v_infos: Sequence[VideoEntry],
        *,
        resolve: FieldResolver,
        record: TimelineFilter,
        into: VideoEntry | None = None,        # a previous merge to continue from
        timeline: VideoTimeline = VideoTimeline(),
    ) -> tuple[VideoEntry, VideoTimeline]

# ---- the fold ----

Process inputs **oldest first** (`model.rank(epoch, level)`), because the timeline is a record
of what was learned when, and folding in any other order makes the recorded progression read
backwards.

Per input, per key:

1.  `is_latest = epoch >= highest_epoch_seen_for[key]` -- **per key**, not per infodict. A
    flat extraction can carry a newer `view_count` than the last full extraction while
    carrying nothing at all for `description`.
2.  `resolve(merged, key, value, is_latest)` decides what happens and reports whether it
    changed anything. A key the input lacks is `NO_VALUE`, which is distinct from `None`:
    absent means "this extractor did not say", `None` means "it said nothing is there".
3.  If it changed and `record(key)`, add a `FieldUpdate` to this instant's timeline entry.

Iterate keys **sorted**. The set union of two dicts' keys iterates in hash order, which varies
between processes, and that is enough to make two runs over identical inputs write different
bytes. "Same inputs, byte-identical output" is a test.

# ---- what the fold owns rather than the resolver ----

`info_level` and `unavailable_msgs` are not resolved field-by-field; the fold handles both, and
the resolver tables map them to `no_update` so a stray rule cannot reach them.

- **Level** only ever rises. When it does, the entry for that instant records
  `prev_info_level` and `info_level`; when it does not, it records neither, and
  `is_better_info` stays False.
- **Unavailability** accumulates. Reports from different extractors at the same instant are all
  kept -- YouTube saying "private" and a mirror saying "not archived" are two facts, not a
  conflict -- deduplicated on their content.

# ---- the timeline ----

One entry per instant that contributed something. An entry that ends up empty is dropped: a
refresh that taught nothing new should leave no trace, since the timeline records change and
not that a session ran.

**Entries already on the timeline are read-only.** Stamp only the entry for the instant being
folded now. Reaching back to restamp older entries with the current level rewrites history in
every file it touches, and it is the single most damaging thing this fold can get wrong.
"""
