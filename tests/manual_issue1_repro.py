"""
Reproduction harness for the defects reported in GitHub issue 1.

Issue 1 is a read-only audit written at 5c7982e with **no human confirmation** and no live
yt-dlp run anywhere. Before the rewrite designs around any of it, each finding has to be
shown to still reproduce against the tree as it stands. This script is that gate.

It is deliberately a `manual_*` module: `unittest discover` does not collect it, because its
checks assert *current, buggy* behaviour. It is not a spec of what pldl should do -- it is a
record of what pldl does today, so the rewrite can prove it changed.

    .venv/Scripts/python.exe tests/manual_issue1_repro.py          # verdicts only
    .venv/Scripts/python.exe tests/manual_issue1_repro.py -v       # + the evidence
    .venv/Scripts/python.exe tests/manual_issue1_repro.py --keep   # keep the scratch dir

Exit code is 0 when every check matches BASELINE, 1 when any check drifted. A drift is not
automatically bad -- fixing a defect is a drift -- but it must be looked at and the baseline
updated deliberately.

Everything is written under a temp directory and no network call is made. The only
monkeypatches are PlaylistDL._download_v_infos, utils.input_string, yt_utils.extract_flat_info
and YoutubeDL.extract_info.

Adapted from the `repro_bugs.py` scratch script published in the issue.
"""
# This harness reaches the defects by doing what the type contracts forbid: it patches
# methods, builds half-initialized PlaylistDL objects and passes plain dicts where
# TypedDicts are declared. That is the point, so the checker is quieted file-wide.
# pyright: reportArgumentType=false, reportAttributeAccessIssue=false
# pyright: reportCallIssue=false, reportIndexIssue=false, reportOptionalMemberAccess=false
# pyright: reportTypedDictNotRequiredAccess=false
import contextlib
import inspect
import io
import json
import os
import shutil
import sys
import tempfile
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pldl import *
from pldl import display, yt_utils
from pldl.config import default_path_tmpls
from pldl.playlist_dl import (
    PlaylistDL,
    _Infos,
    _InfosEntry,
    default_field_updater,
    default_update_filter,
    default_wrapper_match_filter,
    init_metadata,
    wrapper_match_filter_builder,
)
from pldl.pldl_types import *
from pldl.utils import utils

VERBOSE = '-v' in sys.argv or '--verbose' in sys.argv
KEEP = '--keep' in sys.argv

SCRATCH = tempfile.mkdtemp(prefix='pldl_issue1_')
HOME = os.path.join(SCRATCH, 'home')
os.makedirs(HOME, exist_ok=True)


