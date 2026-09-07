"""MergeTimelineEntry, with **structured** better_info (from/to fields, not "FLAT -> EXTRACT").

Kills the round-trip where the timeline formats a string and display.py:234 regexes it back
into an enum -- the old code self-documents this as "this is very fragile, but it'll work".
The rendered string is still written to disk for readability, but it is derived from the
structured fields and never parsed back.

Entries are **immutable once written**: stamp only the entry for the epoch being folded now,
and treat older entries as read-only (issue-1 #6, confirmed still live).
"""
