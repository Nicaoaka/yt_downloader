from yt_types import *
from post_processing import merge_pl_infos
import pprint, json, sys

# --- Helpers ---

COMMON = {
    "id": "PL_ID",
    "title": "PL TITLE",
    "availability": "private",
    "channel_follower_count": None,
    "description": "PL Desc",
    "tags": ['pl_tag'],
    "modified_date": "20260625",
    "view_count": None,
    "playlist_count": 4,
    "channel": "PL Channel",
    "channel_id": "PLChannelID",
    "uploader_id": "@PLChannelDisplay",
    "uploader": "PL Channel Username",
    "channel_url": "https://www.youtube.com/channel/PLChannelID",
    "uploader_url": "https://www.youtube.com/@PLChannelDisplay",
    "_type": "playlist",
    "extractor_key": "YoutubeTab",
    "extractor": "youtube:tab",
    "webpage_url": "https://www.youtube.com/playlist?list=PL_ID",
    "original_url": "https://www.youtube.com/watch?v=FIRST_V_ID&list=PL_ID&index=1",
    "webpage_url_basename": "playlist",
    "webpage_url_domain": "youtube.com",
    "release_year": None,
    "epoch": 12345
}
ARBITRARY = "ArBiTrArY"

def v(
        id,
        avail: bool = True,
        ext: bool = True,
        dl: bool = True,
        yt_unavail=None,
        wa_unavail=None,
        epoch: list[int] = [100000],
):
    res = {'id': id, 'epoch': epoch[0]}
    epoch[0] -= 1
    if avail:       res['channel'] = ARBITRARY
    if ext:         res['extractor'] = ARBITRARY
    if dl:          res['requested_downloads'] = ARBITRARY
    if yt_unavail:  res['yt_unavailable_msg'] = yt_unavail
    if wa_unavail:  res['wa_unavailable_msg'] = wa_unavail
    return res

def pl(entries, epoch, **overrides):
    return {**COMMON, 'entries': entries, 'epoch': epoch, **overrides}

def run(name, pl_infos, checks=None):
    print(f'\n{"="*60}')
    print(f'TEST: {name}')
    print('='*60)
    try:
        res = merge_pl_infos(pl_infos)  # type: ignore
        pprint.pprint(res)
        if checks:
            for desc, ok in checks(res):
                status = 'PASS' if ok else 'FAIL'
                print(f'  [{status}] {desc}')
        with open(f'test/merge_pl/test_{name.replace(" ", "_")}.json', 'w') as f:
            json.dump(res, f, indent=4, default=str)
    except Exception as e:
        print(f'  [ERROR] {e}')
        raise


# =============================================================================
# 1. Single playlist — baseline, nothing to merge
# =============================================================================
run('single playlist', [
    pl([v('1'), v('2'), v('3')], epoch=100),
], checks=lambda r: [
    ('3 entries', len(r['entries']) == 3),
    ('order preserved: 1,2,3', [e['id'] for e in r['entries']] == ['1','2','3']),
    ('playlist_count matches', r['playlist_count'] == 3),
])


# =============================================================================
# 2. Two identical playlists — deduplication, no drift
# =============================================================================
run('identical playlists', [
    pl([v('1'), v('2'), v('3')], epoch=200),
    pl([v('1'), v('2'), v('3')], epoch=100),
], checks=lambda r: [
    ('no duplicate entries', len(r['entries']) == 3),
    ('order preserved', [e['id'] for e in r['entries']] == ['1','2','3']),
])


# =============================================================================
# 3. Newer playlist has a video added at the end
# =============================================================================
run('addition at end', [
    pl([v('1'), v('2'), v('3'), v('4')], epoch=200),
    pl([v('1'), v('2'), v('3')],         epoch=100),
], checks=lambda r: [
    ('4 entries', len(r['entries']) == 4),
    ('4 is last', r['entries'][-1]['id'] == '4'),
])


# =============================================================================
# 4. Newer playlist has a video added in the middle
# =============================================================================
run('addition in middle', [
    pl([v('1'), v('2'), v('NEW'), v('3')], epoch=200),
    pl([v('1'), v('2'), v('3')],           epoch=100),
], checks=lambda r: [
    ('4 entries', len(r['entries']) == 4),
    ('NEW before 3', r['entries'].index(next(e for e in r['entries'] if e['id']=='NEW'))
                   < r['entries'].index(next(e for e in r['entries'] if e['id']=='3'))),
])


# =============================================================================
# 5. Video removed in newer playlist — should still appear (from older)
# =============================================================================
run('removal in newer', [
    pl([v('1'), v('3')],         epoch=200),
    pl([v('1'), v('2'), v('3')], epoch=100),
], checks=lambda r: [
    ('all 3 videos present', {e['id'] for e in r['entries']} == {'1','2','3'}),
    ('playlist_count == 3', r['playlist_count'] == 3),
    # 2 is an "orphan" from old list — should appear between 1 and 3 or at end
    ('1 before 3', r['entries'].index(next(e for e in r['entries'] if e['id']=='1'))
                 < r['entries'].index(next(e for e in r['entries'] if e['id']=='3'))),
])