# ---------------------------------------------------------------------------
# Observations recorded at 7c9ee67 (fix/issue-1), python 3.14, yt-dlp 2026.08.19, windows 11.
#
# `issue` is the defect's heading in issue 1. `status` is the verdict at that commit:
# CONFIRMED = still reproduces, FIXED = no longer reproduces.
# ---------------------------------------------------------------------------
BASELINE = {
    'R1': dict(issue='#9  remove_videos skips the first entry', status='CONFIRMED',
               obs={'plural_result': ['a', 'b'], 'singular_result': ['b', 'c'], 'warned': True}),
    'R2': dict(issue='#10 insert_videos breaks on negative positions', status='CONFIRMED',
               obs={'pos_neg1': 'ValueError', 'pos_neg2': ['x', 'y', 'a', 'z', 'b'],
                    'singular_neg1': ['x', 'y', 'z', 'a']}),
    'R3': dict(issue='#11 manipulation timeline entries overwrite each other', status='CONFIRMED',
               obs={'entry_keys': ['update'], 'entries_after_two_updates': 1,
                    'replace_chain_kept': '<REPLACE ID from=b to=c>'}),
    'R4': dict(issue='#7  delete_prev never deletes the previous file', status='FIXED',
               obs={'prev_file_still_exists': False, 'merge_flat_files_on_disk': 1}),
    'R5': dict(issue='#1  download_v_infos wrong opts (cookies half)', status='CONFIRMED',
               obs={'default_call': False, 'cookiefile_kwarg': False, 'with_opts_arg': True}),
    'R6': dict(issue='#4  the archive sync fix can never converge', status='CONFIRMED',
               obs={'prompts': 3, 'recognized_ids': [], 'archive_lines': 3,
                    'every_line_unreadable': True}),
    'R8': dict(issue='minor: safely_resolve_path never calls part_sanitizer', status='CONFIRMED',
               obs={'sanitizer_applied': False}),
    'R9': dict(issue='minor: _print_per_id with ident_colors=[] prints one row', status='CONFIRMED',
               obs={'rows_for_3_ids': 1}),
    'R10': dict(issue='#23 download_video_generic stores the V_InfoLevel enum', status='CONFIRMED',
                obs={'is_enum_not_str': True, 'json_roundtrips_to': 0}),
    'R11': dict(issue='#12 PL_INFO_PATH with a fresh pl_info never builds _merge_flat',
                status='CONFIRMED',
                obs={'merge_flat_is_none': True, 'make_merge_info': 'AttributeError',
                     'remove_video': 'TypeError', 'close_wrote_metadata': True}),
    'R12': dict(issue='#13 the config demands a cookie file that close() empties',
                status='CONFIRMED',
                obs={'empty_rejected': True, 'size_after_empty_cookies': 0,
                     'next_run_rejected': True}),
    'R13': dict(issue="minor: config.opts['paths']['temp'] dropped by the shallow merge",
                status='CONFIRMED', obs={'temp_survives': False, 'merged_paths_keys': ['home']}),
    'R14': dict(issue='minor: _add_to_merge_timeline nests under "merge_timeline"',
                status='CONFIRMED', obs={'double_nested': True}),
    'R16': dict(issue='#14 playlist titles with filesystem characters crash the first write',
                status='CONFIRMED', obs={'dir_contains_colon': True, 'makedirs_raised': True}),
    'R17': dict(issue='#3  the 403 backoff is checked once per process', status='CONFIRMED',
                obs={'fresh_filter': 'quit', 'default_1st_call': 'download',
                     'default_2nd_call': 'download'}),
    'R18': dict(issue='#8  make_pl_info/make_merge_info crash after a same-session removal',
                status='CONFIRMED', obs={'make_pl_info': 'KeyError', 'make_merge_info': 'KeyError'}),
    'R19': dict(issue='#17 readable epoch keys collide across the DST fall-back hour',
                status='CONFIRMED', obs={'collision_found': True, 'second_epoch_lost': True}),
    'R20': dict(issue='#1  download_v_infos wrong opts (self.opts half)', status='CONFIRMED',
                obs={'opts_handed_to_ytdlp': ['cookiefile', 'format'],
                     'self_opts_keys_dropped': ['download_archive', 'outtmpl', 'paths']}),
    'R21': dict(issue='#18 an unrecognized [youtube] error counts as a confirmed failure',
                status='CONFIRMED', obs={'interpreted': ['youtube', False], 'action': 'skip'}),
    'R22': dict(issue='#5  the default filter quits the pass after one failed video',
                status='CONFIRMED',
                obs={'max_fails': 1, 'quit_when_maxed': True, 'action_0_fails': 'download',
                     'action_1_fail': 'quit'}),
    'R23': dict(issue='#6  every merge restamps older timeline entries', status='CONFIRMED',
                obs={'run1_levels': ['FLAT', 'EXTRACT'], 'run2_levels': ['EXTRACT', 'EXTRACT'],
                     'restamped': True}),
    'R24': dict(issue='#33 make_pl_info prints a Mismatching PL_InfoLevel warning',
                status='CONFIRMED', obs={'warned': True, 'resulting_level': 'NORMAL'}),
    'R25': dict(issue='#15 likely-unavailable videos no longer bypass the maxes',
                status='CONFIRMED', obs={'action': 'skip'}),
    'R26': dict(issue='#23 a raw v_infos file carrying "info_level": 0 cannot be re-added',
                status='CONFIRMED', obs={'roundtrip_value': 0, 'add_raw_v_infos': 'AttributeError'}),
    'R28': dict(issue='#2  a renamed playlist forks history and archive into a new folder',
                status='CONFIRMED',
                obs={'new_folder': 'New Title [LL]', 'history_rows_seen': 0,
                     'archive_ids_seen': [], 'metadata_files': 2}),
}

RESULTS: dict[str, dict] = {}


def quiet():
    return contextlib.redirect_stdout(io.StringIO())


class Check:
    """Collects observations for one R-number; the diff against BASELINE happens in report()."""

    def __init__(self, rid):
        self.rid = rid
        self.obs = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.obs['__harness_error__'] = ''.join(
                traceback.format_exception(exc_type, exc, tb))[-500:]
        RESULTS[self.rid] = self.obs
        return True  # one broken check must not end the run

    def __call__(self, key, value):
        self.obs[key] = value
        return value


