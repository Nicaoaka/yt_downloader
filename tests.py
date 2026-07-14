from yt_types import *
from merge_infos import merge_pl_infos, merge_v_infos
import pprint
import json
import sys
import display
import utils
import random
import pp_utils


def rand(chance: float) -> bool:
    return random.random() < chance

PL = {
    "id": "PL_ID",
    "title": "PL TITLE",
    # "availability": "private",
    # "channel_follower_count": None,
    # "description": "PL Desc",
    # "tags": ['pl_tag'],
    # "modified_date": "20260625",
    # "view_count": None,
    # "playlist_count": 4,
    "channel": "PL Channel",
    # "channel_id": "PLChannelID",
    "uploader_id": "@PLChannelDisplay",
    "uploader": "PL Channel Username",
    # "channel_url": "https://www.youtube.com/channel/PLChannelID",
    # "uploader_url": "https://www.youtube.com/@PLChannelDisplay",
    # "_type": "playlist",
    # "extractor_key": "YoutubeTab",
    # "extractor": "youtube:tab",
    # "webpage_url": "https://www.youtube.com/playlist?list=PL_ID",
    # "original_url": "https://www.youtube.com/watch?v=FIRST_V_ID&list=PL_ID&index=1",
    # "webpage_url_basename": "playlist",
    # "webpage_url_domain": "youtube.com",
    # "release_year": None,
    "epoch": 12345
}

FLAT_UNAVAIL = {
    # "_type": "url",
    # "ie_key": "Youtube",
    "id": "v_id",
    # "url": "https://www.youtube.com/watch?v=v_id",
    # "title": "v title",
    # "description": None,
    # "duration": None,
    # "channel_id": None,
    "channel": None,
    # "channel_url": None,
    # "uploader": None,
    # "uploader_id": None,
    # "uploader_url": None,
    # "thumbnails": [
    # {
    #     "url": "https://i.ytimg.com/img/no_thumbnail.jpg",
    #     "height": 90,
    #     "width": 120
    # },
    # {
    #     "url": "https://i.ytimg.com/img/no_thumbnail.jpg",
    #     "height": 180,
    #     "width": 320
    # },
    # {
    #     "url": "https://i.ytimg.com/img/no_thumbnail.jpg",
    #     "height": 360,
    #     "width": 480
    # }
    # ],
    # "timestamp": None,
    # "release_timestamp": None,
    # "availability": None,
    # "view_count": None,
    # "live_status": None,
    # "channel_is_verified": None,
    # "__x_forwarded_for_ip": None,

    # "playlist_id": "PL_ID",
    # "playlist": "PL TITLE",
    # "playlist_count": 1,
    # "n_entries": 2,
    # "playlist_index": 3,
    # "playlist_autonumber": 4,
    # "playlist_title": "PL TITLE",
    # "playlist_channel": "PLChannel",
    # "playlist_channel_id": "PLChannelID",
    # "playlist_uploader": "PL Channel Username",
    # "playlist_uploader_id": "@PLChannelDisplay",
    # "playlist_webpage_url": "https://www.youtube.com/playlist?list=PL_ID"
}

ARBITRARY = "ArBiTrArY"
global_epoch = 0
def reset():
    global global_epoch
    global_epoch = utils.epoch_now()

class DEFAULT: ...
def v(
        id,
        avail_yt: bool = True,
        ext:   bool = True,
        dl:    bool = False,
        yt: bool=False,
        wa: bool=False,
        epoch:int|None|type[DEFAULT]=DEFAULT,
        **overrides,
) -> V_InfoDict:
    global global_epoch
    global_epoch += 1
    res = {**FLAT_UNAVAIL, 'id': f'{id} (v_id)'}
    if epoch is not None:
        res['epoch'] = global_epoch if epoch is DEFAULT else epoch
    if avail_yt:    res['channel'] = 'AVAIL_YT'
    if ext:         res['extractor'] = 'EXTRACT'
    if dl:          res['requested_downloads'] = 'DOWNLOADED'
    if yt:  res['yt_unavailable_msg'] = f'{res['epoch']} YouTube'
    if wa:  res['wa_unavailable_msg'] = f'{res['epoch']} WebArchive'
    return res | overrides # type: ignore

