"""Find user-owned captures by globbing. **Replaces pointers entirely.**

flat/, v_infos/ and merges/ are the user's: they may be pruned, moved or corrupted between
runs, and pldl only ever adds to them. Their filenames start with a sortable readable
timestamp, so "the latest" is a directory listing and a sort -- which is also the only thing
that still works once half of them are deleted.

Every read here tolerates an absent directory and downgrades a missing, corrupt or
hand-mangled file to a reported Issue instead of raising. No code path may assume a specific
file is present, including the newest one.
"""
