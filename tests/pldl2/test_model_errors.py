"""Error classification, against the real yt-dlp strings.

Verification item 9: these are the messages that sat unused in
`tests/manual_merge_info_tests.py:13-54` -- captured from real runs, ANSI escapes and all --
now doing the job they were collected for.

The distinction the whole thing exists to preserve is `confirmed_unavailable`. v1 returned it
and `wrapper_match_filter` threw it away, so anything it could not classify was treated as a
confirmed failure and frozen for the full 7-day backoff (issue-1 #18).
"""
import unittest

from pldl2.model.errors import (
    Classification,
    ErrorClass,
    Issue,
    Severity,
    classify,
)

E = '\x1b'
RED, OFF = f'{E}[0;31m', f'{E}[0m'


def err(body: str) -> str:
    """A yt-dlp error string exactly as it reaches pldl: ANSI-wrapped ERROR: prefix."""
    return f'{RED}ERROR:{OFF} {body}'


# Verbatim from tests/manual_merge_info_tests.py, captured from real runs.
CORPUS: dict[str, tuple[str, ErrorClass]] = {
    'yt-dlp misc': (
        err('Postprocessing: Conversion failed!'),
        ErrorClass.POSTPROCESSING),
    'timedout': (
        err("\r[download] Got error: HTTPSConnectionPool("
            "host='rr1---sn-a5mekndl.googlevideo.com', port=443): "
            'Read timed out. (read timeout=20.0)'),
        ErrorClass.TIMED_OUT),
    'forbidden': (
        err('unable to download video data: HTTP Error 403: Forbidden'),
        ErrorClass.HTTP_403),
    'yt--terminated_acc': (
        err('[youtube] C5uMV-iK3Ps: Video unavailable. This video is no longer available '
            'because the YouTube account associated with this video has been terminated.'),
        ErrorClass.UNAVAILABLE),
    'yt--removed_vid': (
        err("[youtube] 1yipP37b58c: This video has been removed for violating "
            "YouTube's Terms of Service"),
        ErrorClass.UNAVAILABLE),
    'yt--unavailable': (
        err('[youtube] dvyG8KWrB_E: Video unavailable. This video is not available'),
        ErrorClass.UNAVAILABLE),
    'yt--unavailable-short': (
        err('[youtube] PSrU6IQ9-Gs: Video unavailable'),
        ErrorClass.UNAVAILABLE),
    'yt--private': (
        err("[youtube] qMuLtIC4w64: Private video. Sign in if you've been granted access to "
            'this video. Use --cookies-from-browser or --cookies for the authentication.'),
        ErrorClass.UNAVAILABLE),
    'yt--takedown': (
        err('[youtube] rGDim_zxiqQ: Video unavailable. It was removed following a copyright '
            'removal request by Sony Music Entertainment (Japan) Inc.'),
        ErrorClass.UNAVAILABLE),
    'wa--not_indexed': (
        err('[web.archive:youtube] x5PZVROWgYM: The requested video is not archived or indexed'),
        ErrorClass.UNAVAILABLE),
}

BOT_CHECK = err("[youtube] aaaaaaaaaaa: Sign in to confirm you're not a bot. "
                'Use --cookies-from-browser or --cookies for the authentication.')


class RealCorpus(unittest.TestCase):
    def test_every_captured_message_classifies_as_expected(self):
        for name, (message, expected) in CORPUS.items():
            with self.subTest(case=name):
                self.assertIs(classify(message).error_class, expected)

    def test_no_captured_message_is_unrecognized(self):
        """An UNRECOGNIZED here means a pattern regressed against real data."""
        for name, (message, _) in CORPUS.items():
            with self.subTest(case=name):
                self.assertIsNot(classify(message).error_class, ErrorClass.UNRECOGNIZED)

    def test_ansi_never_reaches_the_classification(self):
        for name, (message, _) in CORPUS.items():
            with self.subTest(case=name):
                self.assertNotIn(E, classify(message).message)

    def test_extractor_tags_are_recovered(self):
        self.assertEqual(classify(CORPUS['yt--private'][0]).tag, 'youtube')
        self.assertEqual(classify(CORPUS['wa--not_indexed'][0]).tag, 'web.archive:youtube')