# =============================================================================
# 6. Video info level upgrade: unavailable → available
# =============================================================================
E6 = [200000]
run('info level upgrade unavail to avail', [
    pl([v('1', epoch=E6)],                    epoch=200),  # fully available
    pl([v('1', avail=False, yt_unavail='yt-gone', epoch=E6)], epoch=100),  # unavailable
], checks=lambda r: [
    ('entry has requested_downloads', 'requested_downloads' in r['entries'][0]),
    ('unavailable_msgs recorded', 'unavailable_msgs' in r['entries'][0]),
    ('wa msg not present', r['entries'][0].get('yt_unavailable_msg') is None
                        or 'unavailable_msgs' in r['entries'][0]),
])


# =============================================================================
# 7. Video info level downgrade: available in old, unavailable in new
#    The higher info level (downloaded) should win regardless of epoch
# =============================================================================
E7 = [200000]
run('info level: downloaded beats newer unavailable', [
    pl([v('1', avail=False, yt_unavail='now-gone', epoch=E7)], epoch=200),  # newer but unavail
    pl([v('1', epoch=E7)],                                      epoch=100),  # older but downloaded
], checks=lambda r: [
    ('requested_downloads present (higher info level wins)', 'requested_downloads' in r['entries'][0]),
    ('unavailable_msgs recorded', 'unavailable_msgs' in r['entries'][0]),
])


# =============================================================================
# 8. Both wa and yt unavailable messages across versions
# =============================================================================
E8 = [200000]
run('both unavail msg types', [
    pl([v('1', False, False, False, wa_unavail='wa-200', epoch=E8)], epoch=200),
    pl([v('1', False, False, False, yt_unavail='yt-100', epoch=E8)], epoch=100),
], checks=lambda r: [
    ('unavailable_msgs has 2 entries', len(r['entries'][0].get('unavailable_msgs', [])) == 2),
    ('wa msg present', any(m['msg'] == 'wa-200' for m in r['entries'][0].get('unavailable_msgs', []))),
    ('yt msg present', any(m['msg'] == 'yt-100' for m in r['entries'][0].get('unavailable_msgs', []))),
])


# =============================================================================
# 9. Ordering conflict: two playlists disagree on relative order of two videos
#    Newer playlist's order should win
# =============================================================================
run('ordering conflict newer wins', [
    pl([v('A'), v('B'), v('C')], epoch=200),  # newer: A B C
    pl([v('B'), v('A'), v('C')], epoch=100),  # older: B A C
], checks=lambda r: [
    ('A before B (newer playlist order)', 
     [e['id'] for e in r['entries']].index('A') < [e['id'] for e in r['entries']].index('B')),
])


# =============================================================================
# 10. Multiple playlists, progressive additions over time
# =============================================================================
run('progressive additions', [
    pl([v('1'), v('2'), v('3'), v('4'), v('5')], epoch=500),
    pl([v('1'), v('2'), v('3'), v('4')],         epoch=400),
    pl([v('1'), v('2'), v('3')],                 epoch=300),
    pl([v('1'), v('2')],                         epoch=200),
    pl([v('1')],                                 epoch=100),
], checks=lambda r: [
    ('5 entries', len(r['entries']) == 5),
    ('order is 1-5', [e['id'] for e in r['entries']] == ['1','2','3','4','5']),
])


# =============================================================================
# 11. Single video playlist
# =============================================================================
run('single video', [
    pl([v('ONLY')], epoch=100),
], checks=lambda r: [
    ('1 entry', len(r['entries']) == 1),
    ('correct id', r['entries'][0]['id'] == 'ONLY'),
    ('playlist_count == 1', r['playlist_count'] == 1),
])


# =============================================================================
# 12. Error cases
# =============================================================================
print(f'\n{"="*60}')
print('TEST: error — empty list')
print('='*60)
try:
    merge_pl_infos([])
    print('  [FAIL] should have raised')
except ValueError as e:
    print(f'  [PASS] raised ValueError: {e}')

print(f'\n{"="*60}')
print('TEST: error — mismatched playlist ids')
print('='*60)
try:
    merge_pl_infos([  # type: ignore
        {**COMMON, 'id': 'PL_A', 'entries': [], 'epoch': 100},
        {**COMMON, 'id': 'PL_B', 'entries': [], 'epoch': 200},
    ])
    print('  [FAIL] should have raised')
except ValueError as e:
    print(f'  [PASS] raised ValueError: {e}')