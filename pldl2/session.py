"""L4. DownloadSession -- drives yt-dlp, applies a DownloadPolicy, hands results to the record.

The only L4 object that touches the network. Emits events to a Reporter rather than
printing, so tests run silent and the 42 print / 18 WARNING calls in playlist_dl.py have a
home. Thin: it sequences ytdlp/, policy/ and store/ and owns no algorithms.
"""
