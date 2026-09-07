"""
The on-disk format version, in one place.

Every pldl-owned document -- _roster.json, _metadata.json, and every stored capture -- writes
`schema_version`. That single field is what turns a future format change into a migration
instead of a break, and it is the reason store/migrate.py can be the only module that knows
what v1 looked like.

Bump this **only** alongside a migration step in store/migrate.py, and only for a change that
a v(N-1) reader would get wrong. Adding an optional field that older readers can ignore is
not a version bump.
"""
from __future__ import annotations

__all__ = ['SCHEMA_VERSION', 'LEGACY_SCHEMA_VERSION']

SCHEMA_VERSION = 2
"""The format this package reads and writes."""

LEGACY_SCHEMA_VERSION = 1
"""The pldl v1 format: metadata pointers, `_merge_flat`, infodicts with pldl keys inlined.

v1 files carry no `schema_version` field at all -- its absence *is* the version marker.
"""
