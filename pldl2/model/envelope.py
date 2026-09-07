"""VideoEntry / Capture -- pldl's own fields wrapped *around* a payload, never injected into it.

Today info_level, unavailable_msgs and playlist_epoch are written straight into the dict
yt-dlp returned (yt_utils.py:127-130). That is why the merge has to `continue` on specific
keys, why COMMON_UPDATER carries unreachable no_update entries, and why any field a future
yt-dlp adds could collide with ours. Here the envelope carries pldl's fields and `data`
stays exactly what yt-dlp returned.

Frozen dataclasses (frozen=True, slots=True, kw_only=True) -- these are ours, so we get
defaults, __post_init__ invariants, dataclasses.replace(), real ==, and a typo in a field
name becomes an error instead of a new dict key.
"""
