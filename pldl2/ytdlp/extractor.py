"""The Extractor Protocol and YtDlpExtractor.

    class Extractor(Protocol):
        def extract_flat(self, pl_id, opts) -> PL_InfoDict: ...
        def fetch(self, v_id, opts, *, download: bool) -> FetchResult: ...
        def fetch_url(self, url, opts, *, download: bool) -> FetchResult: ...

This Protocol is the seam that makes the whole lifecycle testable offline, and it replaces
the _no_yt_dlp_downloads flag that currently threads a dev concern through the production
path. Structural typing means FakeExtractor needs no base class.

FetchResult distinguishes **cached / cancelled / failed / ok**. Today download_video returns
None for both "already in archive" and "cancelled", collapsed at _get_dl_result:1074 into a
single CACHED.

ANSI stripping happens here, once, at capture; classification is model/errors.py.
"""
