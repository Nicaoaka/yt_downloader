"""The roster, timeline, manipulations, envelope, metadata and kind registry.

These carry the invariants the record depends on, so the tests are written as statements of
those invariants rather than as coverage of the methods.
"""
import dataclasses
import unittest

from pldl2.model import kinds as kinds_module
from pldl2.model.envelope import Capture, VideoEntry
from pldl2.model.epoch import Epoch
from pldl2.model.errors import UnavailableInfo
from pldl2.model.kinds import (
    KINDS,
    PATH_TEMPLATE_KEYS,
    InfoKind,
    KindName,
    Owner,
    PayloadShape,
    pldl_owned,
    user_owned,
)
from pldl2.model.levels import V_InfoLevel
from pldl2.model.manipulations import Manipulation, ManipulationKind, ManipulationLog
from pldl2.model.metadata import Metadata, Paths, SessionLog, VideoLog
from pldl2.model.roster import Roster, RosterEntry, apply_flat_extraction, update_context
from pldl2.model.timeline import FieldUpdate, MergeTimelineEntry, VideoTimeline


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


class ApplyFlatExtraction(unittest.TestCase):
    """The only writer of in_playlist. These are its invariants."""

    def test_a_video_gone_from_youtube_keeps_its_row(self):
        folded = apply_flat_extraction(_roster('a', 'b', 'c', epoch=1000), ['a', 'c'], epoch=2000)
        self.assertEqual(folded.ids(), ('a', 'b', 'c'), 'b must still be present')
        self.assertFalse(folded.get('b').in_playlist)
        self.assertTrue(folded.get('a').in_playlist)

    def test_a_disappeared_video_keeps_its_last_seen(self):
        folded = apply_flat_extraction(_roster('a', 'b', epoch=1000), ['a'], epoch=2000)
        self.assertEqual(folded.get('b').last_seen, 1000, 'last_seen is when it was last there')
        self.assertEqual(folded.get('a').last_seen, 2000)

    def test_a_video_can_come_back(self):
        roster = apply_flat_extraction(_roster('a', 'b', epoch=1000), ['a'], epoch=2000)
        self.assertFalse(roster.get('b').in_playlist)

        returned = apply_flat_extraction(roster, ['a', 'b'], epoch=3000)
        self.assertTrue(returned.get('b').in_playlist)
        self.assertEqual(returned.get('b').last_seen, 3000)
        self.assertEqual(returned.get('b').first_seen, 1000, 'first_seen never moves')

    def test_new_ids_are_added(self):
        folded = apply_flat_extraction(_roster('a', epoch=1000), ['a', 'new'], epoch=2000)
        self.assertEqual(folded.ids(), ('a', 'new'))
        self.assertEqual(folded.get('new').first_seen, 2000)

    def test_supplied_order_wins(self):
        folded = apply_flat_extraction(_roster('a', 'b', 'c'), ['a', 'b', 'c'], epoch=2000,
                                       order=['c', 'a', 'b'])
        self.assertEqual(folded.ids(), ('c', 'a', 'b'))

    def test_an_order_that_omits_a_known_id_still_keeps_it(self):
        """Order reconciliation must never be able to delete a row."""
        folded = apply_flat_extraction(_roster('a', 'b', 'c'), ['a', 'c'], epoch=2000,
                                       order=['c', 'a'])
        self.assertEqual(set(folded.ids()), {'a', 'b', 'c'})
        self.assertEqual(folded.ids()[:2], ('c', 'a'))

    def test_last_updated_moves_forward_only(self):
        folded = apply_flat_extraction(_roster('a', epoch=5000), ['a'], epoch=1000)
        self.assertEqual(folded.last_updated, 5000)

    def test_folding_an_empty_extraction_marks_everything_gone(self):
        folded = apply_flat_extraction(_roster('a', 'b'), [], epoch=2000)
        self.assertEqual(folded.ids(), ('a', 'b'))
        self.assertEqual(folded.ids(in_playlist=True), ())

    def test_first_seen_is_set_once(self):
        first = apply_flat_extraction(Roster(id='p'), ['a'], epoch=2000)
        self.assertEqual(first.first_seen, 2000)
        later = apply_flat_extraction(first, ['a'], epoch=9000)
        self.assertEqual(later.first_seen, 2000, 'when the playlist was first recorded')
        self.assertEqual(later.last_updated, 9000)


