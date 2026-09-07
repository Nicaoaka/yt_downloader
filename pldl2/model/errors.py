"""ErrorClass and a **pure** classifier over already-clean text.

yt_utils.interpret_error_msg currently does three jobs on the hot path of both the filter and
the display layer: it regex-strips ANSI escapes, warns on stdout when the pattern misses, and
colours its own warning. Stripping moves to ytdlp/ (once, at capture); classification lands
here as a pure function.

Two things to get right, both confirmed still live:
  - return a real enum, and have callers consume it -- issue-1 #18 discards the second return
    value, so a bot-check ("not confirmed unavailable") freezes an available video for the
    full 7-day fail backoff
  - AUTH_REQUIRED: yt-dlp reports a private playlist you cannot see as "playlist does not
    exist", so say "cookies may be missing, expired, or for the wrong account" instead of
    repeating its wording
"""