def action_name(a):
    return a.name.lower() if hasattr(a, 'name') else str(a)


def make_cookie(path, content='# Netscape HTTP Cookie File\n.youtube.com\tTRUE\t/\tTRUE\t0\tX\tY\n'):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def fake_pldl(entry_ids, home=HOME, config=None):
    """Build a PlaylistDL without running __init__ (no network, no prompts)."""
    if config is None:
        config = PlaylistDL_Config(ident='LL', ident_type=Config_IdentType.PL_ID_OR_URL, home=home)
    p = object.__new__(PlaylistDL)
    p.session_start_epoch = utils.epoch_now()
    p._config = config
    p.id = 'LL'
    pl_info = {
        'id': 'LL', 'title': 'T', 'epoch': 1_700_000_000, 'info_level': 'MERGE_FLAT',
        'merge_timeline': {},
        'entries': [{'id': i, 'title': f'title {i}', 'epoch': 1_700_000_000, 'info_level': 'NONE'}
                    for i in entry_ids],
    }
    yt_utils.fixup_pl_info(pl_info)
    p._pl_outtmpls = PlaylistDL.get_pl_outtmpls(home, config.path_tmpls, pl_info)
    p.opts = {}
    p._metadata = init_metadata('LL', {k: os.path.relpath(v, home)
                                       for k, v in p._pl_outtmpls.items()})
    p._yt_dlp_archive = []
    p._infos = _Infos()
    p._infos.raw_v_infos = _InfosEntry([], p._pl_outtmpls['raw_video_infojson'],
                                       is_written=False, metadata_key=None)
    p._infos._merge_flat = _InfosEntry(pl_info, p._pl_outtmpls['_merged_flat_infojson'],
                                       is_written=False, metadata_key='_merge_flat')
    return p


def ids(p):
    return PlaylistDL.get_v_ids(p._infos._merge_flat)


V = {'id': 'aaaaaaaaaaa', 'title': 't', 'view_count': 10}
EMPTY_IDS = {'fail': [], 'extract': [], 'download': [], 'error': []}
ERR_403 = "\x1b[0;31mERROR:\x1b[0m unable to download video data: HTTP Error 403: Forbidden"
ERR_BOT = ("\x1b[0;31mERROR:\x1b[0m [youtube] aaaaaaaaaaa: Sign in to confirm you're not a bot. "
           "Use --cookies-from-browser or --cookies for the authentication.")
ERR_WA = ("\x1b[0;31mERROR:\x1b[0m [web.archive:youtube] aaaaaaaaaaa: "
          "The requested video is not archived or indexed")


# ===========================================================================
# edit/ -- pure list manipulation (issue 1: #9, #10, #11)
# ===========================================================================

with Check('R1') as c:
    p = fake_pldl(['a', 'b', 'c'])
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        p.remove_videos(['a', 'c'])
    c('plural_result', ids(p))
    c('warned', 'is not in the playlist' in buf.getvalue())
    p = fake_pldl(['a', 'b', 'c'])
    with quiet():
        p.remove_video('a')
    c('singular_result', ids(p))

with Check('R2') as c:
    p = fake_pldl(['x', 'y', 'z'])
    try:
        with quiet():
            p.insert_videos(['a', 'b'], position=-1)
        c('pos_neg1', ids(p))
    except ValueError:
        c('pos_neg1', 'ValueError')
    p = fake_pldl(['x', 'y', 'z'])
    with quiet():
        p.insert_videos(['a', 'b'], position=-2)
    c('pos_neg2', ids(p))
    p = fake_pldl(['x', 'y', 'z'])
    with quiet():
        p.insert_video('a', -1)
    c('singular_neg1', ids(p))

with Check('R3') as c:
    info = {'id': 'LL', 'entries': []}
    PlaylistDL._add_update_to_merge_timeline(info, 'v', '<REMOVE v>', raw_epoch=1_700_000_000)
    PlaylistDL._add_update_to_merge_timeline(info, 'v', '<INSERT to=1>', raw_epoch=1_700_000_000)
    entries = info['merge_timeline']['v']
    c('entries_after_two_updates', len(entries))
    c('entry_keys', sorted(next(iter(entries.values())).keys()))
    p = fake_pldl(['a', 'x'])
    with quiet():
        p.replace_videos([('a', 'b'), ('b', 'c')])
    tl_b = p._infos._merge_flat.data['merge_timeline'].get('b') or {}
    kept = [v for e in tl_b.values() for v in e.values()]
    c('replace_chain_kept', kept[0] if len(kept) == 1 else kept)


