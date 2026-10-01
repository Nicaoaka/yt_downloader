"""The yt-dlp download archive: **one reader/writer pair** with a round-trip invariant.

Today the desync auto-repair writes `pldl_sync_fix <id>` while the reader accepts only
youtube / youtubewebarchive / __pldl_yt_dlp_generic__, so every startup re-prompts and
re-appends the same line forever (issue-1 #4 -- the harness confirms three startups produce
three unreadable lines). A generic download writes its real extractor key (`bilibili <id>`)
and desyncs permanently.

Property test: every key the writer emits is parsed by the reader. The reader must stay
narrow -- a key yt-dlp does not recognise will not suppress its re-download.
"""
