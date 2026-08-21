import random

from pldl import *
from pldl.config import default_update_filter


def rand(chance: float) -> bool:
    return random.random() < chance

PL: PL_InfoDict = {'id': "1", 'entries': []}
V: V_InfoDict = {'id': '00000-00001'}

UNAVAILABLE_MSGS: dict[str, UnavailableMsg] = {
    'yt-dlp misc': { # not sure what went wrong
        'type': 'yt', 'epoch': 0,
        'msg': "\u001b[0;31mERROR:\u001b[0m Postprocessing: Conversion failed!",
    },
    'timedout': { # (throttling)
        'type': 'yt', 'epoch': 0,
        'msg': "\u001b[0;31mERROR:\u001b[0m \r[download] Got error: HTTPSConnectionPool(host='rr1---sn-a5mekndl.googlevideo.com', port=443): Read timed out. (read timeout=20.0)"
    },
    'forbidden': { # (also throttling?)
        'type': 'yt', 'epoch': 0,
        'msg': "\u001b[0;31mERROR:\u001b[0m unable to download video data: HTTP Error 403: Forbidden"
    },
    'yt--terminated_acc': {
        'type': 'yt', 'epoch': 0,
        'msg': "\u001b[0;31mERROR:\u001b[0m [youtube] C5uMV-iK3Ps: Video unavailable. This video is no longer available because the YouTube account associated with this video has been terminated.",
    },
    'yt--removed_vid': {
        'type': 'yt', 'epoch': 0,
        'msg': "\u001b[0;31mERROR:\u001b[0m [youtube] 1yipP37b58c: This video has been removed for violating YouTube's Terms of Service",
    },
    'yt--unavailable': {
        'type': 'yt', 'epoch': 0,
        'msg': "\u001b[0;31mERROR:\u001b[0m [youtube] dvyG8KWrB_E: Video unavailable. This video is not available",
    },
    'yt--unavailable-short': {
        'type': 'yt', 'epoch': 0,
        'msg': "\u001b[0;31mERROR:\u001b[0m [youtube] PSrU6IQ9-Gs: Video unavailable",
    },
    'yt--private': {
        'type': 'yt', 'epoch': 0,
        'msg': "\u001b[0;31mERROR:\u001b[0m [youtube] qMuLtIC4w64: Private video. Sign in if you've been granted access to this video. Use --cookies-from-browser or --cookies for the authentication. See  https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp  for how to manually pass cookies. Also see  https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies  for tips on effectively exporting YouTube cookies"
    },
    'yt--takedown': {
        'type': 'yt', 'epoch': 0,
        'msg': "\u001b[0;31mERROR:\u001b[0m [youtube] rGDim_zxiqQ: Video unavailable. It was removed following a copyright removal request by Sony Music Entertainment (Japan) Inc."
    },
    'wa--not_indexed': {
        'type': 'wa', 'epoch': 0,
        'msg': "\u001b[0;31mERROR:\u001b[0m [web.archive:youtube] x5PZVROWgYM: The requested video is not archived or indexed"
    },
}
global_epoch = utils.epoch_now()

def reset():
    global global_epoch
    global_epoch = utils.epoch_now()

def v(
        id: str,
        info_level: yt_utils.V_InfoLevel = V_InfoLevel.FLAT,
        unavailable_msgs: list[UnavailableMsg]|None=None,
        epoch: int|None = None,
        info: pldl_types._V_InfoDict_NoReqs = {},  # noqa: B006
) -> V_InfoDict:

    if epoch is None:
        global global_epoch
        epoch = global_epoch
        global_epoch += 1

    res: V_InfoDict = {'id': f'{id}', 'info_level': info_level.name, 'epoch': epoch, **info}
    if unavailable_msgs:
        um = unavailable_msgs.copy()
        for m in um:
            m['epoch'] = epoch
        res['unavailable_msgs'] = um
    return res

def pl(
        id: str,
        entries: list[V_InfoDict],
        info_level: PL_InfoLevel = PL_InfoLevel.FLAT,
        epoch: int|None = None,
        info: pldl_types._PL_InfoDict_NoReqs = {},  # noqa: B006
) -> PL_InfoDict:

    if epoch is None:
        global global_epoch
        epoch = global_epoch
        global_epoch += 1
    
    res: PL_InfoDict = {'id': id, 'entries': entries, 'info_level': info_level.name, 'epoch': epoch, **info}
    return res


def test_merging_mfs():
    new_ids = list(range(1, 6))
    normal_ids = list(range(6, 11))

    old = pl(
        id='test',
        entries=[
            v(f'{i}', V_InfoLevel.FLAT)
            for i in normal_ids
        ],
        info_level=PL_InfoLevel.FLAT,
    )

    new = pl(
        id='test',
        entries=[
            v(f'{i}', V_InfoLevel.DOWNLOAD)
            for i in new_ids+normal_ids
        ],
        info_level=PL_InfoLevel.NORMAL,
    )

    _merge_pl_infos = lambda pl_infos, init: post_processing.merge_pl_infos(pl_infos, post_processing.merge_updaters.COMMON_UPDATER, default_update_filter, _init_merge_info=init)


    old_mf = _merge_pl_infos([old], None)
    new_mf = _merge_pl_infos([new, old_mf], None)

    utils.json_dump(old_mf, 'old-mf.json', 'rm old', indent=4)
    utils.json_dump(new_mf, 'new-mf.json', 'rm old', indent=4)

def test_merge_unavailable_msgs():

    old = pl(
        id='test',
        entries=[v('video', unavailable_msgs=[UNAVAILABLE_MSGS['forbidden']])])

    # multiple unavailable_msgs at different times
    new1 = pl(
        id='test',
        entries=[v('video', unavailable_msgs=[UNAVAILABLE_MSGS['yt--takedown']])])
    
    # same unavailable_msg at same time
    new1a = pl(
        id='test',
        entries=[v('video', unavailable_msgs=[UNAVAILABLE_MSGS['yt--takedown']], epoch=yt_utils.get_epoch(new1))])
    
    # same unavailable_msg at different time
    new2 = pl(
        id='test',
        entries=[v('video', unavailable_msgs=[UNAVAILABLE_MSGS['yt--takedown']])])

    utils.json_dump(
        post_processing.merge_pl_infos(
            [new1, new1a, new2],
            post_processing.merge_updaters.COMMON_UPDATER,
            default_update_filter,
            _init_merge_info=old),
        'merged-unavailable.json', 'rm old', indent=4)

def test_from_real():

    # res = post_processing.merge_v_infos(
    #     utils.json_load(r"merge-test/v_infos.json"),
    #     post_processing.merge_updaters.COMMON_UPDATER,
    #     default_update_filter,
    # )
    # utils.json_dump(res, 'merge-test/v-output.json', 'rm old', indent=4)

    res = post_processing.merge_pl_infos(
        utils.json_load(r"merge-test/pl_infos.json"),
        post_processing.merge_updaters.COMMON_UPDATER,
        default_update_filter,
        utils.json_load(r"merge-test/init-no-merge.json")
    )

    display.pl_merge_timeline(res, [entry['id'] for entry in res['entries']])
    utils.json_dump(res, 'merge-test/output.json', 'rm old', indent=4)

# test_merge_unavailable_msgs()
test_from_real()
