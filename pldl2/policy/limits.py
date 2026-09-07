"""Limits: max_extracts, max_downloads, max_fails, quit_when_maxed.

**max_fails defaults to 5, and the quit branch gets the `!= 0` escape that downloads and
extracts already have.** Today it is 1 with quit_when_maxed=True and no escape, so the first
video failing on both YouTube and web.archive ends the whole pass: a 100-entry playlist with
10 dead videos needs 10 sessions to be walked once, and max_downloads=5 never engages
(issue-1 #5, confirmed -- the second video returns QUIT).

Also #15: is_maxed is now checked *before* the likely_unavailable bypass, so the
yt -> web.archive probe that records unavailable_msgs stops once the cap is hit, while the
comment above it still says "unavailable ignores maxes".
"""
