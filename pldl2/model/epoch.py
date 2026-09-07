"""Epoch handling. Ints are canonical; ISO-8601 local strings with an explicit offset are the
readable form.

Replaces to_readable_epoch / from_readable_epoch and the hardcoded `epoch-25200` in the path
templates, whose own comment admits "This will need adjusting if you have daylight savings".
datetime.fromtimestamp(e).astimezone() attaches the *actual* current offset, so DST is right
without touching a template, and the two epochs an hour apart in the fall-back hour stop
collapsing onto one dict key (issue-1 #17).
"""
