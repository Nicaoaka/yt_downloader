import shutil
import pprint
import os

from pldl import *

TEST_HOME = 'Lists-Sim'
TEST_INFO_PATH = os.path.join(TEST_HOME, '__fake_list__.json')
BASE_INFO_DIR = os.path.join(TEST_HOME, 'base')

# cleanup
if os.path.exists(TEST_HOME):
    shutil.rmtree(TEST_HOME)

pl_info: PL_InfoDict[V_InfoDict] = yt_utils.min_pl_info('__test_id__', yt_utils.PL_InfoLevel.NONE)
pl_info['entries'] = [
    yt_utils.min_v_info(str(i), yt_utils.V_InfoLevel.NONE)
    for i in range(1, 6)]

utils.json_dump(pl_info, TEST_INFO_PATH, 'rm old')

_config = PlaylistDL_Config(
    ident=TEST_INFO_PATH,
    ident_type=Config_IdentType.PL_INFO_PATH,
    base_info_type='any',
    home=TEST_HOME,
    refresh_after = float('inf'),
    
    _use_as_merge_flat = True,
)

def write_base(info, name):
    utils.json_dump(info, os.path.join(TEST_HOME, f'{name}.json'), 'mov new', indent=4)

with PlaylistDL(_config) as pl_dl:
    write_base(pl_dl._infos.base_info.data, 'b')
    write_base(pl_dl._infos._merge_flat.data, 'mf')

    # pl_dl.remove_video('4')
    # pl_dl.remove_videos('234566734', True)
    pl_dl.insert_videos('680', 100)
    pl_dl.insert_videos('6', 100, True)
    # pl_dl.replace_videos([('5', '7'), ('2', '6'), ('1', '2')])
    # pl_dl.replace_videos([('5', '7'), ('2', '5')], True)
    # pl_dl.move_video('1', 4)
    # pl_dl.move_video('1', 4, True)

    write_base(pl_dl._infos.base_info.data, 'b')
    write_base(pl_dl._infos._merge_flat.data, 'mf')
