__all__ = [
    'hex',
    'exc', 'WARNING', 'ERROR',
    'truncate', 'numbered_list', 'clear',
    'input_string',

    'dict_without_keys', 'dict_with_keys',
    'get_missing_typeddict_keys', 'dedup', 'dict_merge',

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

from pathlib import Path
import os
import time
import datetime
from typing import Iterable, Any, Callable, Literal, Hashable
import json
import copy
import re
import traceback



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
    set_fg = sgr_cmd.format(f'38;2;{';'.join(map(lambda i:f'{i:03}', fg))}') if fg else ''
    set_bg = sgr_cmd.format(f'48;2;{';'.join(map(lambda i:f'{i:03}', bg))}') if bg else ''
    reset_cmd = sgr_cmd.format('0') if reset else ''
    return set_fg \
         + set_bg \
         + str(text) \
         + reset_cmd

def exc(e: BaseException) -> str:
    return hex(''.join(traceback.format_exception(e)).rstrip(), fg='#db6a6a')

def WARNING(msg: str) -> None:
    print(hex(" WARNING ", bg="#ffff47"), msg)
def ERROR(msg: str) -> None:
    print(hex("  ERROR  ", bg="#ff4747"), msg)


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
    try:
        if sort_elems:
            _list.sort()
    except Exception:
        ...
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

class __NO_DEFAULT: ...
def input_string(
        options: list[str],
        query_message: str = "",
        prefix_options: bool = True,
        case_sensitive: bool = True,
        attempts: int = -1,
        default: str|type[__NO_DEFAULT] = __NO_DEFAULT,
        use_default_for: set[str] = set(),
        show_hints: bool = True,
    ) -> str:
    """ returns one of the string options or default if ran out of attempts
    
    input() is called directly after `query_message`. So a new line or space is recommended
    """

    HINT_COLOR = "#76A0A3"
    INPUT_COLOR = "#6BF5FF"
    WARN_COLOR = "#FF1515"

    if not options:
        raise ValueError("Options list cannot be empty.")

    if attempts >= 0 and default is __NO_DEFAULT:
        raise ValueError("Limited attempts requires a default.")
    
    if use_default_for and default is __NO_DEFAULT:
        raise ValueError("Entered use_default_for requires a default")

    option_map = dict()
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
        try:
            print(hex('', INPUT_COLOR, reset=False), end='') # set color
            inp = input()
        finally:
            print(hex(''), end='') # reset color

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
    res = dict()
    for k in keys:
        if k not in d and default is KeyError:
            raise KeyError(k) # mimic normal key error
        res[k] = copy.deepcopy(d.get(k, default))
    return res

class PRINT_WARNING: ...
class RAISE_EXC: ...


def get_missing_typeddict_keys(data: dict, typeddict) -> list[str]:
    """ data may contain extra keys """
    if not isinstance(data, dict):
        raise ValueError("data wasn't of type dict")
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


def dict_merge(dict1: dict, dict2: dict) -> dict:
    """ Recursive dict merge. `dict2` is prioritized in collisions. """
    res = dict1.copy()
    for key, value in dict2.items():
        # dict collision
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            res[key] = dict_merge(res[key], value)
        else:
            # dict2 overwrites non-dict collisions
            res[key] = value
    return res


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
        WARNING(f"Error in json_load(). Returning default\n{exc(e)}")
        return default

# def json_load_typeddict(src: str | Path, typeddict, default: Any|type[RAISE_EXC] = RAISE_EXC) -> Any:
#     """
#     Load json and check if required keys are present. Extra keys are ok.
#     Or follow default: return default or raise Exception.
#     """
#     obj = json_load(src, default)
#     try:
#         missing_keys = get_missing_typeddict_keys(obj, typeddict)
#         if not missing_keys:
#             return obj
#     except Exception as e:
#         msg = f"Error in get_missing_typeddict_keys(). Returning default.\nPath: {src}\nExpected {typeddict}\n{e}"
#         if default is RAISE_EXC:
#             raise TypeError(msg) from None
#         WARNING(msg)
#         return default

#     if missing_keys:
#         msg = f"Path: {src}\nExpected {typeddict}\nMissing keys: {missing_keys}"
#         if default is RAISE_EXC:
#             raise TypeError(msg)
#         WARNING(msg)
#     return default

def json_dump(
        obj,
        _dst: str|Path,
        on_collision: Literal['rm new', 'rm old', 'mov new', 'mov old'] = 'mov new',
        auto_rename: bool = True,
) -> Path|None:
    """ Writes json based on selected `on_collision` policy. Returns dst Path used, or None if not written """
    dst = handle_collision(Path(_dst), on_collision, auto_rename)
    if dst is None:
        return # policy chose not to write
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, default=str)
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
        raise FileNotFoundError(f"dst_dir does not exist")
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
                print(f"{repr(dst_name)} is already in use. Try again.")
            dst_name = input()
        else:
            dst_name = f"{stem} ({i}){ext}"
        
        i += 1
    return dst_dir / dst_name

class Delete: ...
CollisionPolicies = Literal['rm new', 'rm old', 'mov new', 'mov old']
def _handle_collision(
        dst: Path,
        on_collision: CollisionPolicies = 'mov new',
        auto_rename: bool = True
) -> tuple[Path|Delete, Path|Delete|None]:
    """ Returns changes based on arguments.

        Returns:
        ```
            tuple[
                new: Path|Delete, 
                old: Path|Delete|None
            ]
        ```
        - `Path` is the Path to write or move it to
        - `Delete` means don't write or unlink
        - `None` means it wasn't found
        
        All Branches:
        ```
            NO Collision:
                (new, None)
            Collision:
                'rm new'  -> (`Delete`, None)
                'rm old'  -> (new, `Delete`)
                'mov new'  -> (new_renamed, None)
                'mov old'  -> (new, old_renamed)
        ```
    """
    if not dst.exists():
        return (dst, None)

    # names_in_dst = os.listdir(dst_dir)
    # collision = any(name == desired_filename for name in names_in_dst)
    # if not collision:
    #     return None, [dst_path, dst_path]

    if on_collision == 'rm new':
        return (Delete(), None)

    if on_collision == 'rm old':
        return (dst, Delete())

    renamed = _get_unused_name(
        dst, auto_rename,
        msg="Rename new file...\n" if on_collision=='mov new' else
            "Rename existing flle...\n")
    if on_collision == 'mov new':
        return (renamed, None)
    
    if on_collision == 'mov old':
        return (dst, renamed)
    
    raise ValueError(f"Unkonwn on_collision option: {on_collision}")

def _setup_handle_collision(dst: Path, old: Path|Delete|None):
    if isinstance(old, Delete):
        os.unlink(dst)
    if isinstance(old, Path):
        os.rename(dst, old)

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
    _setup_handle_collision(dst, old)
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

def safely_resolve_path(path: Path|str, part_data: list[dict]|dict = {}, part_sanitizer: Callable[[str], str]|None = None) -> Path:
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
