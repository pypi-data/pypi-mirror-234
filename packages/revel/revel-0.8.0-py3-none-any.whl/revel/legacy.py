import atexit
import enum
import io
import sys
import time
import typing
from abc import ABC, abstractmethod
from datetime import timedelta
from sys import stdin, stdout
from typing import *  # type: ignore

import blessed
import readchar
from . import markup as markup_module

from .style import Back, Fore, Format

# These aren't available on all platforms
try:
    import readline  # type: ignore  (Just importing readline activates it)
    import termios
except ImportError:
    readline = None
    termios = None


# Keep track of the environment the script is running in
def _detect_mode() -> Literal["terminal", "ipython", "jupyter"]:
    try:
        _ipy_str = str(type(get_ipython()))  # type: ignore
    except NameError:
        return "terminal"

    if "zmqshell" in _ipy_str:
        return "jupyter"

    return "ipython"


mode = _detect_mode()

T = TypeVar("T")
_SENTINEL = object()
_py_input = input

# Keep track of global state
_docked_widget: Optional["Widget"] = None
_chapter: Optional[str] = None
_is_first_line = True
_is_in_new_line = True

# The position of the leftmost character in each line. This is 0 if outside of
# chapters, and higher if inside a chapter
_start_x: int = 0


_KEY_NAMES = {
    readchar.key.ENTER: "\n",
    readchar.key.CR: "\r",
    readchar.key.SPACE: " ",
    readchar.key.ESC: "escape",
    readchar.key.TAB: "\t",
    readchar.key.BACKSPACE: "backspace",
    readchar.key.UP: "up",
    readchar.key.DOWN: "down",
    readchar.key.LEFT: "left",
    readchar.key.RIGHT: "right",
    readchar.key.INSERT: "insert",
    readchar.key.HOME: "home",
    readchar.key.END: "end",
    readchar.key.PAGE_UP: "page-up",
    readchar.key.PAGE_DOWN: "page-down",
    readchar.key.F1: "f1",
    readchar.key.F2: "f2",
    readchar.key.F3: "f3",
    readchar.key.F4: "f4",
    readchar.key.F5: "f5",
    readchar.key.F6: "f6",
    readchar.key.F7: "f7",
    readchar.key.F8: "f8",
    readchar.key.F9: "f9",
    readchar.key.F10: "f10",
    readchar.key.F11: "f11",
    readchar.key.F12: "f12",
    readchar.key.DELETE: "delete",
    readchar.key.CTRL_A: "ctrl-a",
    readchar.key.CTRL_B: "ctrl-b",
    readchar.key.CTRL_C: "ctrl-c",
    readchar.key.CTRL_D: "ctrl-d",
    readchar.key.CTRL_E: "ctrl-e",
    readchar.key.CTRL_F: "ctrl-f",
    readchar.key.CTRL_G: "ctrl-g",
    readchar.key.CTRL_H: "ctrl-h",
    readchar.key.CTRL_I: "ctrl-i",
    readchar.key.CTRL_J: "ctrl-j",
    readchar.key.CTRL_K: "ctrl-k",
    readchar.key.CTRL_L: "ctrl-l",
    readchar.key.CTRL_M: "ctrl-m",
    readchar.key.CTRL_N: "ctrl-n",
    readchar.key.CTRL_O: "ctrl-o",
    readchar.key.CTRL_P: "ctrl-p",
    readchar.key.CTRL_Q: "ctrl-q",
    readchar.key.CTRL_R: "ctrl-r",
    readchar.key.CTRL_S: "ctrl-s",
    readchar.key.CTRL_T: "ctrl-t",
    readchar.key.CTRL_U: "ctrl-u",
    readchar.key.CTRL_V: "ctrl-v",
    readchar.key.CTRL_W: "ctrl-w",
    readchar.key.CTRL_X: "ctrl-x",
    readchar.key.CTRL_Y: "ctrl-y",
    readchar.key.CTRL_Z: "ctrl-z",
    # These can clash with some other keys (probably depending on platform?). By
    # defining them here they receive priority over the other keys.
    readchar.key.ENTER: "\n",  # Clashes with "ctrl-j" on unix
    readchar.key.CR: "\r",  # Clashes with "ctrl-m" on unix
    readchar.key.TAB: "\t",  # Clashes with "ctrl-i" on unix
}