# ===========================================================================
# store/ -- persistence and pointers (issue 1: #7, #12, #13)
# ===========================================================================

with Check('R4') as c:
    home4 = os.path.join(SCRATCH, 'r4')
    os.makedirs(home4, exist_ok=True)
    cfg4 = PlaylistDL_Config(ident='LL', ident_type=Config_IdentType.PL_ID_OR_URL, home=home4)
    p = fake_pldl(['a'], home=home4, config=cfg4)
    entry = p._infos._merge_flat
    with quiet():
        ptr1 = p.write_info(entry, 'rm old', delete_prev=True)
        entry.data['epoch'] += 3600
        ptr2 = p.write_info(entry, 'rm old', delete_prev=True)
    folder = os.path.dirname(os.path.join(home4, ptr2[0]))
    c('merge_flat_files_on_disk',
      len([f for f in os.listdir(folder) if f.endswith('.merge.flat.json')]))
    c('prev_file_still_exists', os.path.exists(os.path.join(home4, ptr1[0])))

with Check('R11') as c:
    home11 = os.path.join(SCRATCH, 'r11')
    os.makedirs(home11, exist_ok=True)
    pl_path = os.path.join(home11, 'pl.json')
    now = utils.epoch_now()
    with open(pl_path, 'w', encoding='utf-8') as f:
        json.dump({'id': 'LL', 'title': 'T', 'epoch': now, 'info_level': 'FLAT',
                   'entries': [{'id': 'aaaaaaaaaaa', 'title': 'x', 'epoch': now}]}, f)
    cfg11 = PlaylistDL_Config(ident=pl_path, ident_type=Config_IdentType.PL_INFO_PATH,
                              home=home11, _no_yt_dlp_downloads=True)
    with quiet():
        p11 = PlaylistDL(cfg11)
    c('merge_flat_is_none', p11._infos._merge_flat is None)
    for name, fn in (('make_merge_info', lambda: p11.make_merge_info(write=False)),
                     ('remove_video', lambda: p11.remove_video('aaaaaaaaaaa'))):
        try:
            with quiet():
                fn()
            c(name, 'ok')
        except Exception as e:  # noqa: BLE001 - the exception type IS the observation
            c(name, type(e).__name__)
    with quiet():
        p11.close()
    c('close_wrote_metadata', os.path.exists(p11._pl_outtmpls['metadata']))

with Check('R12') as c:
    empty = os.path.join(SCRATCH, 'empty_cookies.txt')
    open(empty, 'w').close()
    try:
        PlaylistDL_Config(ident='LL', ident_type=Config_IdentType.PL_ID_OR_URL,
                          home=HOME, cookie_file=empty)
        c('empty_rejected', False)
    except RuntimeError:
        c('empty_rejected', True)
    cookie2 = make_cookie(os.path.join(SCRATCH, 'cookies2.txt'))
    cfg12 = PlaylistDL_Config(ident='LL', ident_type=Config_IdentType.PL_ID_OR_URL,
                              home=HOME, cookie_file=cookie2)
    p = fake_pldl(['a'], config=cfg12)
    with quiet():
        p.empty_cookies()
    c('size_after_empty_cookies', os.path.getsize(cookie2))
    try:
        PlaylistDL_Config(ident='LL', ident_type=Config_IdentType.PL_ID_OR_URL,
                          home=HOME, cookie_file=cookie2)
        c('next_run_rejected', False)
    except RuntimeError:
        c('next_run_rejected', True)

with Check('R13') as c:
    cfg13 = PlaylistDL_Config(ident='LL', ident_type=Config_IdentType.PL_ID_OR_URL,
                              home=HOME, opts={'paths': {'temp': 'tmp'}})
    outt = PlaylistDL.get_pl_outtmpls(HOME, cfg13.path_tmpls,
                                      {'id': 'LL', 'title': 'T', 'entries': []})
    merged = cfg13.opts | PlaylistDL.create_path_opts(HOME, outt)
    c('merged_paths_keys', sorted(merged['paths'].keys()))
    c('temp_survives', 'temp' in merged['paths'])

