"""DecisionContext -- built **once per session**, not per video.

    history_index: HistoryIndex   replaces the O(videos x history) linear rescan per video
    archive_ids:   frozenset[str]
    counts:        RunningCounts  replaces the hidden nonlocal flag

Three confirmed defects share one root cause -- decision state living in a closure built at
import time -- and all three vanish once state moves here. The worst is #3: because
default_wrapper_match_filter is constructed at import and is the default argument of
download_v_infos, a second run in the same process skips the history scan entirely and
downloads straight into an active 3-day 403 backoff. The harness reproduces exactly that.
"""
