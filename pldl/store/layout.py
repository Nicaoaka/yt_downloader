"""Templates -> resolved paths, plus validation and sanitization. Owns every path decision.

Sanitization runs on **every resolved component**, whether the template was a string or a
callable. Today only the string branch sanitizes, so the default `Playlist` callable lets a
title like "Best: of 2024" reach mkdir and die with WinError 267 (issue-1 #14, confirmed).

Validation is a pure function `validate(paths) -> list[Issue]` over the templates plus a few
dry resolutions against synthetic infodicts, so it is unit-testable with no filesystem.

Hard error -- the template must be **id-discriminating**. This has to work for a callable
(the current default is one), so it is not "does it mention the id" but the property we
actually want:

    resolve(tmpl, {**sample, 'id': 'PL_aaa...'}) != resolve(tmpl, {**sample, 'id': 'PL_bbb...'})

Also always an error: absolute paths, `..`, escaping the playlist dir, Windows reserved
device names (CON, PRN, AUX, NUL, COM1-9, LPT1-9), reserved characters, control characters,
trailing dots/spaces, over-long paths. Warning only: a link_file without %(id)s.
"""