def input_key(
    *,
    raise_on_eof: bool = True,
    raise_on_interrupt: bool = True,
) -> str:
    """
    Get a single keypress from the user.

    Regular characters are returned as-is, any special keys (such as "enter")
    are translated to strings. The strings for regular characters are always one
    character long, while the strings for special keys are guaranteed to be
    longer.

    In addition to regular characters, the following special keys strings may be
    returned:

    - escape
    - backspace
    - up
    - down
    - left
    - right
    - insert
    - home
    - end
    - page-up
    - page-down
    - f1
    - f2
    - f3
    - f4
    - f5
    - f6
    - f7
    - f8
    - f9
    - f10
    - f11
    - f12
    - delete
    - ctrl-a
    - ctrl-b
    - ctrl-c
    - ctrl-d
    - ctrl-e
    - ctrl-f
    - ctrl-g
    - ctrl-h
    - ctrl-i
    - ctrl-j
    - ctrl-k
    - ctrl-l
    - ctrl-m
    - ctrl-n
    - ctrl-o
    - ctrl-p
    - ctrl-q
    - ctrl-r
    - ctrl-s
    - ctrl-t
    - ctrl-u
    - ctrl-v
    - ctrl-w
    - ctrl-x
    - ctrl-y
    - ctrl-z

    Note that not all keys can be detected on all platforms. That's because some
    platforms use the same internal code for different keys, making it
    impossible to distinguish them.

    If `raise_on_eof` is `True`, an `EOFError` will be raised if the user
    presses Ctrl+D. If `raise_on_interrupt` is `True`, a `KeyboardInterrupt` is
    raised if the user presses Ctrl+C. These are the default, to allow users to
    interrupt the program as they would expect.
    """
    # Get a key
    key = readchar.readkey()

    # Ctrl+C
    if raise_on_interrupt and key == readchar.key.CTRL_C:
        raise KeyboardInterrupt()

    # Ctrl+D / EOF
    if raise_on_eof and key == readchar.key.CTRL_D:
        raise EOFError()

    # Translate special characters and return
    return _KEY_NAMES.get(key, key)


class Widget(ABC):
    def __init__(self):
        self._parent: Optional[Widget] = None

    def mark_dirty(self) -> None:
        """
        Mark this widget as dirty, requesting a redraw.
        """

        # If this widget has a parent, let that handle the call instead
        if self._parent is not None:
            self._parent.mark_dirty()
            return

        # The widget isn't docked, there is nothing it can do
        if not self.is_docked:
            return

        # Redraw
        term = blessed.Terminal()
        stdout.write(term.clear_bol())  # type: ignore
        stdout.write(term.move_x(_start_x))
        self.draw(term)

    @property
    def is_docked(self) -> bool:
        """
        Returns `True` if this widget is currently docked and `False` otherwise.
        """
        return self is _docked_widget

    def undock(self) -> None:
        global _docked_widget
        if _docked_widget is not self:
            raise ValueError("Widget is not docked")

        _docked_widget = None
        self.on_undock()

    def on_dock(self) -> None:
        """
        Called whenever a widget is being docked.
        """
        pass

    def on_undock(self) -> None:
        """
        Called whenever a widget is being undocked.
        """
        pass

    @abstractmethod
    def draw(self, term: blessed.Terminal) -> None:
        """
        Draw the widget. The curser is at the top left position of the widget.

        TODO: Where should the cursor be after the widget is drawn?
        """
        pass


class TextLine(Widget):
    """
    A simple line of text, optionally formatted with `rich` style markup.
    """

    _text: str

    def __init__(self, text: str = "", *, markup: bool = True):
        super().__init__()

        self.text = text
        self.markup = markup

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: Any) -> None:
        self._text = str(value)
        self.mark_dirty()

    def draw(self, term: blessed.Terminal) -> None:
        if self.markup:
            stdout.write(markup_module.unescape(self.text))
        else:
            stdout.write(self.text)

        stdout.flush()


