"""The merge updaters: a binary operator over candidates per field, and the table that picks one."""
import unittest
from itertools import chain, permutations

from pldl2.merge.updaters import (
    COMMON_TIMELINE_KEYS,
    COMMON_UPDATER,
    PL_UPDATER,
    ROSTER_UPDATER,
    ZERO_CANDIDATE,
    Candidate,
    MergeUpdaterMap,
    apply_updater,
    fill_absent,
    keep,
    latest,
    latest_not_none,
    maximum,
    richest_latest,
    richest_latest_not_none,
    unwrap_candidates,
)
from pldl2.model.infodicts import NO_VALUE
from pldl2.model.levels import Rank, V_InfoLevel
from pldl2.model.roster import PLAYLIST_CONTEXT_SOURCES, VIDEO_CONTEXT_SOURCES

VALUES = (NO_VALUE, None, 0, 5, 10, 'x')
FLAT, EXTRACT, DOWNLOAD = V_InfoLevel.FLAT, V_InfoLevel.EXTRACT, V_InfoLevel.DOWNLOAD


def C(value, epoch=0, level=FLAT) -> Candidate:
    return Candidate(value, Rank(epoch, level))


class Rules(unittest.TestCase):
    def test_keep_never_changes(self):
        for cur in VALUES:
            for new in VALUES:
                with self.subTest(current=cur, incoming=new):
                    current = C(cur, 1)
                    self.assertIs(keep(current, C(new, 2)), current)

    def test_latest_is_decided_by_rank_not_by_arrival(self):
        self.assertEqual(latest(C('old', 1), C('new', 2)).value, 'new')
        self.assertEqual(latest(C('new', 2), C('old', 1)).value, 'new',
                         'an older source arriving later does not win')
        self.assertEqual(latest(C('a', 5), C('b', 5)).value, 'b', 'a tie goes to the incoming')

    def test_latest_takes_none_and_absent(self):
        self.assertIsNone(latest(C('old', 1), C(None, 2)).value)
        self.assertIs(latest(C('old', 1), C(NO_VALUE, 2)).value, NO_VALUE,
                      'the newest source lacking the key removes it')

    def test_latest_not_none_leaves_the_current_candidate_untouched(self):
        """Not just the value: the rank stays too, which is what lets an older real value
        still win afterwards."""
        cur = C('old', 1)
        self.assertIs(latest_not_none(cur, C(None, 3)), cur)
        self.assertIs(latest_not_none(cur, C(NO_VALUE, 3)), cur)
        self.assertEqual(latest_not_none(cur, C('new', 2)).value, 'new')
        self.assertIs(latest_not_none(ZERO_CANDIDATE, C(None, 3)), ZERO_CANDIDATE, 'an unknown stays unknown')

    def test_fill_absent_writes_once(self):
        self.assertEqual(fill_absent(ZERO_CANDIDATE, C('first', 1)).value, 'first')
        self.assertEqual(fill_absent(C('first', 1), C('second', 2)).value, 'first')
        self.assertEqual(fill_absent(C('first', 1), C(NO_VALUE, 2)).value, 'first')

    def test_maximum_only_grows(self):
        self.assertEqual(maximum(C(5), C(10)).value, 10)
        self.assertEqual(maximum(C(10), C(5)).value, 10)
        self.assertEqual(maximum(ZERO_CANDIDATE, C(5)).value, 5)
        self.assertEqual(maximum(C(None), C(5)).value, 5)
        self.assertEqual(maximum(C(5), C(None)).value, 5)
        self.assertEqual(maximum(C(5), C(NO_VALUE)).value, 5)

    def test_maximum_keeps_the_current_when_the_two_do_not_compare(self):
        self.assertEqual(maximum(C(5), C('x')).value, 5)

    def test_richest_prefers_level_over_recency(self):
        """The `thumbnails` case: a flat extraction carries 4, a full one 45. A fresh flat
        must not replace the full one, and a fresh full one must replace the flat one."""
        full = C(45, 100, DOWNLOAD)
        self.assertIs(richest_latest(full, C(4, 300, FLAT)), full)
        self.assertEqual(richest_latest(C(4, 100, FLAT), C(45, 300, DOWNLOAD)).value, 45)
        self.assertEqual(richest_latest(C(4, 100, FLAT), C(45, 50, DOWNLOAD)).value, 45,
                         'even an older richer source wins')

    def test_richest_falls_back_to_latest_among_equals(self):
        self.assertEqual(richest_latest(C('a', 100, FLAT), C('b', 200, FLAT)).value, 'b')
        self.assertEqual(richest_latest(C('b', 200, FLAT), C('a', 100, FLAT)).value, 'b')

    def test_richest_not_none_ignores_blanks_at_any_level(self):
        cur = C(4, 100, FLAT)
        self.assertIs(richest_latest_not_none(cur, C(None, 300, DOWNLOAD)), cur)
        self.assertIs(richest_latest_not_none(cur, C(NO_VALUE, 300, DOWNLOAD)), cur)


