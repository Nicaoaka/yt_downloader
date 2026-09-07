# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A `yt-dlp` wrapper library (`pldl`) that keeps a **durable, historical record of a YouTube playlist**.
Videos get deleted, privated, or reordered; the point of the codebase is that every extraction is
merged into an accumulating snapshot so information is never lost. Downloading files is secondary to
preserving infodicts.

There is no CLI and no packaging — usage is a Python script that builds a `PlaylistDL_Config` and
opens a `PlaylistDL` (see `example.py`). The gitignored scripts in `scripts/` (`general.py`,
`liked_list.py`, `watch_later.py`, `sb.py`, `task_scheduler_bs.py`) are the owner's personal run
configs; treat them as scratch, not API. Each starts with `import _bootstrap`, which puts the repo
root on `sys.path` and makes it the cwd, so `from pldl import *` and relative paths like
`data/Lists 8` resolve no matter where the script is launched from.

## Commands

Python 3.14, venv at `.venv` (Windows layout, `.venv/Scripts/python.exe`). Only runtime dep is `yt-dlp[default]`.

```ps
# all tests (unittest; `manual_*.py` files are NOT collected by design)
.venv/Scripts/python.exe -m unittest discover -s tests -t .

# reproduce the GitHub issue 1 defects against the current tree (offline; exits 1 on drift)
.venv/Scripts/python.exe tests/manual_issue1_repro.py

# one module / class / method
.venv/Scripts/python.exe -m unittest tests.test_merge_ordered_lists
.venv/Scripts/python.exe -m unittest tests.test_utils.Tests.test_merge_objs

# keep yt-dlp current — extraction breaks otherwise
pip install -U "yt-dlp[default]"

# translate a yt-dlp CLI invocation into the API opts dict for config.opts
.venv/Scripts/python.exe cli_to_api.py <yt-dlp cli args>

# print a default config + its generated opts
.venv/Scripts/python.exe -m pldl.config
```

Running `example.py` or the `scripts/` run configs performs **real network extraction/downloads**
with sleeps.
To exercise the pipeline without touching the network, set `_no_yt_dlp_downloads=True` in the config —
any `pre_yt_dlp_download()` then raises `No_YT_DLP_Downloads`.

Sources carry ruff `# noqa` codes, but no ruff config or install lives in the repo.

## Architecture

### The five info types

Everything revolves around one taxonomy, split across `pldl_types.py` (types), `config.py`
(`default_path_tmpls`, one output template per type), and `playlist_dl.py` (production).
All live under `<config.home>/<Playlist>/`:

| Info | Produced by | Written to | Role |
|---|---|---|---|
| `raw_flat` | `extract_flat_info()` | `_flat/` | one flat extraction (ids + order only) |
| `raw_v_infos` | `download_v_infos()` | `_v_infos/` | this session's per-video infodicts |
| `_merge_flat` | maintained continuously | `*.merge.flat.json` | **source of truth for membership + order**; always written on close, never drops a video |
| `pl_info` | `make_pl_info()` | `playlist/` | flat + this session's v_infos, no timeline |
| `merge_info` | `make_merge_info()` | `*.merge.json` | full history merge, carries `merge_timeline` |

`_metadata.json` is the index: `pointers` (relative path + epoch for `latest_flat_info`,
`latest_pl_info`, `latest_merge_info`, `_merge_flat`) plus `history`, a download log keyed by
readable-epoch string. `load()` resolves a pointer; `write_info()` writes and advances the pointer
— but only if the new epoch is `>=` the stored one, so an older info can never clobber a newer pointer.

### Info levels drive merge priority

`V_InfoLevel` (NONE < FLAT < EXTRACT < DOWNLOAD) and `PL_InfoLevel` (NONE < FLAT < MERGE_FLAT <
NORMAL < MERGE) are stored on infodicts as `info_level` and re-derivable from content via
`yt_utils.derive_v_info_level` / `derive_pl_info_level`.