class Unit(enum.Enum):
    """
    Internal class for representing a unit.
    """

    COUNT = enum.auto()
    PERCENT = enum.auto()
    BYTE = enum.auto()
    TIME = enum.auto()

    @classmethod
    def from_string(cls, value: str) -> "Unit":
        if value == "count":
            return cls.COUNT
        elif value == "percent":
            return cls.PERCENT
        elif value == "byte":
            return cls.BYTE
        elif value == "time":
            return cls.TIME
        else:
            raise ValueError(f"Unknown unit type: {value}")

    def __str__(self) -> str:
        return self.name.lower()

    def _units(self) -> Iterable[Tuple[str, float, bool]]:
        """
        Return names of all units for this type and the divisor to convert from
        the base unit to them. The results are ordered from smallest to largest.
        In addition, a boolean is also returned, which indicates whether this
        unit is favorable (i.e. not an outdated or otherwise undesirable unit).
        """

        if self is Unit.COUNT:
            yield "", 1, True

        elif self is Unit.PERCENT:
            yield "%", 100, True

        elif self is Unit.BYTE:
            yield "B", 1, True
            yield "KB", 1000, False
            yield "KiB", 1024, True
            yield "MB", 1000**2, False
            yield "MiB", 1024**2, True
            yield "GB", 1000**3, False
            yield "GiB", 1024**3, True
            yield "TB", 1000**4, False
            yield "TiB", 1024**4, True
            yield "PB", 1000**5, False
            yield "PiB", 1024**5, True

        elif self is Unit.TIME:
            yield "ms", 1 / 1000, True
            yield "s", 1, False
            yield "second", 1, True
            yield "m", 60, False
            yield "minute", 60, True
            yield "h", 60 * 60, False
            yield "hour", 60 * 60, True
            yield "d", 60 * 60 * 24, False
            yield "day", 60 * 60 * 24, True

        else:
            raise NotImplementedError(f"Unknown unit type: {self}")

    def pretty_approximate_value(self, value: Union[int, float]) -> str:
        # Count: there is nothing to do here
        if self == Unit.COUNT:
            return str(round(value))

        # Time: This is a special case, because multiple units are used in the
        # result
        if self == Unit.TIME:
            seconds = int(value)

            # Special case: 0
            if seconds == 0:
                return "none"

            # Determine the time, in multiple sub-units
            units = (
                ("second", 60),
                ("minute", 60),
                ("hour", 24),
                ("day", None),
            )

            parts = []

            amount = seconds
            for unit_info in units:
                unit_name, unit_factor = unit_info

                if unit_factor is None:
                    cur = amount
                else:
                    cur = amount % unit_factor
                    amount = amount // unit_factor

                if cur == 0:
                    continue

                parts.append((unit_name, cur))

            # Drop any pointless ones
            while len(parts) > 2:
                parts.pop(0)

            # Turn everything into a string
            chunks = []
            for unit_name, amount in reversed(parts):
                if amount == 1:
                    chunks.append(f"1 {unit_name}")

                else:
                    chunks.append(f"{amount} {unit_name}s")

            return " ".join(chunks)

        # All other units: Find the largest unit that is still smaller than the
        # value
        unit_name, unit_factor = "", 1

        for next_unit_name, next_unit_factor, desirable in self._units():
            if not desirable:
                continue

            if value < next_unit_factor:
                break

            unit_name, unit_factor = next_unit_name, next_unit_factor

        # Round as appropriate
        unit_value = value / unit_factor

        if unit_value == int(unit_value):
            unit_value = int(unit_value)
        elif unit_value < 10:
            unit_value = round(unit_value, 1)
        else:
            unit_value = round(unit_value)

        return f"{unit_value}{unit_name}"  # type: ignore


