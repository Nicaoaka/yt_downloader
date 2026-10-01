# CLAUDE.md

Guidance for Claude Code in this folder.

## What this is

v2 of `pldl`, a `yt-dlp` wrapper that keeps a **durable, historical record of a YouTube playlist**:
videos get deleted, privated and reordered, and every extraction is folded into the record so
nothing is lost. Preserving infodicts matters more than downloading files.

v2 is a rewrite. v1 lives on `main`, in its own folder (`../yt_downloader`), with a separate git
history; this branch (`v2`) shares no commits with it. The design and its decisions are in the
master plan: `~/.claude/plans/this-repo-was-initialized-delightful-phoenix.md`.

## Working agreement

- **The owner writes the implementation.** Claude reviews, explains, and writes tests, harnesses
  or demos when asked. No implementation code unless explicitly asked.
- Push `v2` after every commit whose suite is green. Never push `main` unless asked. Never
  force-push or rewrite pushed history. Never commit `secrets/` or `claude-issues/`.

## Commands

```ps
# venv lives in this folder (Python 3.14)
.venv/Scripts/python.exe -m unittest discover -s tests -t .
```

## Layout

Stages, in the order data flows through them:

| Stage | Holds |
|---|---|
| `model/` | generic building blocks: `Epoch`, the schema version |
| `downloader/` | what yt-dlp hands back, wrapped: `VideoEntry`, `Capture`, levels, errors |
| `roster/` | the authoritative record: membership, order, context, timeline |
| `merge/` | folds captures into a `MergePlaylist` and updates the roster |

- **A stage imports only from stages before it.** A type lives with the stage that produces it.
- From outside a stage, import through its `__init__.py`: `from pldl.downloader import VideoEntry`.
  Inside a stage, import siblings by submodule path: `from pldl.merge.updaters import ...`.
- Nothing in these stages imports `yt_dlp` (the import alone costs ~0.4 s).

merge/ answers three questions with three mechanisms; collapsing any two is the mistake that cost
v1 its timeline. Order is `rank(epoch, level)` (chronological, level only breaks a same-second
tie). Which value wins a field is a per-field updater, `(current, incoming) -> winner`. Which
change gets recorded is a per-field timeline filter.

## Tests

A test stays if it names, in one sentence, a bug that would otherwise go unnoticed (wrong data
rather than a crash), and it goes through public functions rather than internals. No tests of
dataclass mechanics, docstrings, or design choices.

## Conventions

- `v1-compat` tags code that exists only to read v1 files; `_v1_` prefixes deprecated types.
- Module docstrings say what a module is, not how it differs from v1.
- Issue numbers appear in tests only.
- `# ---- section ----` comments. US spellings.

## Data

The live playlist data is at `C:\Users\nicol\Videos\yt-dlp`: **read it, never write to it.**
Old fixtures (`data/Lists 1-8`) are in the v1 folder, not this one.
