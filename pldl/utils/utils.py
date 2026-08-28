__all__ = [  # noqa: RUF022
    'FalsySentinel',

    'hex',
    'EXC_COLOR', 'format_exception',
    'WARN_COLOR', 'WARNING',
    'ERR_COLOR', 'ERROR',
    'truncate', 'numbered_list', 'clear',
    'color_bool', 'color_input', 'input_string',

    'dict_without_keys', 'dict_with_keys', 'dict_reorder_keys',
    'get_missing_typeddict_keys', 'dedup', 'merge_objs',
    'has_content', 'first_non_default',
    'position_to_index',
    'regex_map',
    'sort_by_other',
    'random_in_bell_curve',

    'json_load', 'json_dump',
    'handle_collision',
    'sanitize_str', 'safely_resolve_path',
    'assert_file',

    'epoch_now',
    'get_domain',
]

"""
Only depends on python std lib
"""

import copy
import json
import os
import random
import re
import sys
import time
import traceback
from collections.abc import Callable, Hashable, Iterable, Mapping, MutableMapping
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison  # noqa: TC004


def get_caller_function(offset: int = 0):
    return sys._getframe(2+offset).f_code.co_qualname


# Source - https://stackoverflow.com/a/69243488
# Posted by Alex Waygood, modified by community. See post 'Timeline' for change history
# Retrieved 2026-07-22, License - CC BY-SA 4.0
class FalsySentinelMeta(type):
    def __repr__(cls) -> str:
        return f'<{cls.__name__}>'
    def __bool__(cls) -> Literal[False]:
        return False
class FalsySentinel(metaclass=FalsySentinelMeta): pass

class __NO_DEFAULT(FalsySentinel): ...
class RAISE_EXC(FalsySentinel): ...
class Delete(FalsySentinel): ...


# Print format helpers

def _hex_to_rgb(hex_str: str|None) -> tuple[int,int,int]|None:
    if hex_str is None:
        return None
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4)) # type: ignore

def hex(text, fg: str|None = None, bg: str|None = None, reset: bool=True):
    return _rgb(text=text,
               fg=_hex_to_rgb(fg),
               bg=_hex_to_rgb(bg),
               reset=reset)

def _rgb(text, fg: tuple[int, int, int]|None = None, bg: tuple[int, int, int]|None = None, reset: bool=True):
    """ Add ANSI commands to text (Select Graphic Rendition) """
    sgr_cmd = '\033[{}m'
    set_fg = sgr_cmd.format(f'38;2;{';'.join(f'{i:03}' for i in fg)}') if fg else ''
    set_bg = sgr_cmd.format(f'48;2;{';'.join(f'{i:03}' for i in bg)}') if bg else ''
    reset_cmd = sgr_cmd.format('0') if reset else ''
    return set_fg \
         + set_bg \
         + str(text) \
         + reset_cmd

EXC_COLOR = '#db6a6a'
WARN_COLOR = '#ffff47'
ERR_COLOR = '#ff4747'
def format_exception(e: BaseException) -> str:
    return hex(''.join(traceback.format_exception(e)).rstrip(), fg=EXC_COLOR)
def WARNING(msg: str, caller_offset: int = 0, auto_print: bool = True) -> str:
    res = ' '.join(
        (hex(" WARNING ", bg=WARN_COLOR),
        hex(f"[{get_caller_function(caller_offset)}]", fg=WARN_COLOR),
        msg))
    if auto_print:
        print(res)
    return res
def ERROR(msg: str, caller_offset: int = 0, auto_print: bool = True) -> str:
    res = ' '.join((
        hex("  ERROR  ", bg=ERR_COLOR),
        hex(f"[{get_caller_function(caller_offset)}]", fg=ERR_COLOR),
        msg))
    if auto_print:
        print(res)
    return res


def truncate(s: str, max_len: int, end='...', *, end_in_max: bool = True, trunc_start: bool = False):
    # note some chars have modifiers/combine with others. eg 👈🏾 is '👈 🏾' and len(👨‍👩🏽‍👧‍👦) == 8
    # so if the modifer is cutoff, the char may change a solution to this is using the graphene library
    # to turn the str into a list of graphemes like 
    # ['T','h','i','s','👈🏾'] instead of ['T','h','i','s','👈',' 🏾']
    # https://stackoverflow.com/a/56282726
    # https://github.com/microsoft/vscode/issues/99629#issuecomment-831565509
    def _truncate(_s: str):
        if len(_s) <= max_len:
            return _s
        if end_in_max:
            return _s[:max_len-len(end)] + end
        return _s[:max_len] + end
    if not trunc_start:
        return _truncate(s)
    return _truncate(s[::-1])[::-1]


