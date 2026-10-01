"""The roster, timeline and envelope.

These carry the invariants the record depends on, so the tests are written as statements of
those invariants rather than as coverage of the methods.
"""
import dataclasses
import unittest

from pldl.model.epoch import Epoch
from pldl.model.errors import UnavailableInfo
from pldl.model.levels import PL_InfoLevel, V_InfoLevel
from pldl.model.playlists import Capture, MergePlaylist
from pldl.model.roster import (
    PLAYLIST_CONTEXT_SOURCES,
    VIDEO_CONTEXT_SOURCES,
    PlaylistContext,
    Roster,
    RosterEntry,
    VideoContext,
)
from pldl.model.timeline import FieldUpdate, MergeTimelineEntry, VideoTimeline
from pldl.model.videos import VideoEntry

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

    def test_is_frozen(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            _roster('a').id = 'other'  # type: ignore[misc]

    def test_epochs_are_coerced(self):
        """Plain ints passed in become Epoch, so `.iso` is always available downstream."""
        roster = Roster(id='p', last_updated=1000, entries=(RosterEntry(id='a', last_seen=5),))
        self.assertIsInstance(roster.last_updated, Epoch)
        self.assertIsInstance(roster.entries[0].first_seen, Epoch)
        self.assertEqual(Epoch.from_iso(roster.last_updated.iso), 1000)


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

    def test_entries_are_moved_not_rebuilt(self):
        roster = _roster('a', 'b')
        self.assertIs(roster.with_order(['b', 'a']).get('a'), roster.get('a'))

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

    def test_a_source_table_exists_for_every_context_field(self):
        """A field with no sources can never be filled, and would sit unexplained forever."""
        self.assertEqual(set(VideoContext.__annotations__), set(VIDEO_CONTEXT_SOURCES))
        self.assertEqual(set(PlaylistContext.__annotations__), set(PLAYLIST_CONTEXT_SOURCES))

    def test_every_source_table_entry_names_at_least_one_key(self):
        for table in (VIDEO_CONTEXT_SOURCES, PLAYLIST_CONTEXT_SOURCES):
            for target, keys in table.items():
                with self.subTest(target=target):
                    self.assertTrue(keys)

    def test_video_context_is_stored_verbatim(self):
        roster = Roster(id='p').with_flat_extraction(['a'], epoch=1000)
        updated = roster.with_video_context('a', {'title': 'T', 'uploader': 'U'})
        self.assertEqual(dict(updated.get('a').context), {'title': 'T', 'uploader': 'U'})

    def test_storing_context_replaces_rather_than_merges(self):
        """Merging is policy. A setter that quietly merged would be a third place where
        "which value wins" is decided."""
        roster = Roster(id='p').with_flat_extraction(['a'], epoch=1000)
        roster = roster.with_video_context('a', {'title': 'First', 'duration': 10})
        roster = roster.with_video_context('a', {'title': 'Second'})
        self.assertEqual(dict(roster.get('a').context), {'title': 'Second'})

    def test_storing_context_for_an_unknown_id_is_a_no_op(self):
        roster = Roster(id='p').with_flat_extraction(['a'], epoch=1000)
        self.assertEqual(roster.with_video_context('zzz', {'title': 'T'}), roster)

    def test_playlist_context_is_stored_verbatim(self):
        roster = Roster(id='p').with_playlist_context({'title': 'My Playlist'})
        self.assertEqual(dict(roster.context), {'title': 'My Playlist'})

    def test_storing_context_leaves_last_updated_alone(self):
        """last_updated answers "how current is membership", not "how current is the text"."""
        roster = Roster(id='p').with_flat_extraction(['a'], epoch=1000)
        self.assertEqual(roster.with_video_context('a', {'title': 'T'}).last_updated, 1000)


class Timeline(unittest.TestCase):
    def test_entries_at_the_same_epoch_all_survive(self):
        """Two distinct things can happen in one second; neither replaces the other."""
        timeline = (VideoTimeline()
                    .add(MergeTimelineEntry(epoch=Epoch(100),
                                            updates=(FieldUpdate(field='title', value='T'),)))
                    .add(MergeTimelineEntry(epoch=Epoch(100),
                                            updates=(FieldUpdate(field='duration', value='9'),))))
        self.assertEqual(len(timeline), 2)
        self.assertEqual(len(timeline.at_epoch(100)), 2)

    def test_identical_entries_collapse(self):
        entry = MergeTimelineEntry(epoch=Epoch(100),
                                   updates=(FieldUpdate(field='title', value='T'),))
        self.assertEqual(len(VideoTimeline().add(entry).add(entry)), 1)

    def test_entries_are_hashable(self):
        """Dedup needs it, so nothing on an entry may be an unhashable container."""
        entry = MergeTimelineEntry(
            epoch=Epoch(1),
            updates=(FieldUpdate(field='a', value='b'),),
            unavailable_infos=(UnavailableInfo(extractor='youtube', msg='gone'),))
        self.assertEqual(len({entry, entry}), 1)

    def test_level_change_is_two_flat_fields(self):
        entry = MergeTimelineEntry(epoch=Epoch(1), prev_info_level=V_InfoLevel.FLAT,
                                   info_level=V_InfoLevel.EXTRACT)
        self.assertTrue(entry.is_better_info)
        self.assertEqual(entry.render_better_info(), 'FLAT -> EXTRACT')

    def test_no_level_change_renders_nothing(self):
        same = MergeTimelineEntry(epoch=Epoch(1), prev_info_level=V_InfoLevel.EXTRACT,
                                  info_level=V_InfoLevel.EXTRACT)
        self.assertFalse(same.is_better_info)
        self.assertIsNone(same.render_better_info())
        self.assertIsNone(MergeTimelineEntry(epoch=Epoch(1)).render_better_info())

    def test_order_is_chronological_with_level_as_tiebreak(self):
        timeline = VideoTimeline((
            MergeTimelineEntry(epoch=Epoch(300), info_level=V_InfoLevel.FLAT,
                               updates=(FieldUpdate(field='c', value='3'),)),
            MergeTimelineEntry(epoch=Epoch(100), info_level=V_InfoLevel.DOWNLOAD,
                               updates=(FieldUpdate(field='a', value='1'),)),
            MergeTimelineEntry(epoch=Epoch(100), info_level=V_InfoLevel.FLAT,
                               updates=(FieldUpdate(field='b', value='2'),)),
        ))
        self.assertEqual([int(e.epoch) for e in timeline], [100, 100, 300])
        self.assertEqual([e.info_level for e in timeline][:2],
                         [V_InfoLevel.FLAT, V_InfoLevel.DOWNLOAD],
                         'within one epoch, lower level first')

    def test_a_newer_poorer_entry_does_not_jump_ahead_of_an_older_richer_one(self):
        """Ordering by merge priority would put the 2026 flat before the 2024 download, and
        the recorded progression would read backwards."""
        timeline = VideoTimeline((
            MergeTimelineEntry(epoch=Epoch(1_788_000_000), info_level=V_InfoLevel.FLAT,
                               updates=(FieldUpdate(field='x', value='1'),)),
            MergeTimelineEntry(epoch=Epoch(1_704_067_200), info_level=V_InfoLevel.DOWNLOAD,
                               updates=(FieldUpdate(field='y', value='2'),)),
        ))
        self.assertEqual([int(e.epoch) for e in timeline], [1_704_067_200, 1_788_000_000])

    def test_empty_entries_are_identifiable(self):
        self.assertTrue(MergeTimelineEntry(epoch=Epoch(1)).is_empty())
        self.assertFalse(MergeTimelineEntry(
            epoch=Epoch(1), updates=(FieldUpdate(field='a', value='b'),)).is_empty())
        self.assertFalse(MergeTimelineEntry(
            epoch=Epoch(1), prev_info_level=V_InfoLevel.NONE,
            info_level=V_InfoLevel.FLAT).is_empty())

    def test_epoch_is_coerced(self):
        self.assertIsInstance(MergeTimelineEntry(epoch=100).epoch, Epoch)

    def test_levels_reads_out_the_recorded_progression(self):
        timeline = VideoTimeline((
            MergeTimelineEntry(epoch=Epoch(100), info_level=V_InfoLevel.FLAT,
                               updates=(FieldUpdate(field='a', value='1'),)),
            MergeTimelineEntry(epoch=Epoch(200), info_level=V_InfoLevel.DOWNLOAD,
                               updates=(FieldUpdate(field='b', value='2'),)),
            MergeTimelineEntry(epoch=Epoch(300),
                               updates=(FieldUpdate(field='c', value='3'),)),
        ))
        self.assertEqual(timeline.levels(), (V_InfoLevel.FLAT, V_InfoLevel.DOWNLOAD))


# A flat extraction as yt-dlp returns it, trimmed. v1 wrote `info_level` into it.
FLAT_PL_INFO = {
    'id': 'PL_x', '_type': 'playlist', 'title': 'Some Playlist', 'uploader': 'U',
    'playlist_count': 2, 'epoch': 500, 'extractor': 'youtube:tab',
    'info_level': 'FLAT',
    'entries': [
        {'id': 'a', '_type': 'url', 'title': 'A', 'channel': 'C', 'info_level': 'FLAT'},
        {'id': 'b', '_type': 'url', 'title': 'B', 'channel': None},
    ],
}


class Envelope(unittest.TestCase):
    def test_data_stays_byte_faithful(self):
        payload = {'id': 'abc', 'title': 'T', 'channel': 'C', 'epoch': 5, 'extractor': 'youtube'}
        self.assertEqual(VideoEntry.wrap(payload).unwrap(), payload)

    def test_pldl_keys_are_lifted_out_of_the_payload(self):
        payload = {
            'id': 'abc', 'channel': 'C', 'extractor': 'youtube',
            'info_level': 'EXTRACT',
            'unavailable_msgs': [{'epoch': 1, 'msg': 'gone', 'type': 'youtube'}],
            'playlist_epoch': 999,
            'yt_unavailable_msg': 'gone', 'wa_unavailable_msg': None,
        }
        entry = VideoEntry.wrap(payload)

        self.assertIs(entry.info_level, V_InfoLevel.EXTRACT)
        self.assertEqual(entry.playlist_epoch, 999)
        self.assertIsInstance(entry.playlist_epoch, Epoch)
        self.assertEqual(
            entry.unavailable_infos,
            (UnavailableInfo(extractor='youtube', msg='gone', epoch=Epoch(1)),),
        )
        for pldl_key in ('info_level', 'unavailable_msgs', 'playlist_epoch',
                         'yt_unavailable_msg', 'wa_unavailable_msg'):
            self.assertNotIn(pldl_key, entry.unwrap())

    def test_data_is_read_only_at_runtime(self):
        """`frozen` protects the reference; the payload needs protecting too."""
        entry = VideoEntry.wrap({'id': 'a', 'title': 'T'})
        with self.assertRaises(TypeError):
            entry.data['title'] = 'changed'  # type: ignore[index]

    def test_mutating_the_source_dict_does_not_reach_inside(self):
        payload = {'id': 'a', 'title': 'T'}
        entry = VideoEntry.wrap(payload)
        payload['title'] = 'changed'
        self.assertEqual(entry.data['title'], 'T')

    def test_an_int_info_level_survives(self):
        self.assertIs(VideoEntry.wrap({'id': 'a', 'info_level': 0}).info_level, V_InfoLevel.NONE)

    def test_level_is_derived_only_when_nothing_is_declared(self):
        self.assertIs(VideoEntry.wrap({'id': 'a', 'channel': 'c'}).info_level, V_InfoLevel.FLAT)
        self.assertIs(VideoEntry.wrap({'id': 'a'}).info_level, V_InfoLevel.NONE)
        self.assertIs(
            VideoEntry.wrap({'id': 'a'}, info_level=V_InfoLevel.DOWNLOAD).info_level,
            V_InfoLevel.DOWNLOAD, 'an explicit level wins over derivation')

    def test_entry_epoch_reads_the_payload(self):
        self.assertEqual(VideoEntry.wrap({'id': 'a', 'epoch': 77}).epoch, 77)
        self.assertEqual(VideoEntry.wrap({'id': 'a'}).epoch, 0)

    def test_capture_is_a_batch(self):
        capture = Capture(epoch=Epoch(100), videos=(
            VideoEntry.wrap({'id': 'a'}), VideoEntry.wrap({'id': 'b'})))
        self.assertEqual(len(capture), 2)
        self.assertEqual(capture.ids(), ('a', 'b'))
        self.assertIsNotNone(capture.get('a'))
        self.assertIsNone(capture.get('zzz'))
        self.assertEqual(Epoch.from_iso(capture.epoch.iso), 100)
        self.assertIsNone(capture.playlist, 'a per-video batch has no playlist payload')
        self.assertIsNone(capture.pl_id)

    def test_a_flat_extraction_wraps_into_the_same_envelope(self):
        capture = Capture.wrap_flat(FLAT_PL_INFO)
        self.assertEqual(capture.epoch, 500)
        self.assertEqual(capture.pl_id, 'PL_x')
        self.assertEqual(capture.ids(), ('a', 'b'))
        self.assertEqual(capture.playlist['title'], 'Some Playlist')
        self.assertNotIn('entries', capture.playlist)
        self.assertNotIn('info_level', capture.playlist, 'v1 key dropped')
        self.assertIs(capture.get('a').info_level, V_InfoLevel.FLAT)
        self.assertNotIn('info_level', capture.get('a').data, 'lifted onto the entry envelope')

    def test_a_flat_extraction_unwraps_to_what_yt_dlp_returned(self):
        expected = {k: v for k, v in FLAT_PL_INFO.items() if k != 'info_level'}
        expected['entries'] = [{k: v for k, v in e.items() if k != 'info_level'}
                               for e in expected['entries']]
        self.assertEqual(Capture.wrap_flat(FLAT_PL_INFO).unwrap_flat(), expected)

    def test_capture_playlist_is_read_only(self):
        capture = Capture.wrap_flat(FLAT_PL_INFO)
        with self.assertRaises(TypeError):
            capture.playlist['title'] = 'changed'  # type: ignore[index]

    def test_merge_playlist_is_a_folded_capture(self):
        doc = MergePlaylist(id='PL_x', epoch=700, info_level=PL_InfoLevel.MERGE,
                            playlist={'title': 'Some Playlist'},
                            videos=(VideoEntry.wrap({'id': 'a'}),))
        self.assertIsInstance(doc.epoch, Epoch)
        self.assertEqual(doc.ids(), ('a',))
        self.assertEqual(doc.playlist['title'], 'Some Playlist')
        self.assertNotIn('info_level', doc.playlist, 'the level lives on the envelope')
        self.assertEqual(doc.timeline, {})
        with self.assertRaises(TypeError):
            doc.playlist['title'] = 'changed'  # type: ignore[index]


if __name__ == '__main__':
    unittest.main()
