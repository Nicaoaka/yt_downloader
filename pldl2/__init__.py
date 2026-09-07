"""L5 facade. Re-exports the public surface so `from pldl2 import *` works, exactly as
`pldl/__init__.py` does today (the run configs in scripts/ rely on that).

Layering, dependencies point downward only:

    L5  __init__.py       facade + re-exports
    L4  record.py         PlaylistRecord -- opens/queries/commits the durable record
        session.py        DownloadSession -- drives yt-dlp, applies policy, feeds the store
    L3  report/           pure renderers: data -> str. Never print.
    L2  store/            the on-disk record          library/  the global video pool
        ytdlp/            the yt-dlp adapter          policy/   download decisions (pure)
    L1  merge/            fold N infodicts -> 1       edit/     playlist edits (pure)
    L0  model/            types, levels, epochs, ranking, timeline. No deps.

The reference for "done right" is pldl/utils/merge_ordered_lists.py: no pldl imports, no
I/O, no printing, fully tested. Every module here is held to that standard.
"""
