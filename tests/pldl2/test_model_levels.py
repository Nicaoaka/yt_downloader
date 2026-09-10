"""Levels, derivation, and the ranking rule.

The parity test here is step 1's gate: `rank()` must agree with v1's private
`_merge_v_sort_key` on every input that function could handle. Ranking decides which of two
infodicts wins a field during a merge, so a silent change would rewrite the record's meaning
rather than its shape.

That test imports from the old `pldl` package on purpose -- both packages coexist until the
step-12 cutover, which is what makes a parity gate possible at all. **Delete it at cutover**,
along with `pldl/`.
"""
import random
import unittest

from pldl.post_processing.merge_infos import _merge_v_sort_key
from pldl2.model.levels import (
    LARGE_TIME_DELTA,
    PL_InfoLevel,
    V_InfoLevel,
    coerce_pl_level,
    coerce_v_level,
    derive_pl_info_level,
    derive_v_info_level,
    pl_level_mismatch,
    rank,
    info_rank,
    v_level_mismatch,
)


class RankParity(unittest.TestCase):
    """rank() vs v1's _merge_v_sort_key. The step-1 gate."""

    def test_matches_legacy_sort_key_on_random_inputs(self):
        rng = random.Random(12345)
        inputs = [
            *V_InfoLevel,                                   # the enum itself
            *[lvl.name for lvl in V_InfoLevel],             # valid names
            None,                                           # explicit absence
            'NOT_A_LEVEL', '', 'flat', 'Download',          # unrecognized strings
        ]
        for _ in range(2000):
            level = rng.choice(inputs)
            epoch = rng.choice([
                0, 1, -1,
                rng.randint(-10**9, 10**9),
                rng.randint(1_700_000_000, 1_800_000_000),
            ])
            with self.subTest(level=level, epoch=epoch):
                self.assertEqual(rank(level, epoch), _merge_v_sort_key(level, epoch))

    def test_legacy_key_cannot_handle_an_int_level_but_rank_can(self):
        """The documented divergence, and the reason for it.

        A v1 file can carry `"info_level": 0`, because download_video_generic stored the enum
        rather than its name and JSON serialized it to an int. _merge_v_sort_key converts str
        but not int, so 0 reaches `.value` and raises -- which is what makes such a file
        permanently un-re-addable (issue-1 #23).
        """
        with self.assertRaises(AttributeError):
            _merge_v_sort_key(0, 1_700_000_000)  # type: ignore[arg-type]

        self.assertEqual(rank(0, 1_700_000_000), rank(V_InfoLevel.NONE, 1_700_000_000))
        self.assertEqual(rank(3, 5), rank(V_InfoLevel.DOWNLOAD, 5))


class Ranking(unittest.TestCase):
    def test_level_dominates_epoch(self):
        """A richer old extraction outranks a poorer new one. The whole point."""
        old_download = rank(V_InfoLevel.DOWNLOAD, 1_600_000_000)
        new_flat = rank(V_InfoLevel.FLAT, 1_800_000_000)
        self.assertGreater(old_download, new_flat)

    def test_epoch_breaks_ties_within_a_level(self):
        self.assertGreater(rank(V_InfoLevel.FLAT, 200), rank(V_InfoLevel.FLAT, 100))

    def test_no_realistic_epoch_spread_bridges_a_level(self):
        far_future = 32_503_680_000  # year 3000
        self.assertLess(rank(V_InfoLevel.NONE, far_future), rank(V_InfoLevel.FLAT, 0))
        self.assertGreater(LARGE_TIME_DELTA, far_future)

    def test_info_rank_reads_the_infodict(self):
        info = {'id': 'a', 'info_level': 'EXTRACT', 'epoch': 1_700_000_000}
        self.assertEqual(info_rank(info), rank(V_InfoLevel.EXTRACT, 1_700_000_000))
        self.assertEqual(info_rank(info, epoch=5), rank(V_InfoLevel.EXTRACT, 5))

    def test_info_rank_tolerates_a_missing_epoch(self):
        self.assertEqual(info_rank({'id': 'a', 'info_level': 'FLAT'}), rank(V_InfoLevel.FLAT, 0))


