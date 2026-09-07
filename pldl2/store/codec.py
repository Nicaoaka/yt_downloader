"""JSON encode/decode, key reordering, and the per-kind filters.

One function each way. dataclasses.asdict() covers the write direction; the read direction is
explicit so an unknown or missing field becomes a reported Issue rather than a TypeError --
which matters precisely because the user is allowed to hand-edit these files.

Determinism: sort keys, fixed separators, and json.object_pairs_hook to preserve order on
load.
"""
