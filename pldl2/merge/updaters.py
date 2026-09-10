"""
Per-field rules: which value wins, and whether the change is worth recording.

Two callables, deliberately named apart, because conflating them is easy and the consequences
are opposite -- one silently loses data, the other silently loses history:

    FieldResolver(merged, key, value, is_latest) -> changed: bool
        Decides what `merged[key]` becomes. Returns True when it actually changed something,
        which is the only input the timeline filter gets to see.

    TimelineFilter(key) -> record: bool
        Decides whether a change to `key` is written to the timeline. `view_count` moves every
        session and recording it would drown everything else; `title` moving is the whole
        point of keeping a record.

`is_latest` is per key, not per infodict: a flat extraction can carry a newer `view_count` than
the last full extraction while carrying nothing at all for `description`. The fold tracks the
highest epoch seen *per key* and passes the verdict in.

# ---- the resolvers ----

    no_update       never writes. For fields the fold owns itself.
    latest_exact    the newest value wins, even if that means removing the key.
    latest_not_none the newest non-None value wins. The sensible default: an extractor that
                    omits a field is saying "I don't know", not "it is empty".
    fill_absent     only writes a key that is missing. For values that should never move once
                    known.
    maximizer       only writes a larger value. For counters that should not appear to shrink.

`builder(k_to_func, default_func)` composes them into one resolver, and raises if a key is
listed twice -- so two rules can never silently disagree about the same field.

# ---- the tables ----

    COMMON_UPDATER  for a full merge. `latest_not_none` by default.
    ROSTER_UPDATER  for folding into the roster. A **whitelist** with `no_update` as the
                    default, so the roster only ever accumulates the small set of fields it is
                    supposed to hold and cannot drift into being a second copy of the merge.
    PL_UPDATER      for playlist-level fields, which currently have no policy at all -- the
                    first pl_info simply wins. Default to that behavior so nothing changes,
                    but make it visible and overridable.

# ---- open, and worth resolving with a test ----

Folding a video's own info into the roster gives that entry an epoch equal to its source, so
the two collide. v1 subtracted a second from the roster's copy to keep them distinguishable,
which works but splits one extraction across two timeline instants a second apart. Now that
several timeline entries may share an epoch and are ordered by `(epoch, level)`, ranking the
roster's copy below its source by *level* is available instead, and costs no fake time. Write
the test first and pick whichever reads correctly.
"""
