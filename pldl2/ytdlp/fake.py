"""FakeExtractor -- an in-memory Extractor for tests. Scripted responses, no network, no sleeps.

Structural typing means it needs no base class. This is what makes the full
open -> refresh -> download -> merge -> commit lifecycle testable offline, and it is also the
assertion vehicle for the cookie pre-flight: a FakeExtractor that fails the test if it is
called at all proves the refusal happened *before* any yt-dlp call.
"""
