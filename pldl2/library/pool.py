"""The media pool: one copy per video id, under <library_root>/_videos/.

The pool filename is **effectively fixed at %(id)s.%(ext)s and is not configurable**, because
it is not a name, it is an address: stable across playlists (the same bytes serve both),
stable across title changes (a retitled video must not orphan its own file), and
id-recoverable (the index, the archive and adopt() all need the id back out of it).

Everything you actually want from a filename lives on the link instead, where it is free --
see links.py. The global download archive lives here too: handing yt-dlp
<library_root>/_downloaded.txt is what actually prevents the re-download across playlists.
"""
