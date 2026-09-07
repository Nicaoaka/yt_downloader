"""Metadata -- identity, resolved paths, and the download history log. Schema v2.

Carries schema_version, the playlist id, the last-known title, `paths` (with playlist_dir
**authoritative**, written once at creation and never recomputed from a title), and `history`
as an ordered list of {epoch, at, videos} rather than a dict keyed by a local-time string.

`pointers` is gone. One pointer to a fixed path is a filename, and the rest pointed at files
the user is now free to delete.
"""
