"""Read and write _roster.json -- the one authoritative document.

Fixed path, rewritten in place via temp file + os.replace (atomic on Windows and POSIX).
Keep one .bak generation as crash insurance. Nothing is ever unlinked because a pointer
moved, which is what deletes delete_prev, the orphan-file class, the commit-ordering hazard
and the empty-pointers failure all at once.

Invariants are checked at open, not assumed: the roster must exist, parse and carry the
playlist id. Today a PL_INFO_PATH ident leaves _merge_flat as None, every method then raises,
and close() cheerfully writes a metadata file with no pointers (issue-1 #12, confirmed).
"""