class Context(unittest.TestCase):
    """Best-effort, best-value: a richer source wins, a poorer one only fills gaps."""

    def test_context_comes_from_the_flat_entry(self):
        folded = apply_flat_extraction(Roster(id='p'), ['a'], epoch=2000, infos={
            'a': {'id': 'a', 'title': 'A Video', 'channel': 'Some Channel', 'duration': 42}})
        context = folded.get('a').context
        self.assertEqual(context['title'], 'A Video')
        self.assertEqual(context['uploader'], 'Some Channel')
        self.assertEqual(context['duration'], 42)

    def test_uploader_falls_back_across_the_names_youtube_uses(self):
        for key in ('uploader', 'channel', 'creator'):
            with self.subTest(key=key):
                folded = apply_flat_extraction(Roster(id='p'), ['a'], epoch=1,
                                               infos={'a': {'id': 'a', key: 'X'}})
                self.assertEqual(folded.get('a').context['uploader'], 'X')

    def test_a_richer_source_fills_in_what_flat_cannot_see(self):
        """The case that matters for a dead video: a flat extraction of a removed video knows
        almost nothing, but a mirror's full extraction knows its title and author."""
        roster = apply_flat_extraction(Roster(id='p'), ['a'], epoch=1000,
                                       infos={'a': {'id': 'a'}})
        self.assertNotIn('title', roster.get('a').context)

        roster = update_context(
            roster, 'a',
            {'id': 'a', 'title': 'Recovered', 'uploader': 'Original Author'},
            level=V_InfoLevel.EXTRACT, epoch=1500)
        self.assertEqual(roster.get('a').context['title'], 'Recovered')

    def test_a_later_flat_refresh_does_not_flatten_a_richer_value(self):
        """The whole reason context is rank-guarded rather than latest-wins."""
        roster = update_context(
            apply_flat_extraction(Roster(id='p'), ['a'], epoch=1000),
            'a', {'id': 'a', 'title': 'Recovered'}, level=V_InfoLevel.EXTRACT, epoch=1500)

        refreshed = apply_flat_extraction(roster, ['a'], epoch=9000,
                                          infos={'a': {'id': 'a', 'title': 'Deleted video'}})
        self.assertEqual(refreshed.get('a').context['title'], 'Recovered',
                         'a poorer, newer source must not overwrite a richer one')

    def test_a_poorer_source_still_fills_an_unknown_field(self):
        roster = update_context(
            apply_flat_extraction(Roster(id='p'), ['a'], epoch=1000),
            'a', {'id': 'a', 'title': 'Recovered'}, level=V_InfoLevel.EXTRACT, epoch=1500)

        refreshed = apply_flat_extraction(roster, ['a'], epoch=9000,
                                          infos={'a': {'id': 'a', 'duration': 99}})
        self.assertEqual(refreshed.get('a').context['title'], 'Recovered')
        self.assertEqual(refreshed.get('a').context['duration'], 99, 'gaps still get filled')

    def test_an_equally_ranked_newer_source_does_win(self):
        roster = apply_flat_extraction(Roster(id='p'), ['a'], epoch=1000,
                                       infos={'a': {'id': 'a', 'title': 'Old'}})
        roster = apply_flat_extraction(roster, ['a'], epoch=2000,
                                       infos={'a': {'id': 'a', 'title': 'Renamed'}})
        self.assertEqual(roster.get('a').context['title'], 'Renamed')

    def test_playlist_context(self):
        roster = apply_flat_extraction(
            Roster(id='p'), ['a'], epoch=1000,
            playlist_info={'id': 'p', 'title': 'My Playlist', 'uploader': 'Me'})
        self.assertEqual(roster.context['title'], 'My Playlist')
        self.assertEqual(roster.context['uploader'], 'Me')

    def test_updating_context_leaves_last_updated_alone(self):
        """last_updated answers "how current is membership", not "how current is the text"."""
        roster = apply_flat_extraction(Roster(id='p'), ['a'], epoch=1000)
        updated = update_context(roster, 'a', {'id': 'a', 'title': 'T'},
                                 level=V_InfoLevel.EXTRACT, epoch=5000)
        self.assertEqual(updated.last_updated, 1000)

    def test_updating_an_unknown_id_is_a_no_op(self):
        roster = _roster('a')
        self.assertEqual(update_context(roster, 'zzz', {'title': 'T'},
                                        level=V_InfoLevel.EXTRACT, epoch=1), roster)


