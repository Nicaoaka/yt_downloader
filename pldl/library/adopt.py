"""adopt(playlist_dir) -- pull an existing per-playlist Videos/ folder into the pool.

Recovers each id from the filename, falling back to matching against the roster and then to a
content hash (hashlib / filecmp) for files it cannot parse; moves the file in, writes the
index, and creates the link back. Same dry-run / backup discipline as the migrator.

A file whose id cannot be established is reported and **left exactly where it is**, never
guessed at.
"""