class Coercion(unittest.TestCase):
    def test_is_total_over_its_input_type(self):
        cases = [
            (V_InfoLevel.EXTRACT, V_InfoLevel.EXTRACT),
            ('DOWNLOAD', V_InfoLevel.DOWNLOAD),
            (2, V_InfoLevel.EXTRACT),
            (None, V_InfoLevel.NONE),
            ('nonsense', V_InfoLevel.NONE),
            (99, V_InfoLevel.NONE),
            (-1, V_InfoLevel.NONE),
            ([], V_InfoLevel.NONE),
            (object(), V_InfoLevel.NONE),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertIs(coerce_v_level(value), expected)

    def test_bool_is_not_an_int_here(self):
        """True would otherwise coerce to FLAT, which is nonsense and hard to spot."""
        self.assertIs(coerce_v_level(True), V_InfoLevel.NONE)
        self.assertIs(coerce_v_level(False), V_InfoLevel.NONE)

    def test_playlist_levels_coerce_the_same_way(self):
        self.assertIs(coerce_pl_level('MERGE'), PL_InfoLevel.MERGE)
        self.assertIs(coerce_pl_level(4), PL_InfoLevel.MERGE)
        self.assertIs(coerce_pl_level('nope'), PL_InfoLevel.NONE)


class Derivation(unittest.TestCase):
    def test_video_levels_from_content(self):
        cases = [
            ({}, V_InfoLevel.NONE),
            (None, V_InfoLevel.NONE),
            ({'id': 'a'}, V_InfoLevel.NONE),
            ({'id': 'a', 'channel': 'c'}, V_InfoLevel.FLAT),
            ({'id': 'a', 'extractor_key': 'YoutubeWebArchive'}, V_InfoLevel.FLAT),
            ({'id': 'a', 'channel': 'c', 'extractor': 'youtube'}, V_InfoLevel.EXTRACT),
            ({'id': 'a', 'extractor': 'youtube', 'requested_downloads': [{}]},
             V_InfoLevel.DOWNLOAD),
        ]
        for info, expected in cases:
            with self.subTest(info=info):
                self.assertIs(derive_v_info_level(info), expected)

    def test_playlist_levels_from_content(self):
        flat_entry = {'id': 'a', 'channel': 'c'}
        extracted = {'id': 'a', 'extractor': 'youtube'}
        cases = [
            ({'id': 'p', 'entries': [flat_entry]}, PL_InfoLevel.FLAT),
            ({'id': 'p', 'entries': [flat_entry], 'merge_timeline': {}},
             PL_InfoLevel.MERGE_FLAT),
            ({'id': 'p', 'entries': [extracted]}, PL_InfoLevel.NORMAL),
            ({'id': 'p', 'entries': [extracted], 'merge_timeline': {}}, PL_InfoLevel.MERGE),
        ]
        for info, expected in cases:
            with self.subTest(expected=expected):
                self.assertIs(derive_pl_info_level(info), expected)

    def test_derivation_never_prints(self):
        """L0 does not print."""
        import contextlib
        import io as _io
        buf = _io.StringIO()
        with contextlib.redirect_stdout(buf):
            derive_v_info_level({'id': 'a', 'info_level': 'DOWNLOAD'})
            derive_pl_info_level({'id': 'p', 'entries': [], 'info_level': 'MERGE'})
        self.assertEqual(buf.getvalue(), '')

    def test_mismatch_is_reported_as_a_value(self):
        info = {'id': 'a', 'info_level': 'DOWNLOAD'}  # claims DOWNLOAD, content says NONE
        self.assertEqual(v_level_mismatch(info), ('DOWNLOAD', V_InfoLevel.NONE))

    def test_no_mismatch_when_they_agree_or_nothing_is_declared(self):
        self.assertIsNone(v_level_mismatch({'id': 'a', 'channel': 'c', 'info_level': 'FLAT'}))
        self.assertIsNone(v_level_mismatch({'id': 'a', 'channel': 'c'}))
        self.assertIsNone(v_level_mismatch({}))

    def test_playlist_mismatch(self):
        self.assertEqual(
            pl_level_mismatch({'id': 'p', 'entries': [], 'info_level': 'MERGE'}),
            ('MERGE', PL_InfoLevel.FLAT))


if __name__ == '__main__':
    unittest.main()
