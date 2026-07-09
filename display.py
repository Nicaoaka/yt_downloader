import traceback

from yt_types import *
from yt_types import PL_DownloadInfo
import utils



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


USER         = utils.hex("   USER INPUT   ", bg='#696969')
QUIT         = utils.hex("   QUIT   ", bg="#ff5c5c")
SKIP         = utils.hex("   SKIP   ", bg="#363636")
EXTRACT      = utils.hex("   EXTRACT   ", bg="#97ffff")
DOWNLOAD     = utils.hex("   DOWNLOAD   ", bg="#8c00ff")

# Results
_EXTRACT     = utils.hex("  EXTR  ", bg="#97ffff")
_DOWNLOAD    = utils.hex("  DWLD  ", bg="#8c00ff")
CANCEL       = utils.hex(" CANCEL ", bg="#363636")
FAIL         = utils.hex("  FAIL  ", bg="#ff5c5c")
UNRECOGNIZED = utils.hex("  ????  ", bg="#ffffff")
NO_INFO      = utils.hex(" NOINFO ", bg="#FFEE52")
OK           = utils.hex("   OK   ", bg='#4bc84b')
NO_DOWNLOAD  = utils.hex(" NODWLD ", bg="#ff8738")
IMPOSSIBLE_STATE = utils.hex("  IMPOSSIBLE STATE  ", bg="#0000ac")

DL_ACTION_STR_MAP = {
    DL_Action.USER     : USER,
    DL_Action.QUIT     : QUIT,
    DL_Action.SKIP     : SKIP,
    DL_Action.EXTRACT  : EXTRACT,
    DL_Action.DOWNLOAD : DOWNLOAD,
}

DL_RESULT_STR_MAP = {
    DL_Result.CANCELLED    : CANCEL,
    DL_Result.FAIL         : FAIL,
    DL_Result.UNRECOGNIZED : UNRECOGNIZED,
    DL_Result.NO_INFO      : NO_INFO,
    DL_Result.EXTRACT      : _EXTRACT,
    DL_Result.DOWNLOAD     : _DOWNLOAD,
}


def exc(e: BaseException):
    return utils.hex(''.join(traceback.format_exception(e)).rstrip(), fg='#db6a6a')

def download_result(dl: DownloadInfo) -> str:
    if dl['action'] == DL_Action.USER:
        return IMPOSSIBLE_STATE + " DL_Action.User is an invalid action for a DL_Result."
    
    if dl['action'] in (DL_Action.QUIT, DL_Action.SKIP):
        if dl['result'] == DL_Result.CANCELLED:
            return CANCEL + " Action was skipped."
        else:
            return IMPOSSIBLE_STATE + f" SKIP or QUIT should have DL_Result.CANCELLED. Got {dl['result']}"

    if dl['action'] == DL_Action.EXTRACT:
        if dl['result'] == DL_Result.EXTRACT:
            return OK
        if dl['result'] == DL_Result.DOWNLOAD:
            utils.WARNING("Download detected in extract!")
            return OK
        return DL_RESULT_STR_MAP[dl['result']]
    
    if dl['action'] == DL_Action.DOWNLOAD:
        if dl['result'] in (DL_Result.DOWNLOAD):
            return OK
        if dl['result'] in (DL_Result.EXTRACT, DL_Result.NO_INFO):
            return NO_DOWNLOAD + " No download detected."
        return DL_RESULT_STR_MAP[dl['result']]

    return IMPOSSIBLE_STATE + f" Unknown DL_Action: {dl['action']}"

def _download_info(dl: DownloadInfo, errors: bool) -> str:
    res = f'{DL_ACTION_STR_MAP[dl['action']]} -> {download_result(dl)} {dl['id']:100}'
    if errors:
        for e in dl['errors']:
            res += '\n'+exc(e)
    return res

def download_info(dl_info: DownloadInfo, errors: bool):
    print(_download_info(dl_info, errors))

def pl_download_info(pl_dl_info: PL_DownloadInfo, errors: bool):
    for dl_info in pl_dl_info:
        print(_download_info(dl_info, errors))

def _test_dl_info():
    errors = []
    try:
        raise ValueError("Hello")
    except Exception as e:
        errors = [e]
    for a in DL_Action:
        for r in DL_Result:
            download_info({
                'id': 'id',
                'action': a,
                'result': r,
                'errors': errors,
            }, False)

def main():
    _test_dl_info()
    pass

if __name__ == "__main__":
    main()