def numbered_list(an_iterable: Iterable[Any], start_number: int = 1, indent: int = 0, sort_elems: bool = False) -> str:
    """ Returns the iterable's elements as a numbered list string, doesn't end with a new line (\\n) """
    _list = list(an_iterable)
    max_n = start_number + len(_list)
    max_n_len = len(str(max_n))

    # Allow sort to raise exception if list is unsortable
    # Since `sort_elems` must be manually enabled, the caller should be notified
    if sort_elems:
        _list.sort()
    
    numbered_lines = []
    for i, elem in enumerate(_list, start=start_number):
        num_str = str(i).rjust(max_n_len)
        elem_str = str(elem).replace('\n', '\n'+' '*(indent+len(num_str)))
        numbered_lines.append(f"{" " * indent}{num_str}. {elem_str}")
    return '\n'.join(numbered_lines) # don't start or end with a \n

def clear(one_less_new_line: bool = False):
    """ Moves cursor down to make it look like the console is cleared """
    lines = os.get_terminal_size().lines
    if one_less_new_line: lines -= 1
    print('\n'*lines, end='')
    print('\033[H', end='') # move cursor to top left



# Input helpers

def color_bool(boolean: bool, text: str | None = None) -> str:
    return hex(text or int(boolean), fg="#28E48F" if boolean else "#E64631")

def color_input(inp_color: str):
    try:
        print(hex('', inp_color, reset=False), end='') # set color
        return input()
    finally:
        print(hex(''), end='') # reset color

def input_string(
        options: list[str],
        query_message: str = "",
        prefix_options: bool = True,
        case_sensitive: bool = True,
        attempts: int = -1,
        default: str|type[__NO_DEFAULT] = __NO_DEFAULT,
        use_default_for: set[str] | None = None,
        show_hints: bool = True,
    ) -> str:
    """ returns one of the string options or default if ran out of attempts
    
    input() is called directly after `query_message`. So a new line or space is recommended
    """

    if use_default_for is None:
        use_default_for = set()
    HINT_COLOR = "#76A0A3"
    INPUT_COLOR = "#6BF5FF"
    WARN_COLOR = "#FF1515"

    if not options:
        raise ValueError("Options list cannot be empty.")

    if attempts >= 0 and default is __NO_DEFAULT:
        raise ValueError("Limited attempts requires a default.")
    
    if use_default_for and default is __NO_DEFAULT:
        raise ValueError("Entered use_default_for requires a default")

    option_map = {}
    if not case_sensitive:
        option_map = {s.lower(): s for s in options}
        if not case_sensitive and len(option_map) != len(set(options)):
            raise ValueError("Options that differ only by case must have case-specific inputs.\n"+str(options))
    
    if prefix_options:
        print(numbered_list(
            [f"'{hex(repr(opt)[1:-1], INPUT_COLOR)}'" for opt in options],
            indent=2))

    attempts_left = attempts
    while attempts_left != 0:

        hints = []
        hints.append(hex(f"[ {case_sensitive=} ]", HINT_COLOR))
        if attempts > 0:
            hints.append(hex(f"[ {attempts_left=} ]", HINT_COLOR if attempts_left > 1 else WARN_COLOR))
        if default is not __NO_DEFAULT:
            hints.append(
                hex("[ default= '", HINT_COLOR)
                + hex(default, INPUT_COLOR)
                + hex("' ]", HINT_COLOR)
            )
        hint_header = ' '.join(hints) + '\n' if hints and show_hints else ''

        # prompt user
        print(hint_header + query_message, end='')
        inp = color_input(INPUT_COLOR)

        if inp in options:
            return inp
        elif not case_sensitive and inp.lower() in option_map:
            return option_map[inp.lower()]
        elif inp in use_default_for:
            return default # type: ignore - default is a str
        
        print(
            hex("Unrecognized: '", WARN_COLOR)
            + hex(inp, INPUT_COLOR)
            + hex("'", WARN_COLOR),
            end="\n\n")
        attempts_left -= 1

    print(f"Using default: '{hex(default, HINT_COLOR)}'")

    # ran out of attempts
    return default # type: ignore - default is a str



