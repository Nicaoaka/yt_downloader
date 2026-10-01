"""The roster: membership, order, and the rule that a video is never lost."""
import dataclasses
import unittest

from pldl.roster import Roster, RosterEntry


def _roster(*ids, epoch=1000):
    return Roster(
        id='PL_test',
        last_updated=epoch,
        entries=tuple(RosterEntry(id=i, first_seen=epoch, last_seen=epoch) for i in ids),
    )


class RosterQueries(unittest.TestCase):
    def test_index_of_returns_zero_distinguishably_from_absent(self):
        roster = _roster('a', 'b', 'c')
        self.assertEqual(roster.index_of('a'), 0)
        self.assertIsNone(roster.index_of('missing'))

    def test_ids_filters_by_membership(self):
        roster = _roster('a', 'b', 'c')
        roster = roster.with_entries([
            dataclasses.replace(roster.entries[0], in_playlist=True),
            dataclasses.replace(roster.entries[1], in_playlist=False),
            dataclasses.replace(roster.entries[2], in_playlist=True),
        ])
        self.assertEqual(roster.ids(), ('a', 'b', 'c'))
        self.assertEqual(roster.ids(in_playlist=True), ('a', 'c'))
        self.assertEqual(roster.ids(in_playlist=False), ('b',))

    def test_membership_and_lookup(self):
        roster = _roster('a', 'b')
        self.assertIn('a', roster)
        self.assertNotIn('z', roster)
        self.assertEqual(len(roster), 2)
        self.assertIsNone(roster.get('z'))
        self.assertEqual(roster.get('a').id, 'a')

    def test_with_entry_replaces_in_place(self):
        roster = _roster('a', 'b', 'c')
        updated = roster.with_entry(dataclasses.replace(roster.get('b'), in_playlist=False))
        self.assertEqual(updated.ids(), ('a', 'b', 'c'), 'order is preserved')
        self.assertFalse(updated.get('b').in_playlist)


class WithOrder(unittest.TestCase):
    """Applies a sequence; deciding it is the caller's. Must never be able to delete a row."""

    def test_follows_the_sequence(self):
        self.assertEqual(_roster('a', 'b', 'c').with_order(['c', 'a', 'b']).ids(), ('c', 'a', 'b'))

    def test_omitted_ids_keep_their_relative_order_after_the_named_ones(self):
        reordered = _roster('a', 'b', 'c', 'd').with_order(['d', 'b'])
        self.assertEqual(reordered.ids(), ('d', 'b', 'a', 'c'))

    def test_unknown_ids_and_repeats_are_ignored(self):
        reordered = _roster('a', 'b').with_order(['b', 'zzz', 'a', 'b'])
        self.assertEqual(reordered.ids(), ('b', 'a'))

    def test_composes_with_a_membership_fold(self):
        """What merge/ will do: fold membership, then apply the reconciled order."""
        folded = _roster('a', 'b', 'c').with_flat_extraction(['c', 'a'], epoch=2000)
        reordered = folded.with_order(['c', 'a'])
        self.assertEqual(reordered.ids(), ('c', 'a', 'b'))
        self.assertFalse(reordered.get('b').in_playlist)
        self.assertEqual(reordered.last_updated, 2000)


