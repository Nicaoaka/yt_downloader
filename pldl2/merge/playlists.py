"""merge_pl_infos -- fold playlist-level infodicts. Returns a MergeReport (merged info +
omissions + warnings); the caller decides what to persist.

Genuinely pure, unlike today: merge_infos.py:299-310 writes omitted_merge_timeline_infos.json
into the current working directory as a side effect.

Two authority rules:
  - **membership comes from the roster alone.** Today the previous merge's ids are unioned
    with _merge_flat, so a hand-removed video comes back at the next merge (issue-1 #36).
  - validate extra_v_infos ids instead of KeyError-ing on off-playlist ids
    (merge_infos.py:235) -- that invariant currently lives two modules away.
"""