# Data helpers

def dict_without_keys(d: dict, keys: Iterable):
    """
    Returns a new dict from `d` without the items with any key in `keys`
    - Uses ``copy.deepcopy()``
    """
    new_keys = (d.keys() - keys)
    return {k: copy.deepcopy(v) for k, v in d.items() if k in new_keys}

def dict_with_keys(d: dict, keys: Iterable, default: Any = KeyError):
    """ does not support defaultdict """
    res = {}
    for k in keys:
        if k not in d and default is KeyError:
            raise KeyError(k) # mimic normal key error
        res[k] = copy.deepcopy(d.get(k, default))
    return res

def dict_reorder_keys[K: Hashable](d: MutableMapping[K, Any]|Mapping[K, Any], /, start_order: list[K] = [], end_order: list[K] = []) -> None:  # noqa: B006 - init lists are not mutated
    """
    `d` must be mutable (eg a dict or typeddict).
    
    Reorders keys in `d` in-place according to `order`.

    Keys not in `order` are left at the bottom in their original relative order.
    """

    extra_keys = [k for k in d if k not in (start_order + end_order)]

    for k in start_order:
        if k in d:
            d[k] = d.pop(k) # type: ignore
    for k in extra_keys:
        if k in d:
            d[k] = d.pop(k) # type: ignore
    for k in end_order:
        if k in d:
            d[k] = d.pop(k) # type: ignore

def merge_objs(obj1: Any, obj2: Any, make_copy: bool, copy_fallback: Callable[[Any], Any] = str) -> Any:
    """
    Recursive deep merger.
    Tries to create a deepcopy of values, on exception calls default with the value.

    If obj types mismatch obj2 is chosen (even if obj2 is None/falsy).
    Merges elements of dict, list, tuple, and set.
    """
    def _make_copy(o):
        if not make_copy:
            return o
        try:
            return copy.deepcopy(o)
        except TypeError, RecursionError, copy.Error:
            return copy_fallback(o)

    def _merge_objs(a, b):
        if isinstance(a, dict) and isinstance(b, dict):
            return {
                k: (_merge_objs(a[k], b[k]) if k in a and k in b else
                    _make_copy(a[k]) if k in a else
                    _make_copy(b[k])) 
                        for k in a.keys() | b.keys()
            }
        elif isinstance(a, list) and isinstance(b, (list)):
            return _make_copy(a + b) # duplicates are not removed
        elif isinstance(a, set) and isinstance(b, set):
            return _make_copy(a.union(b))
        elif isinstance(a, tuple) and isinstance(b, tuple):
            return _make_copy(a + b)
        return _make_copy(b)

    return _merge_objs(obj1, obj2)

def get_missing_typeddict_keys(data: dict, typeddict) -> list[str]:
    """ data may contain extra keys """
    if not isinstance(data, dict):
        raise ValueError("data wasn't of type dict")  # noqa: TRY004
    return sorted(set(typeddict.__required_keys__) - set(data.keys()))


def dedup[T](items: Iterable[T], hash: Callable[[T], Hashable]=hash) -> list[T]:
    seen = set()
    res = []
    for x in items:
        h = hash(x)
        if h in seen:
            continue
        seen.add(h)
        res.append(x)
    return res


def has_content(obj: Any) -> bool:
    if not obj:
        return False
    if isinstance(obj, (dict, list, set, tuple)):
        return any(has_content(item) for item in obj)
    return True

def first_non_default(
        d: Mapping, 
        keys: list,
        /, *,
        default_values: list,
        default_return: Any|type[RAISE_EXC] = RAISE_EXC,
) -> Any:
    for k in keys:
        if k not in d:
            continue
        val = d[k]
        if val not in default_values:
            return val
    if default_return is RAISE_EXC:
        raise KeyError(keys)
    return default_return # type: ignore - type V


def position_to_index(position: int, len_: int) -> int:
    """
    Get clamped positive equivalent index [0, len_].

    Behavior:

             _ A _ B _ C _ D _
             1   2   3   4   5 ...
        ... -5  -4  -3  -2  -1

        Ret: 0   1   2   3   4

    """
    if position == 0:
        raise ValueError("Position can't be 0")
    if position > 0:
        position -= 1
    
    clamped = max(-(len_+1), min(position, len_))
    
    if clamped < 0:
        clamped += len_ + 1
        
    return clamped


