"""L4. PlaylistRecord -- open, query, mutate and commit the durable record.

**Never touches the network and never imports yt_dlp.** That is the whole point of the
split: inspecting your own history becomes a read. Today the same work requires building a
PlaylistDL, which extracts, can block on input() and writes files from __init__.

Thin by construction: it sequences calls into store/, merge/ and edit/ and owns no
algorithms of its own. Setup belongs in __enter__, not __init__.
"""
