"""Integrity checks. **Returns problems; never prompts.**

    issues = record.check()      # -> list[Issue], pure, no I/O beyond reading
    record.repair(issues)        # explicit, caller-chosen

Today _validate_dl_archive_sync (playlist_dl.py:511-559) prints a diff, blocks on
utils.input_string, raises, appends to a file and mutates two arguments -- inside the
constructor. The facade may still prompt; the store never does. This is also what makes the
store testable at all.

Path-template drift validation lives here too, where the metadata is actually loaded, which
is what breaks the config -> playlist_dl import cycle.
"""