class Provenance(unittest.TestCase):
    """A rank only moves when a value is accepted, so fold order cannot change final values."""

    SOURCES = (
        {'epoch': 1, 'simple': 'init',    'data': 'First'},
        {'epoch': 3, 'simple': 'Final',   'data': None},    # data ignored, not "latest" for data
        {'epoch': 2, 'simple': 'ignored', 'data': 'Final'},
    )

    @classmethod
    def fold(cls, sources, updater):
        merged: dict[str, Candidate] = {}
        timeline = []
        for src in sources:
            rank = Rank(src['epoch'], FLAT)
            for key in sorted(set(src) - {'epoch'}):
                if apply_updater(merged, key, Candidate(src.get(key, NO_VALUE), rank), updater):
                    timeline.append((src['epoch'], key, merged[key].value))
        return unwrap_candidates(merged), timeline

    def test_a_rejected_none_does_not_block_an_older_real_value(self):
        values, _ = self.fold(self.SOURCES, latest_not_none)
        self.assertEqual(values, {'simple': 'Final', 'data': 'Final'})

    def test_final_values_are_the_same_in_every_fold_order(self):
        results = {frozenset(self.fold(order, latest_not_none)[0].items())
                   for order in permutations(self.SOURCES)}
        self.assertEqual(len(results), 1)

    def test_a_removal_is_order_independent_too(self):
        """Under `latest`, the newest source lacking the key removes it -- and must keep it
        removed even when the older source that had it is folded afterwards. That needs the
        removal's rank to survive, which is why a `NO_VALUE` winner is stored, not popped."""
        sources = ({'epoch': 2, 'k': 'A'}, {'epoch': 5})
        for order in permutations(sources):
            with self.subTest(order=[s['epoch'] for s in order]):
                merged: dict[str, Candidate] = {}
                for src in order:
                    apply_updater(merged, 'k',
                                 Candidate(src.get('k', NO_VALUE), Rank(src['epoch'], FLAT)), latest)
                self.assertEqual(unwrap_candidates(merged), {})

    def test_fold_order_decides_what_the_timeline_records(self):
        """Values are order-independent; the timeline is not. Out of order, `simple` was
        never 'ignored' at any point, so no entry says it was."""
        _, as_given = self.fold(self.SOURCES, latest_not_none)
        _, chronological = self.fold(sorted(self.SOURCES, key=lambda s: s['epoch']),
                                     latest_not_none)
        self.assertNotIn((2, 'simple', 'ignored'), as_given)
        self.assertIn((2, 'simple', 'ignored'), chronological)
        self.assertEqual(chronological, sorted(chronological))


class Tables(unittest.TestCase):
    def test_unlisted_keys_get_the_default(self):
        table = MergeUpdaterMap.grouped({('a', 'b'): keep}, default=latest)
        self.assertIs(table['a'], keep)
        self.assertIs(table['b'], keep)
        self.assertIs(table['zzz'], latest)

    def test_a_key_under_two_updaters_is_refused(self):
        with self.assertRaises(ValueError):
            MergeUpdaterMap.grouped({('a',): keep, ('a', 'b'): latest}, default=latest)

    def test_the_map_is_read_only(self):
        table = MergeUpdaterMap({'a': keep}, latest)
        with self.assertRaises(TypeError):
            table.updater_map['b'] = latest  # type: ignore[index]


class ResolveInto(unittest.TestCase):
    def test_writes_and_reports_a_change(self):
        merged = {'title': C('old', 1)}
        self.assertTrue(apply_updater(merged, 'title', C('new', 2), latest))
        self.assertEqual(merged['title'], C('new', 2))

    def test_an_equal_value_is_not_a_change_but_the_rank_still_moves(self):
        merged = {'title': C('same', 1)}
        self.assertFalse(apply_updater(merged, 'title', C('same', 2), latest))
        self.assertEqual(merged['title'].rank, Rank(2, FLAT), 'the newer source confirmed it')

    def test_no_value_out_is_a_change_and_leaves_a_tombstone(self):
        merged = {'title': C('old', 1), 'other': C(1, 1)}
        self.assertTrue(apply_updater(merged, 'title', C(NO_VALUE, 2), latest))
        self.assertEqual(merged['title'], C(NO_VALUE, 2), 'the rank of the removal is kept')
        self.assertEqual(unwrap_candidates(merged), {'other': 1}, 'and projected away')

    def test_removing_an_absent_key_is_not_a_change(self):
        merged: dict[str, Candidate] = {}
        self.assertFalse(apply_updater(merged, 'title', C(NO_VALUE, 2), latest))
        self.assertEqual(unwrap_candidates(merged), {})

    def test_unwrap_drops_tombstones_only(self):
        merged = {'b': C(2), 'a': C(1), 'c': C(NO_VALUE), 'd': C(None)}
        self.assertEqual(unwrap_candidates(merged), {'b': 2, 'a': 1, 'd': None})

    def test_none_is_stored_not_removed(self):
        merged = {'title': C('old', 1)}
        self.assertTrue(apply_updater(merged, 'title', C(None, 2), latest))
        self.assertIsNone(merged['title'].value)