with Check('R16') as c:
    outt = PlaylistDL.get_pl_outtmpls(HOME, default_path_tmpls(),
                                      {'id': 'LL', 'title': 'Best: of 2024', 'entries': []})
    c('dir_contains_colon', ':' in os.path.basename(outt['Playlist']))
    try:
        os.makedirs(outt['Playlist'], exist_ok=True)
        c('makedirs_raised', False)
    except OSError:
        c('makedirs_raised', True)


# ===========================================================================
# library/ -- the yt-dlp download archive (issue 1: #4)
# ===========================================================================

with Check('R6') as c:
    dir6 = os.path.join(SCRATCH, 'r6')
    os.makedirs(dir6, exist_ok=True)
    arch = os.path.join(dir6, '_yt_dlp_archive.txt')
    meta = init_metadata('LL', {}, history={'2026-01-01__00-00-00': [
        {'id': 'aaaaaaaaaaa', 'title': None, 'action': 'download', 'result': 'download'}]})
    prompts = []
    orig_input_string = utils.input_string

    def fake_input_string(*a, **k):
        prompts.append(a[1] if len(a) > 1 else '')
        return 'y'

    utils.input_string = fake_input_string
    try:
        for _ in range(3):
            archive = PlaylistDL._load_yt_archive(arch)
            with quiet():
                PlaylistDL._validate_dl_archive_sync(archive, meta, arch)
    finally:
        utils.input_string = orig_input_string
    c('prompts', len(prompts))
    c('recognized_ids', yt_utils.ids_from_yt_dlp_archive(PlaylistDL._load_yt_archive(arch)))
    with open(arch, encoding='utf-8') as fh:
        lines = [ln for ln in fh.read().splitlines() if ln.strip()]
    c('archive_lines', len(lines))
    c('every_line_unreadable', all(ln.startswith('pldl_sync_fix ') for ln in lines))


# ===========================================================================
# ytdlp/ -- opts assembly and error classification (issue 1: #1, #18, #23)
# ===========================================================================

captured = {}
orig_dl = PlaylistDL.__dict__['_download_v_infos']


def fake_download_v_infos(pl_info, wrapper_match_filter, **kw):
    captured['opts'] = kw['opts']
    return [], []


cookie = make_cookie(os.path.join(SCRATCH, 'cookies.txt'))
cfg5 = PlaylistDL_Config(ident='LL', ident_type=Config_IdentType.PL_ID_OR_URL, home=HOME,
                         cookie_file=cookie, cookies_for_vids=True)

with Check('R5') as c:
    p = fake_pldl(['aaaaaaaaaaa'], config=cfg5)
    PlaylistDL._download_v_infos = staticmethod(fake_download_v_infos)
    try:
        with quiet():
            p.download_v_infos()
        c('default_call', 'cookiefile' in captured['opts'])
        with quiet():
            p.download_v_infos(cookiefile=cookie)
        c('cookiefile_kwarg', 'cookiefile' in captured['opts'])
        with quiet():
            p.download_v_infos(opts={})
        c('with_opts_arg', 'cookiefile' in captured['opts'])
    finally:
        PlaylistDL._download_v_infos = orig_dl

with Check('R20') as c:
    p = fake_pldl(['aaaaaaaaaaa'], config=cfg5)
    p.opts = {'paths': {'home': HOME}, 'outtmpl': {'default': 'x'}, 'download_archive': 'a.txt'}
    PlaylistDL._download_v_infos = staticmethod(fake_download_v_infos)
    try:
        with quiet():
            p.download_v_infos(opts={'format': 'best'})
        handed = sorted(captured['opts'].keys())
        c('opts_handed_to_ytdlp', handed)
        c('self_opts_keys_dropped', sorted(k for k in p.opts if k not in handed))
    finally:
        PlaylistDL._download_v_infos = orig_dl

with Check('R10') as c:
    # The issue used a file:// URL, but yt-dlp now rejects those with a RequestError, which
    # takes the `except Exception` branch and returns None -- the enum is never reached.
    # Forcing a DownloadError hits the branch the defect is actually about.
    from yt_dlp import YoutubeDL
    from yt_dlp.utils import DownloadError
    orig_extract_info = YoutubeDL.extract_info

    def boom(self, url, *a, **k):
        raise DownloadError('[youtube] aaaaaaaaaaa: Video unavailable')

    YoutubeDL.extract_info = boom
    try:
        with quiet(), contextlib.redirect_stderr(io.StringIO()):
            g_info, g_err, g_ok = yt_utils.download_video_generic(
                'https://example.invalid/watch?v=aaaaaaaaaaa',
                {'quiet': True, 'no_warnings': True}, download=False)
    finally:
        YoutubeDL.extract_info = orig_extract_info
    lvl = (g_info or {}).get('info_level')
    c('is_enum_not_str', isinstance(lvl, V_InfoLevel))
    c('json_roundtrips_to', json.loads(json.dumps({'l': lvl}))['l'])