class ApplyFlatExtraction(unittest.TestCase):
    """The only writer of in_playlist. These are its invariants."""

    def test_a_video_gone_from_youtube_keeps_its_row(self):
        folded = _roster('a', 'b', 'c', epoch=1000).with_flat_extraction(['a', 'c'], epoch=2000)
        self.assertEqual(folded.ids(), ('a', 'b', 'c'), 'b must still be present')
        self.assertFalse(folded.get('b').in_playlist)
        self.assertTrue(folded.get('a').in_playlist)

    def test_a_disappeared_video_keeps_its_last_seen(self):
        folded = _roster('a', 'b', epoch=1000).with_flat_extraction(['a'], epoch=2000)
        self.assertEqual(folded.get('b').last_seen, 1000, 'last_seen is when it was last there')
        self.assertEqual(folded.get('a').last_seen, 2000)

    def test_a_video_can_come_back(self):
        roster = _roster('a', 'b', epoch=1000).with_flat_extraction(['a'], epoch=2000)
        self.assertFalse(roster.get('b').in_playlist)

        returned = roster.with_flat_extraction(['a', 'b'], epoch=3000)
        self.assertTrue(returned.get('b').in_playlist)
        self.assertEqual(returned.get('b').last_seen, 3000)
        self.assertEqual(returned.get('b').first_seen, 1000, 'first_seen never moves')

    def test_new_ids_are_added(self):
        folded = _roster('a', epoch=1000).with_flat_extraction(['a', 'new'], epoch=2000)
        self.assertEqual(folded.ids(), ('a', 'new'))
        self.assertEqual(folded.get('new').first_seen, 2000)

    def test_existing_order_is_kept_and_new_ids_follow(self):
        """Membership only: reordering is `with_order`, decided by merge/."""
        folded = _roster('a', 'b', 'c').with_flat_extraction(['c', 'x', 'a', 'y'], epoch=2000)
        self.assertEqual(folded.ids(), ('a', 'b', 'c', 'x', 'y'))

    def test_last_updated_moves_forward_only(self):
        folded = _roster('a', epoch=5000).with_flat_extraction(['a'], epoch=1000)
        self.assertEqual(folded.last_updated, 5000)

    def test_folding_an_empty_extraction_marks_everything_gone(self):
        folded = _roster('a', 'b').with_flat_extraction([], epoch=2000)
        self.assertEqual(folded.ids(), ('a', 'b'))
        self.assertEqual(folded.ids(in_playlist=True), ())

    def test_first_seen_only_moves_earlier(self):
        """Folding an older capture after a newer one -- re-importing an old flat file, or a
        migrator walking the archive backwards -- must correct first_seen, not keep whichever
        was folded first."""
        roster = Roster(id='p').with_flat_extraction(['a'], epoch=5000)
        self.assertEqual(roster.first_seen, 5000)
        self.assertEqual(roster.get('a').first_seen, 5000)

        earlier = roster.with_flat_extraction(['a'], epoch=1000)
        self.assertEqual(earlier.first_seen, 1000, 'the playlist was recorded earlier than we knew')
        self.assertEqual(earlier.get('a').first_seen, 1000)
        self.assertEqual(earlier.get('a').last_seen, 5000, 'last_seen only moves later')
        self.assertEqual(earlier.last_updated, 5000)

    def test_first_seen_does_not_depend_on_fold_order(self):
        forwards = Roster(id='p').with_flat_extraction(['a'], 1000).with_flat_extraction(['a'], 5000)
        backwards = Roster(id='p').with_flat_extraction(['a'], 5000).with_flat_extraction(['a'], 1000)
        self.assertEqual(forwards.get('a').first_seen, backwards.get('a').first_seen)
        self.assertEqual(forwards.first_seen, backwards.first_seen)

    def test_first_seen_is_set_once(self):
        first = Roster(id='p').with_flat_extraction(['a'], epoch=2000)
        self.assertEqual(first.first_seen, 2000)
        later = first.with_flat_extraction(['a'], epoch=9000)
        self.assertEqual(later.first_seen, 2000, 'when the playlist was first recorded')
        self.assertEqual(later.last_updated, 9000)


class ContextShape(unittest.TestCase):
    """The roster holds context; merge/ decides it.

    Resolving two candidate values follows the merge's policy and lives with the field
    resolvers, so there is one implementation rather than two that drift apart.
    """

    def test_storing_context_for_an_unknown_id_is_a_no_op(self):
        roster = Roster(id='p').with_flat_extraction(['a'], epoch=1000)
        self.assertEqual(roster.with_video_context('zzz', {'title': 'T'}), roster)

    def test_storing_context_leaves_last_updated_alone(self):
        """last_updated answers "how current is membership", not "how current is the text"."""
        roster = Roster(id='p').with_flat_extraction(['a'], epoch=1000)
        self.assertEqual(roster.with_video_context('a', {'title': 'T'}).last_updated, 1000)


if __name__ == '__main__':
    unittest.main()