class TheTables(unittest.TestCase):
    """Each row of COMMON_UPDATER exists for a case seen in real captures; fold that case."""

    @staticmethod
    def fold(table, *sources):
        """`sources` are `(epoch, level, payload)`; keys any source mentions are folded."""
        merged: dict[str, Candidate] = {}
        keys = sorted({k for _, _, payload in sources for k in payload})
        for epoch, level, payload in sources:
            for key in keys:
                apply_updater(merged, key, Candidate(payload.get(key, NO_VALUE), Rank(epoch, level)),
                              table[key])
        return unwrap_candidates(merged)

    def test_the_default_is_latest_not_none(self):
        self.assertIs(COMMON_UPDATER['title'], latest_not_none)
        self.assertIs(COMMON_UPDATER['view_count'], latest_not_none, 'a drop is information')

    def test_a_dead_video_does_not_blank_its_title(self):
        """A flat extraction of a removed video carries `title: None, channel: None`."""
        merged = self.fold(COMMON_UPDATER,
                           (100, EXTRACT, {'title': 'T', 'channel': 'C'}),
                           (200, FLAT, {'title': None, 'channel': None}))
        self.assertEqual(merged, {'title': 'T', 'channel': 'C'})

    def test_thumbnails_keep_the_fuller_extraction(self):
        merged = self.fold(COMMON_UPDATER,
                           (100, DOWNLOAD, {'thumbnails': list(range(45))}),
                           (200, FLAT, {'thumbnails': list(range(4))}))
        self.assertEqual(len(merged['thumbnails']), 45)

    def test_a_flat_reference_is_superseded_by_a_real_extraction_for_good(self):
        """`_type: url`, `ie_key`, `url` describe an unresolved entry. A full extraction has
        none of them and must remove them; a later flat must not bring them back."""
        merged = self.fold(COMMON_UPDATER,
                           (100, FLAT, {'_type': 'url', 'ie_key': 'Youtube', 'title': 'T'}),
                           (200, EXTRACT, {'title': 'T', 'extractor': 'youtube'}),
                           (300, FLAT, {'_type': 'url', 'ie_key': 'Youtube', 'title': 'T'}))
        self.assertEqual(merged, {'title': 'T', 'extractor': 'youtube'})

    def test_a_download_keeps_describing_the_file_on_disk(self):
        """A fresher extraction that downloaded nothing selected a different format; the
        merged `ext` must stay the one that was written."""
        merged = self.fold(COMMON_UPDATER,
                           (100, DOWNLOAD, {'ext': 'mkv', 'format_id': '303+251'}),
                           (200, EXTRACT, {'ext': 'webm', 'format_id': '248+251'}))
        self.assertEqual(merged, {'ext': 'mkv', 'format_id': '303+251'})

    def test_the_roster_whitelist_is_exactly_the_context_sources(self):
        """Derived, not listed, so it cannot drift from what the roster can hold."""
        expected = set(chain.from_iterable(VIDEO_CONTEXT_SOURCES.values()))
        expected |= set(chain.from_iterable(PLAYLIST_CONTEXT_SOURCES.values()))
        self.assertEqual(set(ROSTER_UPDATER.updater_map), expected)
        self.assertIs(ROSTER_UPDATER['title'], latest_not_none,
                      'a recent flat takes the title over an old download')
        self.assertIs(ROSTER_UPDATER['formats'], keep, 'the roster is not a second merge')

    def test_a_flat_only_video_still_gets_a_webpage_url_in_context(self):
        """A flat entry has `url`, never `webpage_url`."""
        self.assertIn('url', VIDEO_CONTEXT_SOURCES['webpage_url'])
        self.assertIs(ROSTER_UPDATER['url'], latest_not_none)

    def test_playlist_fields_take_the_newest_non_none(self):
        merged = self.fold(PL_UPDATER,
                           (100, FLAT, {'title': 'Old', 'playlist_count': 5}),
                           (200, FLAT, {'title': 'New', 'playlist_count': None}))
        self.assertEqual(merged, {'title': 'New', 'playlist_count': 5})

    def test_the_timeline_records_identity_not_churn(self):
        for recorded in ('title', 'uploader', 'availability', 'live_status', 'extractor'):
            self.assertIn(recorded, COMMON_TIMELINE_KEYS)
        for churn in ('view_count', 'like_count', 'formats', 'epoch', 'duration_string'):
            self.assertNotIn(churn, COMMON_TIMELINE_KEYS)


if __name__ == '__main__':
    unittest.main()