class ProgressBar(Widget):
    """
    A progress bar, duh.

    Sample usage:

    ```py
    bar = print(
        ProgressBar(max=100, unit="count"),
        dock=True,
    )

    for ii in range(100):
        bar.progress = ii
        time.sleep(0.1)

    bar.complete()
    ```
    """

    _progress: float
    _width: int
    _unit: Unit

    def __init__(
        self,
        progress: Union[int, float] = 0.0,
        max: Union[int, float] = 1.0,
        width: int = 50,
        unit: Literal["count", "percent", "byte", "time"] = "percent",
    ):
        super().__init__()

        # Data used to predict an ETA. This is a list of (timestamp, progress)
        # tuples, with `progress` being in range [0, 1]
        self._progress_timestamps: List[Tuple[float, float]] = []

        self._last_update_time: float = 0.0
        self._last_update_fraction = self._calc_fraction(progress, max)

        self.max = max  # The `progress` setter uses this value, set it first
        self.progress = progress
        self.width = width
        self.unit = unit

    @property
    def progress(self) -> Union[int, float]:
        """
        How far the progress bar is filled. A value of 0 means that the bar is
        empty, while a value of `bar.max` means that the bar is completely
        filled.
        """
        return self._progress

    @progress.setter
    def progress(self, value: Union[int, float]) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("The progressbar's progress must be an integer or float")

        self._progress = value

        # Trigger a redraw, but only if necessary. For quick tasks, updating the
        # progressbar can be orders of magnitude more expensive than the task
        # itself. To prevent this, limit how often the progressbar is updated.
        now = time.time()
        new_fraction = self._calc_fraction(value, self.max)
        if (
            now - self._last_update_time > 0.1
            or abs(new_fraction - self._last_update_fraction) > 0.2
        ):
            self.mark_dirty()
            self._last_update_time = now
            self._last_update_fraction = new_fraction

        # Keep track of the progress so an ETA can be calculated later on. If
        # the progressbar was just reset to 0, it is probably about to be
        # reused, making the previous timestamps invalid
        if value == 0:
            self._progress_timestamps = []
        else:
            self._progress_timestamps.append((time.time(), self.fraction))

            # Don't keep too many timestamps
            time_cutoff = time.time() - 45
            while (
                len(self._progress_timestamps) > 40
                and self._progress_timestamps[1][0] < time_cutoff
            ):
                del self._progress_timestamps[0]

            if len(self._progress_timestamps) > 100:
                self._progress_timestamps = self._progress_timestamps[::2]

    @property
    def max(self) -> Union[int, float]:
        """
        The value at which the bar is considered completely filled.
        """
        return self._max

    @max.setter
    def max(self, value: Union[int, float]) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("The progressbar's maximum value must be a float")

        if value < 0:
            raise ValueError("The progressbar's maximum value cannot be negative")

        self._max = value
        self.mark_dirty()

    @property
    def width(self) -> int:
        """
        The progress bar's width, in characters.
        """
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("The progressbar's width must be an integer")

        if value < 0:
            raise ValueError("The progressbar's width must be a positive integer")

        # TODO: Only redraw if the value has changed by a significant amount?
        # Scripts which report progress very frequently actually experience a
        # massive slowdown, because rendering the bar takes more time than
        # actually doing the work

        self._width = value
        self.mark_dirty()

    def _calc_fraction(self, progress: float, max: float) -> float:
        try:
            return min(progress / max, 1.0)
        except ZeroDivisionError:
            return 0.0

    @property
    def fraction(self) -> float:
        """
        The bar's current progress fraction, as float in range [0, 1].
        """
        return self._calc_fraction(self.progress, self.max)

    @property
    def unit(self) -> str:
        """
        The unit used to display the progress bar's value.
        """
        return str(self._unit)

    @unit.setter
    def unit(self, value: Literal["count", "percent", "byte", "time"]) -> None:
        self._unit = Unit.from_string(value)
        self.mark_dirty()

    def complete(self) -> None:
        """
        Convenience method which sets the bar's progress to its maximum value
        and undocks the bar if it is docked.
        """
        # Force a redraw
        self._last_update_time = 0.0
        self._last_update_fraction = -1.0

        # Set the progress to the maximum value
        self.progress = self.max

        if self.is_docked:
            self.undock()

    @property
    def eta(self) -> Optional[timedelta]:
        """
        The estimated time until the progress bar is complete, or `None` if
        there is not enough data to calculate an ETA with reasonable confidence.
        """
        # Not enough data
        if not self._progress_timestamps or len(self._progress_timestamps) < 3:
            return None

        first_time, first_fraction = self._progress_timestamps[0]
        cur_time, cur_fraction = self._progress_timestamps[-1]

        # Funky data
        if first_time >= cur_time or first_fraction >= cur_fraction:
            return None

        # Good data
        speed = (cur_fraction - first_fraction) / (cur_time - first_time)
        assert speed > 0, speed
        return timedelta(seconds=(1 - cur_fraction) / speed)

    @property
    def bar_string(self) -> str:
        """
        The string representation of the progress bar. This only includes the
        bar, not any text around it. The returned string may be colored, and
        thus should be printed as markup.
        """
        blocks = "·▏▎▍▌▋▊▉█"
        fraction = self.fraction

        # Fully filled blocks
        n_blocks_remaining = self.width
        n_blocks_filled = int(fraction * n_blocks_remaining)
        bar_string = "[blue]" + n_blocks_filled * blocks[-1]
        n_blocks_remaining -= n_blocks_filled

        # Partial block
        partial_frac = fraction * self.width - n_blocks_filled
        partial_index = round(partial_frac * (len(blocks) - 1))
        if n_blocks_remaining > 0 and partial_index != 0:
            bar_string += blocks[partial_index]
            n_blocks_remaining -= 1

        bar_string += "[/]"

        # Empty blocks
        bar_string += n_blocks_remaining * blocks[0]

        return bar_string

    def draw(self, term: blessed.Terminal) -> None:
        # Display the bar
        stdout.write(markup_module.unescape(self.bar_string))

        # Display written progress
        unit = Unit.from_string(self.unit)  # type: ignore
        fraction = self.fraction

        if unit == Unit.PERCENT:
            stdout.write(f" {fraction*100:.1f}%")
        elif unit == Unit.TIME:
            if fraction != 1:
                stdout.write(
                    f"  {unit.pretty_approximate_value(self.max - self.progress)}"
                )
        elif fraction == 1:
            stdout.write(f"  {unit.pretty_approximate_value(self.max)}")
        else:
            stdout.write(
                f"  {unit.pretty_approximate_value(self.progress)} ╱ {unit.pretty_approximate_value(self.max)}"
            )

        # Display an ETA
        if fraction != 1:
            eta = self.eta
            if eta is not None:
                pretty_str = Unit.TIME.pretty_approximate_value(eta.total_seconds())
                stdout.write(
                    markup_module.unescape(
                        f"[bright_black] — about {pretty_str} remaining[/]"
                    )
                )

        stdout.flush()

    def __enter__(self) -> "ProgressBar":
        print(self, dock=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.complete()


def get_docked_widget() -> Optional[Widget]:
    """
    Returns the currently docked widget, or `None` if no widget is docked.
    """
    return _docked_widget


def _print_newline(n_newlines: int = 1) -> None:
    global _is_in_new_line
    assert n_newlines >= 0, n_newlines

    if n_newlines == 0:
        return

    if _is_in_new_line:
        n_newlines -= 1

    stdout.write("\n" * n_newlines)
    _is_in_new_line = False


Tprint = TypeVar("Tprint", bound=Widget)


@typing.overload
def print(*values: Tprint, dock: bool = False, markup: bool = True) -> Tprint:
    ...


@typing.overload
def print(*values: Any, dock: bool = False, markup: bool = True) -> TextLine:
    ...


def print(*values: Any, dock: bool = False, markup: bool = True) -> Widget:
    """
    Prints a widget to the terminal, optionally docking it.

    If a single widget is passed it is returned, otherwise the inputs are
    converted to strings, joined with a space and returned as a `TextLine`.
    """
    global _docked_widget, _is_first_line, _is_in_new_line

    # Convert the inputs to a single Widget
    if len(values) == 1 and isinstance(values[0], Widget):
        widget = values[0]
    else:
        widget = TextLine(
            " ".join(str(v) for v in values),
            markup=markup,
        )

    # Position the cursor at the start of a new line, taking any docked widgets
    # into account
    term = blessed.Terminal()
    other_docked_widget_remains_below = _docked_widget is not None and not dock

    if other_docked_widget_remains_below:
        stdout.write(term.clear_bol)  # Clear to the start of the line
    elif dock:
        if _docked_widget is not None:
            _docked_widget.on_undock()

        widget.on_dock()
        _docked_widget = widget

        _print_newline()
    else:
        _print_newline()

    # Display the widget
    stdout.write(term.move_x(_start_x))
    widget.draw(term)

    # Re-display the docked widget
    if other_docked_widget_remains_below:
        assert _docked_widget is not None
        _print_newline()
        stdout.write(term.move_x(_start_x))
        _docked_widget.draw(term)

    # Update global state
    _is_first_line = False
    _is_in_new_line = False

    return widget


def _basic_print(prefix: str, values: Iterable[Any], markup: bool) -> None:
    values = " ".join(map(str, values))
    if not markup:
        values = markup_module.escape(values)

    print(f"{prefix}{values}", dock=False)


def success(*values: Any, markup: bool = True) -> None:
    """
    Displays a success message, highlighted to draw attention to it.
    """
    _basic_print("[bold][green]Success:[/bold] ", values, markup)


def warning(*values: Any, markup: bool = True) -> None:
    """
    Displays a warning message, highlighted to draw attention to it.
    """
    _basic_print("[bold][yellow]Warning:[/bold] ", values, markup)


def error(*values: Any, markup: bool = True) -> None:
    """
    Displays an error message, highlighted to draw attention to it.
    """
    _basic_print("[bold][red]Error:[/bold] ", values, markup)


def fatal(*values: Any, status_code: int = 1, markup: bool = True) -> NoReturn:
    """
    Displays an error message, highlighted to draw attention to it, and then
    exits the program.
    """
    _basic_print("[bold][red]ERROR:[/bold] ", values, markup)
    sys.exit(status_code)


def print_chapter(name: Optional[str]) -> None:
    """
    Displays a chapter heading. Chapters are highlighted and create whitespace
    to visually separate them from other widgets.
    """

    global _docked_widget, _is_first_line, _chapter, _is_in_new_line, _start_x

    # Undock any previously docked widgets
    if _docked_widget is not None:
        _docked_widget.on_undock()
        _docked_widget = None

    # Spacing to previous content
    if not _is_first_line:
        _print_newline(1)

    # Print the chapter name
    if name is None:
        _start_x = 0
    else:
        _print_newline(1)
        stdout.write(
            markup_module.unescape(f"[bold blue] > {markup_module.escape(name)}[/]")
        )
        _start_x = 3

    stdout.flush()

    # Update global state
    _chapter = name
    _is_first_line = False
    _is_in_new_line = False


def _secret_input() -> str:
    """
    Get input from `stdin`, displaying an asterisk for each character.
    """
    result = ""
    while True:
        # Get a key
        ch = input_key()

        # Done?
        if ch == "\r" or ch == "\n":
            _print_newline()
            return result

        # Backspace
        if ch == "backspace":
            if result:
                result = result[:-1]
                sys.stdout.write("\b \b")
                sys.stdout.flush()
            continue

        # Ignore other control characters
        if len(ch) > 1:
            continue

        # Print an asterisk
        sys.stdout.write("*")
        sys.stdout.flush()
        result += ch


@typing.overload
def input(
    prompt: str = "",
    *,
    sep: str = " > ",
    parse: Callable[[str], T] = str,
    markup: bool = True,
    secret: bool = False,
) -> T:
    ...


@typing.overload
def input(
    *,
    default: T,
    sep: str = " > ",
    parse: Callable[[str], T] = str,
    markup: bool = True,
    secret: bool = False,
) -> T:
    ...


@typing.overload
def input(
    prompt: str,
    default: T,
    *,
    sep: str = " > ",
    parse: Callable[[str], T] = str,
    markup: bool = True,
    secret: bool = False,
) -> T:
    ...


def input(
    prompt: str = "",
    default: T = _SENTINEL,
    *,
    sep: str = " > ",
    parse: Callable[[str], T] = str,
    markup: bool = True,
    secret: bool = False,
) -> T:
    """
    Asks the user for a value and returns it. If `prompt` is given, it is
    displayed first. `parse` is applied to the user's input, and its result
    returned. If `parse` raises a `ValueError` the user is asked for another
    value. Lastly, if `default` is given, it is returned if the user enters an
    empty string.
    """
    global _is_in_new_line

    # Undock any existing widget
    if _docked_widget is not None:
        _docked_widget.undock()

    # Preprocess the prompt
    if markup:
        prompt = markup_module.unescape(prompt)

    prompt += Fore.BLUE + Format.BOLD + sep + Fore.RESET + Format.RESET_BOLD

    if _chapter is not None:
        prompt = f"   {prompt}"

    # Ask for values, until a valid one comes along
    while True:
        # Get a value
        if secret:
            _print_newline()
            stdin.flush()
            sys.stdout.write(prompt)
            sys.stdout.flush()
            value = _secret_input()
        else:
            _set_echo(True)
            _set_cursor(True)
            _print_newline()
            stdin.flush()
            try:
                value = _py_input(prompt).strip()
            finally:
                _set_echo(False)
                _set_cursor(False)

        # Use the default value?
        if not value and default is not _SENTINEL:
            return default  # type: ignore

        # Try to parse it, thus verifying it's valid
        try:
            value = parse(value)
        except ValueError:
            continue

        # The user has just pressed `enter`, so the cursor is in a new line
        _is_in_new_line = True

        return value


def _display_menu_line(
    term: blessed.Terminal,
    index: int,
    option: str,
    is_selected: bool,
):
    line = f"{index + 1}. {option}  "

    if is_selected:
        line = f"[inverted]{line}[/inverted]"

    sys.stdout.write(term.move_x(_start_x))
    sys.stdout.write(markup_module.unescape(line))


def ask(options: Dict[str, T], *, prompt: str = "") -> T:
    """
    Asks the user to select one of the given options. If `prompt` is given, it
    is displayed first. The options are displayed as a numbered list, and the
    user is asked to select one of them.
    """

    if not options:
        raise ValueError("Please provide at least one option")

    term = blessed.Terminal()

    opt_list = list(options.items())
    n_options = len(options)

    previous_index = 0
    active_index = 0

    # Make sure this is is on a newline
    _print_newline()

    # Display the prompt
    if prompt:
        sys.stdout.write(term.move_x(_start_x))
        sys.stdout.write(markup_module.unescape(prompt))
        sys.stdout.write("\n\n")

    # Display the initial menu
    for index, (name, value) in enumerate(opt_list):
        _display_menu_line(term, index, name, index == active_index)
        sys.stdout.write("\n")

    max_index = min(n_options, 9)
    sys.stdout.write("\n")
    sys.stdout.write(term.move_x(_start_x))
    sys.stdout.write(markup_module.unescape(f"[dim]Use ⇅ or 1-{max_index}[/dim]"))
    sys.stdout.flush()

    # Hand control to the user
    with term.cbreak(), term.hidden_cursor():
        while True:
            # Listen for user inputs
            key = term.inkey()
            if key.name == "KEY_UP" or key == "k":
                previous_index = active_index
                active_index = max(active_index - 1, 0)

            elif key.name == "KEY_DOWN" or key == "j":
                previous_index = active_index
                active_index = min(active_index + 1, n_options - 1)

            elif key.name == "KEY_ENTER":
                sys.stdout.write(term.clear_eol())
                sys.stdout.flush()
                return opt_list[active_index][1]

            else:
                # Handle numbers
                try:
                    number = int(key)
                except ValueError:
                    continue

                if number == 0:
                    number = 10

                if 1 <= number <= n_options:
                    sys.stdout.write(term.clear_eol())
                    sys.stdout.flush()
                    return opt_list[number - 1][1]

                continue

            # Update the display
            if previous_index != active_index:
                # Display the previously selected option
                offset = n_options - previous_index + 1
                sys.stdout.write(term.move_up * offset)
                sys.stdout.write(term.move_x(0))
                sys.stdout.write(term.clear_bol())

                _display_menu_line(
                    term,
                    previous_index,
                    opt_list[previous_index][0],
                    is_selected=False,
                )

                sys.stdout.write(term.move_down * offset)

                # Display the currently selected option
                offset = n_options - active_index + 1
                sys.stdout.write(term.move_up * offset)
                sys.stdout.write(term.move_x(0))
                sys.stdout.write(term.clear_bol())

                _display_menu_line(
                    term,
                    active_index,
                    opt_list[active_index][0],
                    is_selected=True,
                )

                sys.stdout.write(term.move_down * offset)
                sys.stdout.write(term.move_x(0))
                sys.stdout.flush()


def ask_short(
    prompt: str,
    options: Dict[str, Any],
    *,
    default_str: Optional[str] = None,
    add_yes_no_options: bool = False,
) -> Any:
    """
    TODO
    """
    for opt in options.keys():
        assert opt == opt.lower(), opt

    # Prepared, commonly used options
    if add_yes_no_options:
        t = {
            "y": True,
            "yes": True,
            "1": True,
            "t": True,
            "true": True,
            "n": False,
            "no": False,
            "0": False,
            "f": False,
            "false": False,
        }
        t.update(options)
        options = t

    # Make sure the default is valid
    assert default_str is None or default_str == default_str.lower(), default_str
    assert default_str is None or default_str in options, (
        default_str,
        options.keys(),
    )

    # Prepare the option strings for the prompt. There's no point in showing all
    # options, as many map to the same values. Instead, show the first option
    # corresponding to each value, while prioritizing the default option.
    #
    # TODO: This currently requires the returned value to be hashable.
    primary_options = {}
    for opt, value in options.items():
        assert opt == opt.lower(), opt

        if default_str is not None and opt == default_str:
            opt = opt.upper()
            primary_options[value] = opt
        else:
            primary_options.setdefault(value, opt)

    options_string = markup_module.escape("/".join(primary_options.values()))

    # Keep asking until there is a valid response
    while True:
        # Ask for input
        response = input(prompt, sep=f" {options_string} > ").lower()

        if not response and default_str is not None:
            response = default_str

        try:
            return options[response]
        except KeyError:
            pass

        # Ask again if it's invalid
        _print_newline()
        sys.stdout.write(f"Please respond with one of {options_string}")


def ask_yes_no(prompt: str, default_value: Optional[bool] = None) -> bool:
    """
    Displays the prompt to the user, and returns True if the user responds with
    yes, and False if the user responds with no. If no input is entered and a
    default value is provided it is returned instead.

    The function makes a best effort to interpret the user's input, and will
    accept a variety of possible values.
    """
    if default_value is None:
        default_str = None
    elif default_value:
        default_str = "y"
    else:
        default_str = "n"

    return ask_short(
        prompt,
        {},
        default_str=default_str,
        add_yes_no_options=True,
    )


def _set_echo(enable_echo: bool):
    if mode != "terminal" or termios is None:
        return  # TODO

    fd = sys.stdin.fileno()
    (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr(fd)

    if enable_echo:
        lflag |= termios.ECHO
    else:
        lflag &= ~termios.ECHO

    new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    termios.tcsetattr(fd, termios.TCSANOW, new_attr)


def _set_cursor(enable_cursor: bool):
    if mode != "terminal":
        return

    stdout.write("\033[?25h" if enable_cursor else "\033[?25l")
    stdout.flush()


def _on_exit():
    # Clean up the terminal
    if mode == "terminal":
        _set_echo(True)
        _set_cursor(True)
        stdout.write("\n")
        stdout.flush()


atexit.register(_on_exit)
_set_echo(False)
_set_cursor(False)
