import traceback

from yt_types import *
from yt_types import PL_DownloadInfo


def pl_v_ids(pl_info: PL_InfoDict) -> None:
    """ Prints video ids from pl_info in a formatted way

    <#ids> IDs:
     1. 123456789012
     2. 123456789012
    ...
    10. 123456789012
    ...

    Args:
        pl_info (_PL_InfoDict): Every entry should have something set for `id`
    """
    video_ids = [entry['id'] for entry in pl_info.get('entries', [])]
    _max_index_len = len(str(len(video_ids)))
    print(f"{len(video_ids)} IDs:")
    for i, id in enumerate(video_ids, 1):
        print(f"{str(i).rjust(_max_index_len)}. {id}")

KEY_ORDER = [
    'no_info',
    'extract', 
    'download',
    'skip',
    'fail',
    'error',
]
assert set(KEY_ORDER) == PL_DownloadInfo.__required_keys__
def download_results(results: PL_DownloadInfo):
    
    print("\n\n" + " + " * 10)
    
    for k in KEY_ORDER:
        print(k)
        for x in results[k]:
            if k == 'error':
                v_id, excs = x
                print(f'\t{v_id}')
                for e in excs:
                    print(f"\t{e!r}")
                    print(''.join(f'\t\t{line}' for line in traceback.format_exception(e)))
            else:
                print(f'\t{x}')

    print(' - ' * 20 + "\n\n")