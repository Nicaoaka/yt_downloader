from yt_types import *

DL_MAP = {
    str(action).lower(): action
    for action in DL_Action
    if action not in (DL_Action.USER)
}
print(DL_MAP)