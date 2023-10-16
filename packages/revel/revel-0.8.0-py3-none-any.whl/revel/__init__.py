import colorama

from .legacy import *
from .style import *
from .markup import unescape, GLOBAL_STYLES

colorama.init()

__all__ = [
    "print",
    "print_chapter",
    "warning",
    "error",
    "fatal",
    "input",
    "ask",
    "ask_short",
    "ask_yes_no",
]
