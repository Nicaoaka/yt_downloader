"""Time: the Epoch type, the canonical int/ISO pair, and the DST defect it exists to kill."""
import datetime
import json
import unittest

from pldl2.model.epoch import (
    Epoch,
    from_iso,
    get_epoch,
    get_latest_epoch,
    to_file_stamp,
    to_iso,
    v1_from_readable_epoch,
    v1_to_readable_epoch,
)


def _find_dst_fallback(start: int = 1_700_000_000, span: int = 4 * 365 * 86400) -> int | None:
    """An epoch whose local wall clock repeats an hour later, or None in a zone without DST."""
    for e in range(start, start + span, 1800):
        if v1_to_readable_epoch(e) == v1_to_readable_epoch(e + 3600):
            return e
    return None


class EpochType(unittest.TestCase):
    """Being an int subclass is the point: it must be substitutable for a raw epoch."""

    def test_is_an_int(self):
        e = Epoch(1_700_000_000)
        self.assertIsInstance(e, int)
        self.assertEqual(e, 1_700_000_000)
        self.assertEqual(e + 1, 1_700_000_001)

    def test_sorts_and_compares_against_raw_ints(self):
        mixed = [1_700_000_005, Epoch(1_700_000_001), 1_700_000_003, Epoch(1_700_000_002)]
        self.assertEqual(sorted(mixed),
                         [1_700_000_001, 1_700_000_002, 1_700_000_003, 1_700_000_005])
        self.assertGreater(Epoch(10), 5)
        self.assertEqual(max(Epoch(10), 20), 20)

    def test_serializes_as_a_number_with_no_encoder(self):
        self.assertEqual(json.dumps({'epoch': Epoch(1_700_000_000)}),
                         '{"epoch": 1700000000}')

    def test_carries_the_conversions(self):
        e = Epoch(1_700_000_000)
        self.assertEqual(e.iso, to_iso(1_700_000_000))
        self.assertEqual(e.file_stamp, to_file_stamp(1_700_000_000))
        self.assertEqual(Epoch.from_iso(e.iso), e)

    def test_repr_shows_both_forms(self):
        text = repr(Epoch(1_700_000_000))
        self.assertIn('1700000000', text)
        self.assertIn('T', text, 'the readable form should be visible when debugging')

    def test_now(self):
        self.assertIsInstance(Epoch.now(), Epoch)

    def test_survives_epochs_near_zero(self):
        """A naive fromtimestamp() raises OSError on Windows here, because local time falls
        before 1970 in a negative-offset zone. Building in UTC has no such hole."""
        for epoch in (0, 1, 100, 3600):
            with self.subTest(epoch=epoch):
                self.assertEqual(Epoch.from_iso(Epoch(epoch).iso), epoch)


class IsoRoundTrip(unittest.TestCase):
    def test_round_trips_exactly(self):
        for epoch in (1_700_000_000, 0, 1, 2_000_000_000, Epoch.now()):
            with self.subTest(epoch=epoch):
                self.assertEqual(from_iso(to_iso(epoch)), epoch)

    def test_carries_an_explicit_offset(self):
        """The offset traveling with each timestamp is what makes DST a non-issue."""
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
    """Two epochs an hour apart share one v1 key, and the reverse mapping keeps only the
    first. Those keys were dict keys in files that are never rewritten, so history rows and
    timeline entries from that hour merged into one bucket."""

    def setUp(self):
        self.epoch = _find_dst_fallback()
        if self.epoch is None:
            self.skipTest('local timezone has no DST fall-back; nothing to collide')

    def test_the_v1_format_really_does_collide(self):
        self.assertEqual(v1_to_readable_epoch(self.epoch),
                         v1_to_readable_epoch(self.epoch + 3600))

    def test_the_v1_reader_loses_the_second_epoch(self):
        key = v1_to_readable_epoch(self.epoch)
        self.assertNotEqual(v1_from_readable_epoch(key), self.epoch + 3600)

    def test_iso_does_not_collide(self):
        """Not "handled better" -- the collision cannot occur, because the offset differs."""
        self.assertNotEqual(to_iso(self.epoch), to_iso(self.epoch + 3600))
        self.assertEqual(from_iso(to_iso(self.epoch)), self.epoch)
        self.assertEqual(from_iso(to_iso(self.epoch + 3600)), self.epoch + 3600)


class FileStamps(unittest.TestCase):
    def test_shape(self):
        self.assertRegex(to_file_stamp(1_700_000_000), r'^\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}$')

    def test_lexicographic_order_matches_chronological_order(self):
        """discover.py finds "the latest" by sorting names, so this must hold."""
        stamps = [to_file_stamp(e) for e in
                  (1_700_000_000, 1_700_003_600, 1_700_090_000, 1_800_000_000)]
        self.assertEqual(stamps, sorted(stamps))

    def test_is_ambiguous_across_the_dst_fallback(self):
        """Documented and accepted: a filename collision is visible and resolvable at write
        time, which is why nothing is keyed by this."""
        epoch = _find_dst_fallback()
        if epoch is None:
            self.skipTest('local timezone has no DST fall-back')
        self.assertEqual(to_file_stamp(epoch), to_file_stamp(epoch + 3600))


class LegacyReader(unittest.TestCase):
    def test_round_trips_a_normal_epoch(self):
        self.assertEqual(v1_from_readable_epoch(v1_to_readable_epoch(1_700_000_000)),
                         1_700_000_000)

    def test_handles_the_malformed_wrapper(self):
        for epoch in (0, 5, -5, 3600):
            with self.subTest(epoch=epoch):
                self.assertEqual(v1_from_readable_epoch(v1_to_readable_epoch(epoch)), epoch)

    def test_returns_an_epoch(self):
        self.assertIsInstance(v1_from_readable_epoch(v1_to_readable_epoch(1_700_000_000)), Epoch)

    def test_rejects_nonsense_loudly(self):
        with self.assertRaises(ValueError):
            v1_from_readable_epoch('not an epoch at all')


class InfoEpochs(unittest.TestCase):
    def test_get_epoch_defaults_explicitly(self):
        self.assertEqual(get_epoch({'epoch': 42}), 42)
        self.assertEqual(get_epoch({}), 0)
        self.assertEqual(get_epoch({}, default=-1), -1)
        self.assertEqual(get_epoch({'epoch': None}), 0)
        self.assertEqual(get_epoch({'epoch': True}), 0, 'bool is not an epoch')

    def test_get_epoch_returns_an_epoch(self):
        self.assertIsInstance(get_epoch({'epoch': 42}), Epoch)
        self.assertIsInstance(get_epoch({}), Epoch)

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
