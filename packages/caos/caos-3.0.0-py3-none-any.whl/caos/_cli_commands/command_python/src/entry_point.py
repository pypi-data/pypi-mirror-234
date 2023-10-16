import os
import sys
import subprocess
from io import StringIO
from typing import List
from caos._internal.types import ExitCode
from caos._internal.utils.yaml import get_virtual_environment_from_yaml
from caos._internal.utils.working_directory import get_current_dir
from caos._internal.utils.os import is_posix_os, is_win_os
from caos._internal.constants import (
    CAOS_YAML_FILE_NAME, DEFAULT_VIRTUAL_ENVIRONMENT_NAME,
    PYTHON_PATH_VENV_WIN, PYTHON_PATH_VENV_POSIX
)
from caos._cli_commands.raise_exceptions import (
    raise_missing_yaml_exception,
    raise_missing_virtual_environment_exception,
    raise_missing_python_binary_exception
)


def main(args: List[str]) -> ExitCode:
    current_dir: str = get_current_dir()
    if not os.path.isfile(os.path.abspath(current_dir + "/" + CAOS_YAML_FILE_NAME)):
        raise_missing_yaml_exception()

    venv_name: str = get_virtual_environment_from_yaml()

    if not os.path.isdir(os.path.abspath(current_dir + "/" + venv_name)):
        raise_missing_virtual_environment_exception(env_name=venv_name)

    if is_win_os():
        python_path: str = PYTHON_PATH_VENV_WIN.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, venv_name)
    elif is_posix_os():
        python_path: str = PYTHON_PATH_VENV_POSIX.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, venv_name)

    if not os.path.isfile(python_path):
        raise_missing_python_binary_exception(env_name=venv_name)

    # The current Unittest for this redirects the stdout to a StringIO() buffer, which is not compatible with
    # subprocess, so for this scenario a subprocess.PIPE is used instead of the sys.stdout to be able to capture
    # the output in the unittests
    is_unittest: bool = True if isinstance(sys.stdout, StringIO) else False
    python_process: subprocess.CompletedProcess = subprocess.run(
        [python_path] + args,
        stdout=subprocess.PIPE if is_unittest else sys.stdout,
        stderr=subprocess.STDOUT,
        stdin=sys.stdin,
        universal_newlines=True
    )

    if is_unittest and python_process.stdout:
        print(python_process.stdout)

    return ExitCode(python_process.returncode)
