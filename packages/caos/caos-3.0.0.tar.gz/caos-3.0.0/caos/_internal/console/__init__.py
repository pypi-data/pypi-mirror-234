from caos._internal.console.ansi_colors import ColorCode as _ColorCode
from caos._internal.console.tools import supports_color as _supports_color
from caos._internal.console.console_art import (
    _LOGO_CAOS_ASCII_SIMPLE,
    _LOGO_CAOS_ASCII_ANSI_COLORS,
    _PROMPT_CAOS_SIMPLE,
    _PROMPT_CAOS_ANSI_COLORS
)


CAOS_CONSOLE_LOGO = _LOGO_CAOS_ASCII_SIMPLE
_CAOS_CONSOLE_PROMPT = _PROMPT_CAOS_SIMPLE
_RED_TEXT = _YELLOW_TEXT = _GREEN_TEXT = _BLUE_TEXT = _GRAY_TEXT = "{text}"
if _supports_color():
    CAOS_CONSOLE_LOGO = _LOGO_CAOS_ASCII_ANSI_COLORS
    _CAOS_CONSOLE_PROMPT = _PROMPT_CAOS_ANSI_COLORS
    _RED_TEXT = _ColorCode.RED + _RED_TEXT + _ColorCode.END
    _YELLOW_TEXT = _ColorCode.YELLOW + _YELLOW_TEXT + _ColorCode.END
    _GREEN_TEXT = _ColorCode.GREEN + _GREEN_TEXT + _ColorCode.END
    _BLUE_TEXT = _ColorCode.BLUE + _BLUE_TEXT + _ColorCode.END
    _GRAY_TEXT = _ColorCode.GRAY + _GRAY_TEXT + _ColorCode.END


def red_text(text: str) -> str:
    return _RED_TEXT.format(text=text)


def yellow_text(text: str) -> str:
    return _YELLOW_TEXT.format(text=text)


def green_text(text: str) -> str:
    return _GREEN_TEXT.format(text=text)


def blue_text(text: str) -> str:
    return _BLUE_TEXT.format(text=text)

def gray_text(text: str) -> str:
    return _GRAY_TEXT.format(text=text)


def caos_command_print(command: str, message: str) -> None:
    print(_CAOS_CONSOLE_PROMPT.format(command=blue_text(command), message=message))


def INFO_MESSAGE(text: str) -> str:
    return gray_text(text="INFO: {}".format(text))

def WARNING_MESSAGE(text: str) -> str:
    return yellow_text(text="WARNING: {}".format(text))

def ERROR_MESSAGE(text: str) -> str:
    return red_text(text="ERROR: {}".format(text))

def SUCCESS_MESSAGE(text: str) -> str:
    return green_text(text="SUCCESS: {}".format(text))