class Manipulations(unittest.TestCase):
    """A separate log, because merging and editing answer different questions."""

    def test_records_edits_chronologically(self):
        log = (ManipulationLog()
               .add(Manipulation(epoch=Epoch(300), kind=ManipulationKind.MOVE, v_id='b'))
               .add(Manipulation(epoch=Epoch(100), kind=ManipulationKind.REMOVE, v_id='a')))
        self.assertEqual([int(m.epoch) for m in log], [100, 300])

    def test_identical_entries_collapse(self):
        m = Manipulation(epoch=Epoch(1), kind=ManipulationKind.REMOVE, v_id='a')
        self.assertEqual(len(ManipulationLog().add(m).add(m)), 1)

    def test_survives_the_removal_of_its_video(self):
        """A removed video loses its row, so the log is the only record it was ever here."""
        roster = dataclasses.replace(
            _roster('a', 'b'),
            manipulations=ManipulationLog((
                Manipulation(epoch=Epoch(500), kind=ManipulationKind.REMOVE, v_id='a'),)))
        without_a = roster.with_entries(e for e in roster.entries if e.id != 'a')

        self.assertNotIn('a', without_a)
        self.assertEqual(len(without_a.manipulations.for_video('a')), 1)

    def test_renders_readably(self):
        self.assertEqual(
            Manipulation(epoch=Epoch(1), kind=ManipulationKind.REPLACE,
                         v_id='b', detail='from=b to=c').render(),
            '<REPLACE b from=b to=c>')


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
            unavailable_msgs=(UnavailableInfo(extractor='youtube', msg='gone'),))
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
        }
        entry = VideoEntry.wrap(payload)

        self.assertIs(entry.info_level, V_InfoLevel.EXTRACT)
        self.assertEqual(entry.playlist_epoch, 999)
        self.assertIsInstance(entry.playlist_epoch, Epoch)
        for pldl_key in ('info_level', 'unavailable_msgs', 'playlist_epoch'):
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


class MetadataRecord(unittest.TestCase):
    def _meta(self):
        return Metadata(id='PL_x', paths=Paths(playlist_dir='Some Playlist [PL_x]'))

    def test_history_stays_ordered_however_it_is_added(self):
        meta = (self._meta()
                .record(SessionLog(started=Epoch(300)))
                .record(SessionLog(started=Epoch(100))))
        self.assertEqual([int(s.started) for s in meta.history], [100, 300])
        self.assertEqual(meta.latest().started, 300)

    def test_a_session_spans_a_range(self):
        session = SessionLog(started=Epoch(1000), ended=Epoch(1900))
        self.assertEqual(session.duration, 900)
        self.assertIsNone(SessionLog(started=Epoch(1000)).duration,
                          'an unfinished session has no duration')

    def test_epochs_for_uses_each_videos_own_epoch(self):
        """A session runs for many minutes, so backoff must use when the video was tried."""
        meta = self._meta().with_history([
            SessionLog(started=Epoch(1000), ended=Epoch(1900), videos=(
                VideoLog(id='a', epoch=Epoch(1100)),
                VideoLog(id='b', epoch=Epoch(1800)),
            )),
            SessionLog(started=Epoch(5000), videos=(VideoLog(id='a', epoch=Epoch(5050)),)),
        ])
        self.assertEqual(meta.epochs_for('a'), (1100, 5050))
        self.assertEqual(meta.epochs_for('b'), (1800,))
        self.assertEqual(meta.epochs_for('never'), ())

    def test_errors_is_always_present(self):
        """Empty rather than absent, so readers never need a default."""
        self.assertEqual(VideoLog(id='a', epoch=Epoch(1)).errors, ())

    def test_session_lookup(self):
        session = SessionLog(started=Epoch(1), videos=(VideoLog(id='a', epoch=Epoch(2)),))
        self.assertIsNotNone(session.get('a'))
        self.assertIsNone(session.get('zzz'))

    def test_there_are_no_pointers(self):
        self.assertNotIn('pointers', {f.name for f in dataclasses.fields(Metadata)})

    def test_path_templates_may_use_yt_dlp_expressions(self):
        """Templates are resolved by yt-dlp, so arithmetic and format specs are legal."""
        self.assertIn('%(playlist_index + 1)d', Paths(playlist_dir='x').link_file)


