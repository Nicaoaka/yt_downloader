from pathlib import Path
import os
import datetime
from typing import Iterable, Any, Callable, Literal
import json
import copy


class __NO_DEFAULT:
    """ DO NOT USE outside of `utils.py` """
    ...


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


def WARNING(msg: str) -> None:
    print(hex(" WARNING ", bg="#ffff47"), msg)


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


def format_epoch(epoch: float | None):
    if epoch is None:
        return "[Epoch Unknown]"
    return datetime.datetime.strftime(datetime.datetime.fromtimestamp(epoch), '%Y/%m/%d %H:%M:%S')


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
        raise ValueError('Entered use_default_for requires a default')

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
                hex('[ default= \'', HINT_COLOR)
                + hex(default, INPUT_COLOR)
                + hex('\' ]', HINT_COLOR)
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
            end='\n\n')
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

class UNSET: ...
def dict_set_if(d: dict, k, repl, match=[UNSET, None]) -> bool:
    """ if `d.get(k, NO_DEFAULT)`in `match`: set `d[k] = repl`
    
    Does not create a deep copy of `repl`

    Returns:
        False if no replace, or if repl is the same as the default. True if there was a change.
    """
    v = d.get(k, UNSET)
    if v not in match:
        return False
    if repl == v:
        return False
    d[k] = repl
    return True


class RAISE_EXC: ...
def first_non_None[T,U](items: Iterable[T], default: U = RAISE_EXC) -> T|U:
    for x in items:
        if x is not None:
            return x
    if default is RAISE_EXC:
        raise RuntimeError("All items were None, and no default was provided")
    return default


def isinstance_typeddict(data, typeddict, raise_exc: bool = False) -> bool:
    """ data may contain extra keys """
    if not isinstance(data, dict):
        if raise_exc:
            raise TypeError(f"Expected dict, got {type(data)}")
        return False
    
    for k in typeddict.__required_keys__:
        if k not in data:
            if raise_exc:
                missing = set(typeddict.__required_keys__) - set(data.keys())
                raise TypeError(
                    f"Malformed\n"
                    f"Missing keys: {', '.join(sorted(missing))}\n")
            return False
    return True


def dif_sets(a: set, b: set) -> tuple[set, set]:
    return a - b, b - a



# File helpers

# Json
def json_load(src: str | Path, default: Any = RAISE_EXC) -> Any:
    """
    What the function does:
    ```
    if exist and no json error
        return loaded json
    if doesn't exist or json error:
        RAISE_EXC or default
    ```
    """
    if not os.path.exists(src) and default is not RAISE_EXC:
        return default
    try:
        with open(src, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        if default is RAISE_EXC:
            raise e from None
        WARNING(e.msg)
        return default

def json_load_typeddict(src: str | Path, typeddict, default: Any = RAISE_EXC) -> Any:
    """
    Like ``json_load()``, but check typeddict keys wil ``isinstance_typeddict()``
    """
    obj = json_load(src, default)
    try:
        if isinstance_typeddict(obj, typeddict, raise_exc=(default is RAISE_EXC)):
            return obj
    except TypeError as e:
        raise TypeError(f'{e}\nPath: {src}\nExpected: {typeddict}') from None

def json_dump(
        obj,
        dst: str|Path,
        on_collision: Literal['rm new', 'rm old', 'mov new', 'mov old'] = 'mov new',
        auto_rename: bool = True,
):
    def _json_dump(dst: Path):
        dst.parent.mkdir(parents=True, exist_ok=True) # type: ignore
        with open(dst, 'w', encoding='utf-8') as f:
            # 日本語 and 絵文字 are expected!
            json.dump(obj, f, ensure_ascii=False, default=str)
        print(hex(f"[write_json] \"{dst.absolute()}\"", '#c800c8'))
    handle_collision(Path(dst), _json_dump, on_collision, auto_rename)


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
            dst_name = f'{stem} ({i}){ext}'
        
        i += 1
    return dst_dir / dst_name

class Delete: ...
def _handle_collision(
        dst: Path,
        on_collision: Literal['rm new', 'rm old', 'mov new', 'mov old'] = 'mov new',
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

def handle_collision[T](
        dst: Path,
        func: Callable[[Path], T],
        on_collision: Literal['rm new', 'rm old', 'mov new', 'mov old'] = 'mov new',
        auto_rename: bool = True,
) -> type[__NO_DEFAULT] | T:
    """
    Performs collision resolution given the policy.
    Call and return ``func(path)`` if it should be written,
    otherwise just return `NO_DEFALT`.
    """
    new, old = _handle_collision(dst, on_collision, auto_rename)
    _setup_handle_collision(dst, old)
    if isinstance(new, Path):
        return func(new)
    return __NO_DEFAULT


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
def assert_file(p: str|None, name: str, min_size: int = 0, or_None: bool = False):
    if p is None:
        if not or_None:
            raise ValueError(f"{name} can not be None. Expected str path.\nPath: {p}")
        return
    if not os.path.exists(p):
        raise FileNotFoundError(f"{name} does not exist.\nPath: {p}")
    if min_size <= 0:
        return
    size = os.stat(p).st_size
    if size < min_size:
        raise RuntimeError(f"{name} is {size} bytes. Expected >= {min_size}.\nPath: {p}")



# Misc

def epoch_now():
    return round(datetime.datetime.now().timestamp())



def main():
    import random
    print(input_string(['abc', 'def', 'ghi'], "Enter your favorite string! "))
    pass

if __name__ == "__main__":
    main()