class UnavailableVsAuth(unittest.TestCase):
    """The distinction issue-1 #18 is about."""

    def test_a_bot_check_is_not_confirmed_unavailable(self):
        result = classify(BOT_CHECK)
        self.assertIs(result.error_class, ErrorClass.AUTH_REQUIRED)
        self.assertFalse(result.confirmed_unavailable,
                         'a bot check means "prove you are human", not "the video is gone"')

    def test_a_private_video_is_confirmed_unavailable_despite_the_cookie_hint(self):
        """yt-dlp appends 'Use --cookies...' to private-video errors too.

        Matching on that hint would reclassify a confirmed-private video as merely needing
        credentials -- the exact opposite of the truth. The discriminator is the reason.
        """
        message = CORPUS['yt--private'][0]
        self.assertIn('--cookies', message)
        result = classify(message)
        self.assertIs(result.error_class, ErrorClass.UNAVAILABLE)
        self.assertTrue(result.confirmed_unavailable)

    def test_an_unrecognized_message_is_not_confirmed_unavailable(self):
        result = classify(err('[youtube] abc: Some brand new failure mode nobody has seen'))
        self.assertIs(result.error_class, ErrorClass.UNRECOGNIZED)
        self.assertFalse(result.confirmed_unavailable)
        self.assertTrue(result.is_transient, 'unknown means retry, not give up for a week')

    def test_only_unavailable_is_confirmed(self):
        for error_class in ErrorClass:
            classification = Classification(error_class=error_class, message='x')
            with self.subTest(error_class=error_class):
                self.assertEqual(classification.confirmed_unavailable,
                                 error_class is ErrorClass.UNAVAILABLE)


class AuthRequired(unittest.TestCase):
    def test_a_not_found_on_an_auth_only_playlist_names_the_real_cause(self):
        """yt-dlp reports a private playlist you cannot see as 'does not exist', so 'LL' with
        bad cookies produces an error pointing at the wrong thing entirely."""
        message = err('[youtube:tab] LL: This playlist does not exist')
        self.assertIs(classify(message).error_class, ErrorClass.UNRECOGNIZED)
        self.assertIs(classify(message, expects_auth=True).error_class,
                      ErrorClass.AUTH_REQUIRED)

    def test_age_gate_and_members_only(self):
        for body in ('[youtube] a: Sign in to confirm your age',
                     "[youtube] a: Join this channel to get access to members-only content"):
            with self.subTest(body=body):
                self.assertIs(classify(err(body)).error_class, ErrorClass.AUTH_REQUIRED)


class Purity(unittest.TestCase):
    def test_classify_never_prints(self):
        """v1's interpret_error_msg warned on stdout and coloured its own warning, on the hot
        path of both the download filter and the display layer."""
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            for message, _ in CORPUS.values():
                classify(message)
            classify('total nonsense')
        self.assertEqual(buf.getvalue(), '')

    def test_classify_is_total(self):
        for message in ('', ' ', 'ERROR:', 'ERROR: ', 'no prefix at all', E, '[]', '[[[' ):
            with self.subTest(message=message):
                self.assertIsInstance(classify(message), Classification)

    def test_a_message_without_the_error_prefix_still_classifies(self):
        self.assertIs(classify('[youtube] a: Video unavailable').error_class,
                      ErrorClass.UNAVAILABLE)


class Issues(unittest.TestCase):
    def test_renders_readably(self):
        issue = Issue(code='roster.missing', message='no _roster.json',
                      severity=Severity.ERROR, path='Some Playlist/_roster.json')
        text = str(issue)
        for part in ('ERROR', 'roster.missing', 'Some Playlist/_roster.json', 'no _roster.json'):
            self.assertIn(part, text)

    def test_defaults_to_a_warning(self):
        self.assertIs(Issue(code='c', message='m').severity, Severity.WARNING)

    def test_is_frozen_and_comparable(self):
        import dataclasses
        a = Issue(code='c', message='m')
        self.assertEqual(a, Issue(code='c', message='m'))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            a.code = 'other'  # type: ignore[misc]


if __name__ == '__main__':
    unittest.main()