def regex_map[T, U](m: dict[str, T], s: str, default: U|type[RAISE_EXC] = RAISE_EXC) -> T|U:
    """
    dict key insertion order matters
    
    keys can also be `re.Pattern[str]`
    """
    for k, v in m.items():
        if re.match(k, s):
            return v
    if default is RAISE_EXC:
        raise KeyError(f"No regex matched: {s!r}")
    return default # type: ignore

def sort_by_other[T, K](
        main: list[T],
        other: list[K],
        /, *,
        key: Callable[[tuple[K, T]], SupportsRichComparison]|None = None,
        reverse: bool = False
) -> list[T]:
    if len(main) != len(other):
        raise ValueError(f"main[{len(main)}] and other[{len(other)}] must have same len")
    return [x for _, x in sorted(zip(other, main), key=key, reverse=reverse)]

def random_in_bell_curve(lo: float, hi: float) -> float:
    if lo < hi: lo, hi = hi, lo
    mean = (lo + hi) / 2
    std = (hi - lo) / 8

    # keep trying until you get something in the range
    while True:
        num = random.gauss(mean, std)
        if lo <= num <= hi:
            return num


# File helpers

# Json
def json_load(src: str | Path, default: Any = RAISE_EXC) -> Any:
    """ Try to load src. On failure return default or raise Exception """
    if not os.path.exists(src) and default is not RAISE_EXC:
        return default
    try:
        with open(src, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        if default is RAISE_EXC:
            raise e from None
        WARNING(f"Error in json_load(). Returning default\n{format_exception(e)}")
        return default

def json_dump(
        obj,
        _dst: str|Path,
        on_collision: Literal['rm new', 'rm old', 'mov new', 'mov old'] = 'mov new',
        auto_rename: bool = True,
        indent: int|str|None = None,
) -> Path|None:
    """ Writes json based on selected `on_collision` policy. Returns dst Path used, or None if not written """
    dst = handle_collision(Path(_dst), on_collision, auto_rename)
    if dst is None:
        return # policy chose not to write
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, default=str, indent=indent)
    return dst


# Writing
def _get_unused_name(dst: Path, auto_rename: bool = True, msg: str = "") -> Path:
    """ Find an unused name in dst_dir, optionally let user decide via input().

    Args:
        dst (Path): Destination path, may exist. `dst.parent` should exist.
        auto_rename (bool, optional): Rename by suffixing an incrementing number (e.g. file (10).txt). Defaults to True.
        msg (str, optional): Message to prepend to the initial prompt. Defaults to "".

    Raises:
        FileNotFoundError: if dst_dir does not exist
        ValueError: if dst_dir isn't a directory

    Returns:
        Path: Unusued Path. If the name is already unused, the input name is returned.
    """
    dst_dir = dst.parent
    dst_name = dst.name
    if not dst_dir.exists():
        raise FileNotFoundError("dst_dir does not exist")
    if not dst_dir.is_dir():
        raise ValueError(f"dst_dir should be a directory. {dst_dir = }")
    
    stem, ext = os.path.splitext(dst_name)

    i = 1
    while dst_name in os.listdir(dst_dir):
        if i == 1 and not auto_rename:
            print(msg, end='')
            print(f"Directory:\n\t{list(dst_dir.iterdir())}\n")
            print(f"Enter the new name for {dst_name} (include extension):")
        if not auto_rename:
            if i > 1:
                print(f"{dst_name!r} is already in use. Try again.")
            dst_name = input()
        else:
            dst_name = f"{stem} ({i}){ext}"
        
        i += 1
    return dst_dir / dst_name

