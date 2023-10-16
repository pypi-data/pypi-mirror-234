import os


def is_win_os() -> bool:
    return os.name == "nt"


def is_posix_os() -> bool:
    return os.name == "posix"


def is_supported_os() -> bool:
    return is_win_os() or is_posix_os()