`merge_infos._merge_v_sort_key` sorts by `(info_level, epoch)` with a huge multiplier on the level, so
**a richer old extraction always outranks a poorer new one.** Field-by-field resolution is delegated to
a `MergeFieldUpdater` (`post_processing/merge_updaters.py`: `COMMON_UPDATER` for normal merges,
`FLAT_MERGE_UPDATER` for `_merge_flat`), and `update_filter` decides which changed keys get recorded in
the `merge_timeline`.

### Playlist ordering

`pldl/utils/merge_ordered_lists.py` reconciles disagreeing snapshot orders: each snapshot is a chain of
edges in a DAG built newest-first, edges that would form a cycle are dropped (so newer order wins), then
weakly-connected "islands" get priority from their best member and a reverse Kahn's sort emits the final
order. This is why order survives insertions/deletions across months of snapshots. It's pure and
dependency-free — `tests/test_merge_ordered_lists.py` covers it with `'AB _ BC'`-style string cases.

### PlaylistDL lifecycle

`__setup()` runs in a fixed order and later steps depend on earlier ones:
resolve `ident` → `get_pl_outtmpls()` → merge `create_path_opts()` into `opts` → load/validate metadata
→ load/validate yt-dlp archive → load `_merge_flat` → if the ident produced a fresh flat extract, feed it
through `add_raw_flat_info()` (which also updates `_merge_flat`).

`close()` (via `__exit__`) empties the cookie file, writes `_merge_flat`, and writes `_metadata.json`
**last**. Always use `with PlaylistDL(config) as pldl:` — bailing out otherwise loses the session's state.

`Config_IdentType` picks the entry point: `PL_ID_OR_URL` (required on first run, always extracts),
`METADATA_PATH` (preferred afterwards; reuses the stored `_merge_flat` unless `refresh_after` elapsed),
`PL_INFO_PATH`.

### Download control

Per-video decisions happen in `wrapper_match_filter` **before** yt-dlp is invoked, so it can gate
extraction as well as downloads and can `QUIT` the playlist — yt-dlp's own `match_filter`
(`config.default_yt_dlp_match_filter`) runs after extraction and can only skip downloads. Build one with
`wrapper_match_filter_builder(...)`, which returns a `DL_Action` (USER/QUIT/SKIP/EXTRACT/DOWNLOAD) using
max counts, per-video predicates, id overrides, and backoff computed from `metadata['history']` epochs
plus `yt_utils.interpret_error_msg` (notably HTTP 403 backoff).

Extraction falls back YouTube → `web.archive.org` (`yt_utils.download_video(yt=..., wa=...)`). For a
video found on neither, `download_v_info_generic()` takes an arbitrary yt-dlp URL — the video id must
already be present in `_merge_flat`.

## Conventions and constraints

- `pldl/__init__.py` is built for `from pldl import *`; the `scripts/` run configs rely on that.
- Path templates are **relative to the playlist folder** and use `\`, so `home` can be moved freely.
  `cookiefile`, `outtmpl`, `paths.home`, and `download_archive` are generated from `config.home` /
  `config.path_tmpls`; setting them in `config.opts` raises in `__post_init__`.
- `_validate_metadata_config_sync` raises if `config.path_tmpls` drifts from the templates recorded in an
  existing `_metadata.json`. Changing a template for a playlist that already has data on disk is a
  breaking change and needs the metadata migrated too.
- Epochs: ints internally, `yt_utils.to_readable_epoch` / `from_readable_epoch` for the
  `"%Y-%m-%d %H-%M-%S"` keys used by `history` and `merge_timeline`. `get_epoch` reads an info's own
  epoch; `get_latest_epoch` takes the max across a playlist's entries.
- Console output is ANSI-colored through `utils.hex`; `utils.WARNING` / `utils.ERROR` prefix the caller
  name. Long-running loops deliberately swallow exceptions and `KeyboardInterrupt` to keep the session
  alive and still persist state.
- `data/`, `scripts/`, `secrets/*`, `.venv`, `.claude/` and `test/` are gitignored. `data/Lists N/`
  holds real downloaded playlist data (~1.9 GB; only `Lists 8` is current) — read it for context,
  never rewrite it. `secrets/cookie_file.txt` is intentionally empty except during a run.