CollisionPolicies = Literal['rm new', 'rm old', 'mov new', 'mov old']
def _handle_collision(
        dst: Path,
        on_collision: CollisionPolicies = 'mov new',
        auto_rename: bool = True
) -> tuple[Path|type[Delete], Path|type[Delete]|None]:
    """
    Returns changes based on arguments.
    - `Path`   = Write or move to that Path
    - `Delete` = Don't write new info or unlink old info
    - `None`   = No action needed
    
    The old action must happen before the new action
    """

    renamed = lambda: _get_unused_name(
        dst, auto_rename,
        msg="Rename new file...\n" if on_collision=='mov new' else
            "Rename existing flle...\n")
    
    match dst.exists(), on_collision:
        case False,  _:         return (dst,        None)
        case True,  'rm new':   return (Delete,     None)
        case True,  'rm old':   return (dst,        Delete)
        case True,  'mov new':  return (renamed(),  None)
        case True,  'mov old':  return (dst,        renamed())
    
    raise ValueError(f"Unkonwn on_collision option: {on_collision}")

def handle_collision(
        dst: Path,
        on_collision: Literal['rm new', 'rm old', 'mov new', 'mov old'] = 'mov new',
        auto_rename: bool = True,
) -> Path | None:
    """
    Performs collision resolution given the policy.
    Call and return ``func(path)`` if it should be written,
    otherwise just return `NO_DEFALT`.
    """
    new, old = _handle_collision(dst, on_collision, auto_rename)

    if old is Delete:
        os.unlink(dst)
    if isinstance(old, Path):
        os.rename(dst, old)

    if isinstance(new, Path):
        return new
    return None

# Sanitization
def sanitize_str(s, data: dict, sanitizer: Callable[[str], str]|None = None) -> str:
    if sanitizer is None:
        def default_part_sanitizer(s: str):
            invalid = r'\/:*?"<>|'
            for c in invalid:
                s = s.replace(c, '_')
            return s
        sanitizer = default_part_sanitizer

    return sanitizer(s % data)

def safely_resolve_path(path: Path|str, part_data: list[dict]|dict|None = None, part_sanitizer: Callable[[str], str]|None = None) -> Path:
    """ Sanitizes and resolves path, can be given part data.

    Args:
        path (Path): Path to resolve
        part_data (list[dict] | dict, optional): Dict info for the last parts of the path ordered left to right.
                If a dict, pass it to all parts. Defaults to {}.

                For example, if `part_data = [{1}, {2}, {3}]`,
                that data will be used like `... / _dir_name % {1} / _dir_name % {2} / _name % {3}`.
        part_sanitizer (Callable[[str], str | Path] | None, optional): Sanitize each part of the path.
                Defaults to replacting `\\/:*?"<>|` with `_`. Doesn't handle `..`, `.`, `<space>`-only, or empty paths

    Returns:
        Path: Resolved Path
    """
    if part_data is None:
        part_data = {}
    if isinstance(path, str):
        path = Path(path)
    if part_sanitizer is None:
        def default_part_sanitizer(s: str):
            invalid = r'\/:*?"<>|'
            for c in invalid:
                s = s.replace(c, '_')
            return s
        part_sanitizer = default_part_sanitizer

    sanitized_parts = []
    _parts = path.parts
    for i in range(len(_parts)):
        if isinstance(part_data, dict):
            sanitized_parts.append(_parts[i] % part_data)
            continue
        _i = len(part_data) - len(_parts) + i
        if _i >= 0:
            sanitized_parts.append(_parts[i] % part_data[_i])
        else:
            sanitized_parts.append(_parts[i])

    if os.name == 'nt' and path.drive:
        sanitized_parts[0] = path.drive + '\\' # isn't added for some reason
    return Path(*sanitized_parts).resolve()

# Assertion
def assert_file(p: str|None, name: str, min_size: int = 0, None_is_ok: bool = False):
    if p is None:
        if None_is_ok:
            return
        raise FileNotFoundError(f"{name} can not be None. Expected str path.\nPath: {p}")
    if not os.path.exists(p):
        raise FileNotFoundError(f"{name} does not exist.\nPath: {p}")
    if min_size <= 0:
        return
    size = os.stat(p).st_size
    if size < min_size:
        raise RuntimeError(f"{name} is {size} bytes. Expected >= {min_size}.\nPath: {p}")



# Epoch

def epoch_now():
    return int(time.time())



# urls

def get_domain(url: str) -> str|None:
    """ If the url is malformed, the result may be weird """
    
    # Source - https://stackoverflow.com/a/25703406
    # Posted by anubhava, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-07-20, License - CC BY-SA 4.0
    pattern = r'^(?:(?:https?:)?\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)'
    match = re.match(pattern, url)
    return match.groups()[0] if match else None
