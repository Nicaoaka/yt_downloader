"""Action / error tag rendering -- **one** implementation.

Today there are two duplicated loops (display.py:221-231 vs :279-291) that have already
drifted: one matches 'yt'/'wa' aliases, the other does not. Relatedly,
_dedup_and_sort_unavail_msgs weights type == 'yt' and 'wa' while download_video actually
records 'youtube' and 'web.archive:youtube', so its same-epoch tie-break never applies.

Also the Reporter protocol: ConsoleReporter renders and prints, NullReporter is the test
default. Orchestrators emit events; that is what removes 42 print and 18 WARNING calls from
playlist_dl.py without losing any output.
"""
