"""
L1. Fold many infodicts into one. Pure: no I/O, no printing, no network.

A merge answers three separate questions, and keeping them apart is what the layer is for:

| Question                                  | Mechanism                                    |
|-------------------------------------------|----------------------------------------------|
| In what order did things happen?          | `model.rank(epoch, level)` -- chronological  |
| Which value wins a field?                 | a **field resolver**, per field              |
| Which of those changes is worth recording?| a **timeline filter**, per field             |

They cannot be collapsed into one rule. Only a per-field rule can say "a view count only ever
goes up" or "never overwrite a title with nothing". And a single global "richer source wins"
ordering would empty the timeline: if an old full extraction outranks every later refresh,
almost no field registers as changed, and a record whose purpose is showing change over time
stops showing any. Folding chronologically produces the opposite problem -- a timeline
saturated with every `view_count` tick -- and that is exactly what the timeline filter is for.

    ordering.py   reconcile disagreeing snapshot orders into one playlist order
    updaters.py   the field resolvers and timeline filters, and the tables that pick one
    videos.py     fold per-video infodicts into one video's merged info + timeline
    playlists.py  fold playlist-level infodicts, and drive videos.py across the entries

Everything here takes values and returns values. `merge_pl_infos` returns a `MergeReport`
rather than writing anything; what to persist is the caller's decision.
"""