class KindRegistry(unittest.TestCase):
    def test_kinds_are_reachable_as_module_constants(self):
        """A misspelling is then an AttributeError at import, not a KeyError at runtime."""
        self.assertIs(kinds_module.ROSTER, KINDS[KindName.ROSTER])
        with self.assertRaises(AttributeError):
            _ = kinds_module.ARHCIVE  # noqa: B018 - the typo is the point

    def test_every_kind_declares_its_owner_consistently(self):
        for name, kind in KINDS.items():
            with self.subTest(kind=name):
                if kind.owner is Owner.PLDL:
                    self.assertTrue(kind.filename.startswith('_'))
                    self.assertFalse(kind.may_be_missing)
                else:
                    self.assertIn(kind.tmpl_key, PATH_TEMPLATE_KEYS)
                    self.assertTrue(kind.may_be_missing)

    def test_a_tmpl_key_must_name_a_real_template_field(self):
        """Validated against Paths itself, so the two cannot drift apart."""
        with self.assertRaises(ValueError) as ctx:
            InfoKind(name=KindName.RAW_FLAT, owner=Owner.USER,
                     payload=PayloadShape.SINGLE, tmpl_key='raw_flta')
        self.assertIn('raw_flta', str(ctx.exception))

    def test_playlist_dir_is_not_a_template_key(self):
        """It names the folder, not a file inside it."""
        self.assertNotIn('playlist_dir', PATH_TEMPLATE_KEYS)

    def test_the_registry_rejects_an_inconsistent_kind(self):
        with self.assertRaises(ValueError):
            InfoKind(name=KindName.ROSTER, owner=Owner.PLDL, payload=PayloadShape.SINGLE)
        with self.assertRaises(ValueError):
            InfoKind(name=KindName.RAW_FLAT, owner=Owner.USER, payload=PayloadShape.SINGLE)
        with self.assertRaises(ValueError):
            InfoKind(name=KindName.ROSTER, owner=Owner.PLDL,
                     payload=PayloadShape.SINGLE, filename='roster.json')

    def test_kinds_carry_no_config_derived_behavior(self):
        """Templates come from Paths and filters from config; store/ combines them at write
        time. Keeping that off the kind is what lets these be module constants."""
        fields = {f.name for f in dataclasses.fields(InfoKind)}
        self.assertNotIn('reorder', fields)
        self.assertNotIn('filter_of', fields)

    def test_the_two_ownership_groups_partition_the_registry(self):
        self.assertEqual(len(user_owned()) + len(pldl_owned()), len(KINDS))
        self.assertEqual({k.name for k in pldl_owned()},
                         {KindName.ROSTER, KindName.METADATA, KindName.ARCHIVE})

    def test_the_batch_kind_reads_the_newest_epoch(self):
        self.assertEqual(
            kinds_module.RAW_V_INFOS.epoch_of({'videos': [{'epoch': 10}, {'epoch': 30}]}), 30)
        self.assertEqual(kinds_module.RAW_V_INFOS.epoch_of({'videos': []}), 0)


if __name__ == '__main__':
    unittest.main()
