"""Time: the canonical int/ISO pair, and the DST defect it exists to kill."""
import datetime
import unittest

from pldl2.model.epoch import (
    epoch_now,
    from_iso,
    from_legacy_key,
    get_epoch,
    get_latest_epoch,
    to_file_stamp,
    to_iso,
    to_legacy_key,
)


def _find_dst_fallback(start: int = 1_700_000_000, span: int = 4 * 365 * 86400) -> int | None:
    """An epoch whose local wall-clock repeats an hour later, or None in a zone without DST."""
    for e in range(start, start + span, 1800):
        if to_legacy_key(e) == to_legacy_key(e + 3600):
            return e
    return None


class IsoRoundTrip(unittest.TestCase):
    def test_round_trips_exactly(self):
        for epoch in (1_700_000_000, 0, 1, 2_000_000_000, epoch_now()):
            with self.subTest(epoch=epoch):
                self.assertEqual(from_iso(to_iso(epoch)), epoch)

    def test_carries_an_explicit_offset(self):
        """The offset travelling with each timestamp is what makes DST a non-issue."""
        parsed = datetime.datetime.fromisoformat(to_iso(1_700_000_000))
        self.assertIsNotNone(parsed.tzinfo)
        self.assertIsNotNone(parsed.utcoffset())

    def test_is_readable_and_local(self):
        text = to_iso(1_700_000_000)
        self.assertRegex(text, r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$')
        self.assertEqual(
            text[:19],
            datetime.datetime.fromtimestamp(1_700_000_000).strftime('%Y-%m-%dT%H:%M:%S'))


class DstFallback(unittest.TestCase):
    """issue-1 #17, confirmed: two epochs an hour apart share one v1 key, and the reverse
    mapping keeps only the first. Those keys were dict keys in files that are never
    rewritten, so history rows and timeline entries from that hour merged into one bucket."""

    def setUp(self):
        self.epoch = _find_dst_fallback()
        if self.epoch is None:
            self.skipTest('local timezone has no DST fall-back; nothing to collide')

    def test_the_v1_format_really_does_collide(self):
        self.assertEqual(to_legacy_key(self.epoch), to_legacy_key(self.epoch + 3600))

    def test_the_v1_reader_loses_the_second_epoch(self):
        key = to_legacy_key(self.epoch)
        self.assertNotEqual(from_legacy_key(key), self.epoch + 3600)

    def test_iso_does_not_collide(self):
        """Not "handled better" -- the collision cannot occur, because the offset differs."""
        self.assertNotEqual(to_iso(self.epoch), to_iso(self.epoch + 3600))
        self.assertEqual(from_iso(to_iso(self.epoch)), self.epoch)
        self.assertEqual(from_iso(to_iso(self.epoch + 3600)), self.epoch + 3600)


class FileStamps(unittest.TestCase):
    def test_matches_the_v1_filename_shape_so_sorted_globs_still_work(self):
        self.assertRegex(to_file_stamp(1_700_000_000), r'^\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}$')

    def test_lexicographic_order_matches_chronological_order(self):
        """discover.py finds "the latest" by sorting names, so this must hold."""
        stamps = [to_file_stamp(e) for e in
                  (1_700_000_000, 1_700_003_600, 1_700_090_000, 1_800_000_000)]
        self.assertEqual(stamps, sorted(stamps))

    def test_is_documented_as_not_injective(self):
        """The docstring promises this, and store/ is told to disambiguate. Pin the promise."""
        self.assertIn('Not injective', to_file_stamp.__doc__ or '')


class LegacyReader(unittest.TestCase):
    def test_round_trips_a_normal_epoch(self):
        self.assertEqual(from_legacy_key(to_legacy_key(1_700_000_000)), 1_700_000_000)

    def test_handles_the_malformed_wrapper(self):
        for epoch in (0, 5, -5, 3600):
            with self.subTest(epoch=epoch):
                self.assertEqual(from_legacy_key(to_legacy_key(epoch)), epoch)

    def test_rejects_nonsense_loudly(self):
        with self.assertRaises(ValueError):
            from_legacy_key('not an epoch at all')


class InfoEpochs(unittest.TestCase):
    def test_get_epoch_defaults_explicitly(self):
        """v1 used -epoch_now(), so a missing epoch became a large negative that still
        compared and sorted like a real one."""
        self.assertEqual(get_epoch({'epoch': 42}), 42)
        self.assertEqual(get_epoch({}), 0)
        self.assertEqual(get_epoch({}, default=-1), -1)
        self.assertEqual(get_epoch({'epoch': None}), 0)
        self.assertEqual(get_epoch({'epoch': True}), 0, 'bool is not an epoch')

    def test_get_latest_epoch_spans_playlist_and_entries(self):
        pl = {'epoch': 100, 'entries': [{'epoch': 50}, {'epoch': 300}, {'id': 'no epoch'}]}
        self.assertEqual(get_latest_epoch(pl), 300)

    def test_get_latest_epoch_with_nothing_to_go_on(self):
        self.assertEqual(get_latest_epoch({'entries': []}), 0)
        self.assertEqual(get_latest_epoch({'entries': []}, default=-7), -7)

    def test_get_latest_epoch_tolerates_a_missing_entries_key(self):
        self.assertEqual(get_latest_epoch({'epoch': 9}), 9)


if __name__ == '__main__':
    unittest.main()
