import json
from yt_dlp import YoutubeDL
import pldl.yt_utils as yt_wrapper

path = r''
with open(path, 'r', encoding='utf-8') as f:
    x = json.load(f)
with open('cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(YoutubeDL.sanitize_info(x, True), f)
with open('cleaned-wrapper.json', 'w', encoding='utf-8') as f:
    json.dump(yt_wrapper.copy_and_sanitize_info(x, True), f)