with Check('R26') as c:
    reloaded = json.loads(json.dumps(
        {'id': 'aaaaaaaaaaa', 'info_level': V_InfoLevel.NONE, 'epoch': 1, 'unavailable_msgs': []}))
    c('roundtrip_value', reloaded['info_level'])
    p = fake_pldl(['aaaaaaaaaaa'])
    try:
        with quiet():
            p.add_raw_v_infos([reloaded], write=False)
        c('add_raw_v_infos', 'ok')
    except Exception as e:  # noqa: BLE001 - the exception type IS the observation
        c('add_raw_v_infos', type(e).__name__)

with Check('R19') as c:
    found = None
    for e in range(1793400000, 1793600000, 1800):
        if yt_utils.to_readable_epoch(e) == yt_utils.to_readable_epoch(e + 3600):
            found = e
            break
    c('collision_found', found is not None)
    if found is None:
        c('second_epoch_lost', f'no DST fall-back in local tz {time.tzname}')
    else:
        key = yt_utils.to_readable_epoch(found)
        c('second_epoch_lost', yt_utils.from_readable_epoch(key) != found + 3600)


# ===========================================================================
# policy/ -- download decisions (issue 1: #3, #5, #15, #18)
# ===========================================================================

with Check('R17') as c:
    history_403 = {yt_utils.to_readable_epoch(utils.epoch_now() - 60): [
        {'id': 'bbbbbbbbbbb', 'title': None, 'action': 'download', 'result': 'fail',
         'errors': [ERR_403]}]}
    with quiet():
        fresh = wrapper_match_filter_builder()
        c('fresh_filter', action_name(fresh(V, [], history_403, EMPTY_IDS, [], [])))
        c('default_1st_call',
          action_name(default_wrapper_match_filter(V, [], {}, EMPTY_IDS, [], [])))
        c('default_2nd_call',
          action_name(default_wrapper_match_filter(V, [], history_403, EMPTY_IDS, [], [])))

with Check('R22') as c:
    sig = inspect.signature(wrapper_match_filter_builder)
    c('max_fails', sig.parameters['max_fails'].default)
    c('quit_when_maxed', sig.parameters['quit_when_maxed'].default)
    one_fail = [{'id': 'bbbbbbbbbbb', 'title': None, 'action': 'download', 'result': 'fail',
                 'errors': ["\x1b[0;31mERROR:\x1b[0m [youtube] bbbbbbbbbbb: Video unavailable",
                            ERR_WA]}]
    with quiet():
        f = wrapper_match_filter_builder()
        c('action_0_fails', action_name(f(V, [], {}, EMPTY_IDS, [], [])))
        c('action_1_fail', action_name(f(V, one_fail, {}, EMPTY_IDS, [], [])))

with Check('R21') as c:
    with quiet():
        res = yt_utils.interpret_error_msg(ERR_BOT)
    c('interpreted', list(res))
    history_bot = {yt_utils.to_readable_epoch(utils.epoch_now() - 60): [
        {'id': 'aaaaaaaaaaa', 'title': None, 'action': 'download', 'result': 'fail',
         'errors': [ERR_BOT, ERR_WA]}]}
    with quiet():
        f = wrapper_match_filter_builder(ignore_ambiguous_dl_errors=True)
        c('action', action_name(f(V, [], history_bot, EMPTY_IDS, [], [])))

with Check('R25') as c:
    unavail = {'id': 'ccccccccccc', 'title': 't', 'view_count': None}
    with quiet():
        f = wrapper_match_filter_builder(max_downloads=0, yt_unavailable_action=DL_Action.DOWNLOAD)
        c('action', action_name(f(unavail, [], {}, EMPTY_IDS, [], [])))


# ===========================================================================
# merge/ -- the fold and its timeline (issue 1: #6, #8, #33)
# ===========================================================================

RAW_EXTRACT = {'id': 'aaaaaaaaaaa', 'title': 'title aaaaaaaaaaa', 'channel': 'c',
               'epoch': 1_700_000_100, 'extractor': 'youtube', 'extractor_key': 'Youtube',
               'info_level': 'EXTRACT', 'description': 'd'}

