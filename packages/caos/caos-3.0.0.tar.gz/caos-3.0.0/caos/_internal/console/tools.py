import re
import sys
from caos._internal.utils.os import is_posix_os, is_win_os
from caos._third_party.colorama_0_4_3 import load_colorama


def supports_color() -> bool:
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    supported_platform = is_posix_os() or (is_win_os() and load_colorama())
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()  # isatty is not always present
    return supported_platform and is_a_tty


def escape_ansi(line) -> str:
    """
    Returns a string without ansi color codes
    """
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)



