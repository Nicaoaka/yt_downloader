"""Pure-data configuration, split by **lifetime** rather than by topic. Shape-only validation:
no filesystem I/O in __post_init__, no import of the orchestrator (that is what makes the
config <-> playlist_dl cycle impossible to reintroduce).

    Layout   record-level  home + path templates. Persisted to _metadata.json; changing it
                           needs record.relocate(), never a raise.
    Library  record-level  optional global pool root + link strategy. Omit for per-playlist
                           Videos/ folders as real files.
    Persist  run-level     which raw captures to write, plus the per-InfoKind filters.

What is deliberately NOT here, and why:
  - the playlist ident      -> Playlist.open(ident, config), so one Config serves every script
  - cookies                 -> a Cookies handle passed to the call that needs it (ytdlp/cookies.py)
  - refresh_after / force   -> arguments of record.refresh()
  - opts                    -> the extractor; a read-only record must not need yt-dlp opts
  - ident_type              -> deleted; id/URL plus _playlists.json resolves it
  - _no_yt_dlp_downloads    -> deleted; FakeExtractor replaces it
"""