with Check('R18') as c:
    p = fake_pldl(['aaaaaaaaaaa', 'bbbbbbbbbbb'])
    raw = dict(RAW_EXTRACT, epoch=utils.epoch_now())
    with quiet():
        p.add_raw_v_infos([raw], write=False)
        p.remove_video('aaaaaaaaaaa')
    for name, fn in (('make_pl_info', lambda: p.make_pl_info(write=False)),
                     ('make_merge_info', lambda: p.make_merge_info(write=False))):
        try:
            with quiet():
                fn()
            c(name, 'ok')
        except Exception as e:  # noqa: BLE001 - the exception type IS the observation
            c(name, type(e).__name__)

with Check('R23') as c:
    p = fake_pldl(['aaaaaaaaaaa'])
    with quiet():
        p.add_raw_v_infos([dict(RAW_EXTRACT)], write=False)
        run1 = p.make_merge_info(write=False).data
    tl1 = run1['merge_timeline']['aaaaaaaaaaa']
    c('run1_levels', [e.get('info_level') for e in tl1.values()])
    with quiet():
        run2 = PlaylistDL._make_merge_info(run1, [p._infos._merge_flat.data], [],
                                           default_field_updater, default_update_filter)
    tl2 = run2['merge_timeline']['aaaaaaaaaaa']
    c('run2_levels', [e.get('info_level') for e in tl2.values()])
    c('restamped', [e.get('info_level') for e in tl1.values()]
                   != [e.get('info_level') for e in tl2.values()])

with Check('R24') as c:
    p = fake_pldl(['aaaaaaaaaaa'])
    with quiet():
        p.add_raw_v_infos([dict(RAW_EXTRACT)], write=False)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        entry24 = p.make_pl_info(write=False)
    c('warned', 'Mismatching PL_InfoLevel' in buf.getvalue())
    c('resulting_level', entry24.data.get('info_level'))


# ===========================================================================
# report/ and utils/ -- latent findings
# ===========================================================================

with Check('R8') as c:
    r = utils.safely_resolve_path(r'dir\bad:name?x', {}, part_sanitizer=lambda s: 'SANITIZED')
    c('sanitizer_applied', 'SANITIZED' in str(r))

with Check('R9') as c:
    pl_info = {'id': 'LL', 'entries': [{'id': 'a'}, {'id': 'b'}, {'id': 'c'}]}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        display._print_per_id(pl_info, ['a', 'b', 'c'], ['1', '2', '3'],
                              ident_colors=[], include_urls=False)
    c('rows_for_3_ids', len([ln for ln in buf.getvalue().splitlines() if ln.strip()]))

with Check('R14') as c:
    info = {'id': 'LL', 'entries': []}
    PlaylistDL._add_to_merge_timeline(
        info, {'v': {'2026-01-01__00-00-00': {'updates': {'title': 'x'}}}})
    c('double_nested', 'merge_timeline' in info['merge_timeline'])


# ===========================================================================
# store/ -- playlist identity (issue 1: #2). Last: it stubs extract_flat_info.
# ===========================================================================