def pl(entries, epoch:int|None|type[DEFAULT]=DEFAULT, **overrides) -> PL_InfoDict:
    global global_epoch
    global_epoch += 1
    res = {**PL, **overrides, 'entries': entries}
    if epoch is not None:
        res['epoch'] = global_epoch if epoch is DEFAULT else epoch
    return res # type: ignore

import os
TEST_HOME = 'test/merge_pl'
os.makedirs(TEST_HOME, exist_ok=True)
def record(data, name):
    with open(f'{TEST_HOME}/{name.replace(" ", "_")}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, default=str, ensure_ascii=False)



def test_basic_v():
    res = merge_v_infos([
        v(1),
    ])
    record(res, 'basic v')

def test_v_better_past():
    res = merge_v_infos([
        v(1, avail_yt=True,  ext=True,  dl=True),
        v(1, avail_yt=True,  ext=True,  dl=False),
        v(1, avail_yt=True,  ext=False, dl=False),
        v(1, avail_yt=False, ext=False, dl=False),
    ])
    record(res, 'better past')

def test_v_unavail():
    res = merge_v_infos([
        v(1, yt=True),
        v(1, wa=True),
        v(1),
        v(1, wa=True),
        v(1, yt=True),
        v(1, yt=True, wa=True),
    ])
    record(res, 'unavailable video')

def test_on_new():
    res = merge_pl_infos([
        pl([v(1)]),
        pl([v(2)]),
        pl([v(3)]),
    ])
    record(res, 'on new')

def test_steps():
    res = merge_pl_infos([
        pl([v(1)]),
        pl([v(2), v(1)]),
        pl([v(3), v(2), v(1)]),
    ])
    record(res, 'steps')

def test_unavailable():
    res = merge_pl_infos([
        pl([v(1, dl=True)]),
        pl([v(1, yt=True)]),
        pl([v(1, yt=True)]),
        pl([v(1, yt=True, wa=True)]),
    ])

    record(res, 'unavailable')

def test_iterations():
    res = merge_pl_infos([
        pl([v(1, yt=True, wa=True)]),
        pl([v(1, yt=True)]),
    ])
    res = merge_pl_infos([
        res,
        pl([v(1, dl=True)]),
    ])
    record(res, 'iterations')

def test_no_change_iterations():
    pls = [
        pl([v(x) for x in range(5)])
        for _ in range(20)
    ]
    res = pls[0]
    for _pl in pls[1:]:
        res = merge_pl_infos([res, _pl])

    res = merge_pl_infos([res, pl([v(x) for x in range(6)])])
    
    record(res, 'no_change_iterations')

def test_stale():
    res = merge_pl_infos([
        pl([v(1, is_stale=1000)]),
        pl([v(1, is_stale=1000)]),
    ])
    res = merge_pl_infos([
        res,
        pl([v(1, is_stale=False)]),
    ])
    record(res, 'stale')

def test_large_list():
    pls = [
        pl([v(x, rand(0.5), rand(0.5), rand(0.5), rand(0.5), rand(0.5)) for x in range(20)])
        for _ in range(5)
    ]
    res = pls[0]
    for _pl in pls[1:]:
        res = merge_pl_infos([res, _pl])

    res = merge_pl_infos([res, pl([v(x) for x in range(6)])])
    
    record(res, 'large list')

def test_jyes():
    res = {}
    d = 'test/jyes [...A-E9x23WGD3]/playlist'
    for _p in os.listdir(d):
        p = os.path.join(d, _p)
        if not res:
            res = utils.json_load(p)
            continue
        res = merge_pl_infos([res, utils.json_load(p)])
    pp_utils.filter_pl_info(res, set(), {'formats', 'requested_formats', 'automatic_captions'})
    record(res, 'jyes')

def main():
    tests = [
        test_basic_v,
        test_v_better_past,
        test_v_unavail,
        test_on_new,
        test_steps,
        test_unavailable,
        test_iterations,
        test_no_change_iterations,
        test_stale,
        test_large_list,
        test_jyes,
    ]
    
    for t in tests:
        try:
            reset()
            t()
        except Exception as e:
            print(display.exc(e))
            print()

if __name__ == "__main__":
    main()
