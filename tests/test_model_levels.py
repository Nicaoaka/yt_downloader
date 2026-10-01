"""Levels, derivation, and the ordering key.

`rank()` orders sources chronologically, with the level only separating two from the same
second.

Which value wins a field is not this module's business: that is per-field and belongs to the
merge's field updater, and which of those changes is written to the timeline belongs to its
update filter.
"""
import unittest

from pldl.model.levels import (
    PL_InfoLevel,
    V_InfoLevel,
    coerce_pl_level,
    coerce_v_level,
    derive_pl_info_level,
    derive_v_info_level,
    info_rank,
    pl_level_mismatch,
    rank,
    v_level_mismatch,
)


class Ordering(unittest.TestCase):
    """rank() is a sort key: chronological, level only as a tiebreak."""

    def test_orders_chronologically(self):
        self.assertLess(rank(100, V_InfoLevel.FLAT), rank(200, V_InfoLevel.FLAT))

    def test_an_older_richer_source_ranks_lower(self):
        """The point of the change: history reads in the order it happened."""
        self.assertLess(
            rank(1_704_067_200, V_InfoLevel.DOWNLOAD),
            rank(1_788_000_000, V_InfoLevel.FLAT))

    def test_level_only_breaks_a_tie_within_one_second(self):
        self.assertLess(rank(100, V_InfoLevel.FLAT), rank(100, V_InfoLevel.DOWNLOAD))

    def test_is_a_tuple_so_there_is_no_multiplier_to_get_wrong(self):
        self.assertEqual(rank(100, V_InfoLevel.EXTRACT), (100, 2))

    def test_info_rank_reads_the_infodict(self):
        info = {'id': 'a', 'info_level': 'EXTRACT', 'epoch': 1_700_000_000}
        self.assertEqual(info_rank(info), rank(1_700_000_000, V_InfoLevel.EXTRACT))
        self.assertEqual(info_rank(info, epoch=5), rank(5, V_InfoLevel.EXTRACT))

    def test_info_rank_tolerates_a_missing_epoch(self):
        self.assertEqual(info_rank({'id': 'a', 'info_level': 'FLAT'}), rank(0, V_InfoLevel.FLAT))


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
