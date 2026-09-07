"""_library.json: v_id -> {path, epoch, ext, filesize, seen_in: [pl_id, ...]}.

`seen_in` is what makes deletion safe -- removing a playlist must not delete a file another
playlist still references, so the index is the refcount (collections.Counter).

The policy layer consults this first: library.has(v_id) resolves a decision to CACHED without
invoking yt-dlp at all, and lets a record report a video as downloaded even though no file
sits under its own folder.
"""
