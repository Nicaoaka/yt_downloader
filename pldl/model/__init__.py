"""Generic building blocks every stage uses: time, and the on-disk schema version.

Imports nothing from the rest of pldl.
"""
from __future__ import annotations

from pldl.model.epoch import (
    EPOCH_ZERO,
    Epoch,
    from_iso,
    from_v1_readable_epoch,
    get_epoch,
    get_latest_epoch,
    to_file_stamp,
    to_iso,
    to_v1_readable_epoch,
)
from pldl.model.schema import LEGACY_SCHEMA_VERSION, SCHEMA_VERSION

__all__ = [  # noqa: RUF022
    'Epoch', 'EPOCH_ZERO', 'get_epoch', 'get_latest_epoch',
    'to_iso', 'from_iso', 'to_file_stamp',
    'to_v1_readable_epoch', 'from_v1_readable_epoch',
    'SCHEMA_VERSION', 'LEGACY_SCHEMA_VERSION',
]
