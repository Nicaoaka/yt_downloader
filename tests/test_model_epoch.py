"""Time: the Epoch type, the canonical int/ISO pair, and the DST defect it exists to kill."""
import datetime
import unittest

from pldl.model.epoch import (
    Epoch,
    from_iso,
    get_epoch,
    to_file_stamp,
    to_iso,
    from_v1_readable_epoch,
    to_v1_readable_epoch,
)


def _find_dst_fallback(start: int = 1_700_000_000, span: int = 4 * 365 * 86400) -> int | None:
    """An epoch whose local wall clock repeats an hour later, or None in a zone without DST."""
    for e in range(start, start + span, 1800):
        if to_v1_readable_epoch(e) == to_v1_readable_epoch(e + 3600):
            return e
    return None


class EpochType(unittest.TestCase):
    """Being an int subclass is the point: it must be substitutable for a raw epoch."""

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


class DstFallback(unittest.TestCase):
    """Two epochs an hour apart share one v1 key, and the reverse mapping keeps only the
    first. Those keys were dict keys in files that are never rewritten, so history rows and
    timeline entries from that hour merged into one bucket."""

    def setUp(self):
        self.epoch = _find_dst_fallback()
        if self.epoch is None:
            self.skipTest('local timezone has no DST fall-back; nothing to collide')

    def test_iso_does_not_collide(self):
        """Not "handled better" -- the collision cannot occur, because the offset differs."""
        self.assertNotEqual(to_iso(self.epoch), to_iso(self.epoch + 3600))
        self.assertEqual(from_iso(to_iso(self.epoch)), self.epoch)
        self.assertEqual(from_iso(to_iso(self.epoch + 3600)), self.epoch + 3600)


class FileStamps(unittest.TestCase):
    def test_lexicographic_order_matches_chronological_order(self):
        """discover.py finds "the latest" by sorting names, so this must hold."""
        stamps = [to_file_stamp(e) for e in
                  (1_700_000_000, 1_700_003_600, 1_700_090_000, 1_800_000_000)]
        self.assertEqual(stamps, sorted(stamps))


class LegacyReader(unittest.TestCase):
    def test_round_trips_a_normal_epoch(self):
        self.assertEqual(from_v1_readable_epoch(to_v1_readable_epoch(1_700_000_000)),
                         1_700_000_000)

    def test_handles_the_malformed_wrapper(self):
        for epoch in (0, 5, -5, 3600):
            with self.subTest(epoch=epoch):
                self.assertEqual(from_v1_readable_epoch(to_v1_readable_epoch(epoch)), epoch)


class InfoEpochs(unittest.TestCase):
    def test_get_epoch_defaults_explicitly(self):
        self.assertEqual(get_epoch({'epoch': 42}), 42)
        self.assertEqual(get_epoch({}), 0)
        self.assertEqual(get_epoch({}, default=-1), -1)
        self.assertEqual(get_epoch({'epoch': None}), 0)
        self.assertEqual(get_epoch({'epoch': True}), 0, 'bool is not an epoch')


if __name__ == '__main__':
    unittest.main()
