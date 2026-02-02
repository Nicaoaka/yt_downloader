from typing import NotRequired, Required, Literal, Any

from yt_downloader import *
from yt_downloader import _InfoDict, _PL_InfoDict

def make_entry(title, id, epoch, ) -> _InfoDict:
    return {}

pl_infos = [
{
    "id": "playlist",
    "entries": [
        {"title": "_", "id": "0", "channel": None},
        {"title": "c", "id": "3", "channel": "available"},
        {"title": "d", "id": "4", "channel": None}, # unavailable
    ],
    "epoch": 150
},
{
    "id": "playlist",
    "entries": [
        {"title": "a", "id": "1", "channel": None},
        {"title": "b", "id": "2", "channel": None},
        {"title": "c", "id": "3", "channel": "available"},
        {"title": "d", "id": "4", "channel": "available"},
    ],
    "epoch": 100
},
{
    "id": "playlist",
    "entries": [
        {"title": "_", "id": "0", "channel": "available"},
        {"title": "between", "id": "69", "channel": "available"},
        {"title": "a", "id": "1", "channel": "available"},
    ],
    "epoch": 50
},
]

res = union_pl_info(pl_infos, verbose=True) # type: ignore
print(res)

import json

with open('test.json', 'w') as f:
    json.dump(res, f, indent=4, default=str)