with Check('R28') as c:
    home28 = os.path.join(SCRATCH, 'r28')
    os.makedirs(home28, exist_ok=True)
    month_ago = utils.epoch_now() - 30 * 86400
    old_pl = {'id': 'LL', 'title': 'Old Title', 'epoch': month_ago, 'info_level': 'MERGE_FLAT',
              'merge_timeline': {},
              'entries': [{'id': 'aaaaaaaaaaa', 'title': 'x', 'epoch': month_ago,
                           'info_level': 'NONE'}]}
    yt_utils.fixup_pl_info(old_pl)
    cfg28 = PlaylistDL_Config(ident='LL', ident_type=Config_IdentType.PL_ID_OR_URL, home=home28)
    p = object.__new__(PlaylistDL)
    p.session_start_epoch = utils.epoch_now()
    p._config = cfg28
    p.id = 'LL'
    p._pl_outtmpls = PlaylistDL.get_pl_outtmpls(home28, cfg28.path_tmpls, old_pl)
    p.opts = {}
    p._metadata = init_metadata('LL', {k: os.path.relpath(v, home28)
                                       for k, v in p._pl_outtmpls.items()})
    p._yt_dlp_archive = []
    p._infos = _Infos()
    p._infos.raw_v_infos = _InfosEntry([], p._pl_outtmpls['raw_video_infojson'],
                                       is_written=False, metadata_key=None)
    p._infos._merge_flat = _InfosEntry(old_pl, p._pl_outtmpls['_merged_flat_infojson'],
                                       is_written=False, metadata_key='_merge_flat')
    with quiet():
        p.write_info(p._infos._merge_flat, 'rm old')
        p._metadata['history'] = {yt_utils.to_readable_epoch(month_ago): [
            {'id': 'aaaaaaaaaaa', 'title': 'x', 'action': 'download', 'result': 'download'}]}
        with open(p._pl_outtmpls['yt_dlp_archive'], 'w', encoding='utf-8') as fh:
            fh.write('youtube aaaaaaaaaaa\n')
        p.write_metadata_file()
    old_meta_path = p._pl_outtmpls['metadata']

    orig_extract = yt_utils.extract_flat_info

    def stub_extract_flat_info(pl_url_or_id, opts=None):
        now = utils.epoch_now()
        return {'id': 'LL', 'title': 'New Title', 'epoch': now, 'info_level': 'FLAT',
                'entries': [{'id': 'aaaaaaaaaaa', 'title': 'x', 'channel': 'c', 'epoch': now,
                             'playlist_epoch': now, 'info_level': 'FLAT'}]}

    yt_utils.extract_flat_info = stub_extract_flat_info
    try:
        cfg28b = PlaylistDL_Config(ident=old_meta_path, ident_type=Config_IdentType.METADATA_PATH,
                                   home=home28)
        with quiet():
            q = PlaylistDL(cfg28b)
    finally:
        yt_utils.extract_flat_info = orig_extract
    c('new_folder', os.path.relpath(q._pl_outtmpls['Playlist'], home28))
    c('history_rows_seen', sum(len(rows) for rows in q._metadata['history'].values()))
    c('archive_ids_seen', yt_utils.ids_from_yt_dlp_archive(q._yt_dlp_archive))
    with quiet():
        q.close()
    c('metadata_files', sum(1 for _, _, fs in os.walk(home28) for f in fs if f == '_metadata.json'))


# ===========================================================================
# Report
# ===========================================================================

def report():
    width = 78
    drifted, missing = [], []
    print('=' * width)
    print('issue 1 reproduction  --  pldl @ ' + os.popen('git rev-parse --short HEAD').read().strip())
    print('=' * width)
    for rid, base in BASELINE.items():
        obs = RESULTS.get(rid)
        if obs is None:
            missing.append(rid)
            print(f'  {rid:<5} !! DID NOT RUN            {base["issue"]}')
            continue
        err = obs.pop('__harness_error__', None)
        diffs = [(k, base['obs'].get(k, '<absent>'), v)
                 for k, v in obs.items() if base['obs'].get(k, '<absent>') != v]
        for k in base['obs']:
            if k not in obs:
                diffs.append((k, base['obs'][k], '<not observed>'))
        if err:
            drifted.append(rid)
            print(f'  {rid:<5} !! HARNESS ERROR          {base["issue"]}')
            print('        ' + err.replace('\n', '\n        ').rstrip())
        elif diffs:
            drifted.append(rid)
            print(f'  {rid:<5} ~~ DRIFTED from {base["status"]:<9} {base["issue"]}')
            for k, want, got in diffs:
                print(f'        {k}: baseline={want!r}  now={got!r}')
        else:
            mark = 'ok' if base['status'] == 'CONFIRMED' else '--'
            print(f'  {mark} {rid:<5}  {base["status"]:<9} {base["issue"]}')
        if VERBOSE and not err:
            for k, v in obs.items():
                print(f'          {k} = {v!r}')
    confirmed = sum(1 for r, b in BASELINE.items()
                    if b['status'] == 'CONFIRMED' and r not in drifted and r not in missing)
    fixed = sum(1 for r, b in BASELINE.items()
                if b['status'] == 'FIXED' and r not in drifted and r not in missing)
    print('-' * width)
    print(f'  {confirmed} still reproduce, {fixed} fixed, {len(drifted)} drifted, '
          f'{len(missing)} did not run  ({len(BASELINE)} checks)')
    if drifted or missing:
        print('  -> a drift is not automatically bad. Look at each one, then update BASELINE.')
    print('=' * width)
    return 1 if (drifted or missing) else 0


code = report()
if KEEP:
    print(f'scratch kept at: {SCRATCH}')
else:
    shutil.rmtree(SCRATCH, ignore_errors=True)
sys.exit(code)
