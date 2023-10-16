import os
import sys
import subprocess
from io import StringIO
from typing import List
from caos._internal.types import ExitCode
from caos._internal.utils.yaml import get_virtual_environment_from_yaml
from caos._internal.utils.working_directory import get_current_dir
from caos._internal.utils.os import is_posix_os, is_win_os
from caos._internal.utils.yaml import get_dependencies_from_yaml, Dependencies
from caos._internal.console import caos_command_print, INFO_MESSAGE, WARNING_MESSAGE, SUCCESS_MESSAGE, ERROR_MESSAGE
from caos._internal.constants import (
    CAOS_YAML_FILE_NAME, DEFAULT_VIRTUAL_ENVIRONMENT_NAME,
    PIP_PATH_VENV_WIN, PIP_PATH_VENV_POSIX,
    PYTHON_PATH_VENV_WIN, PYTHON_PATH_VENV_POSIX
)
from caos._cli_commands.raise_exceptions import (
    raise_missing_yaml_exception,
    raise_missing_virtual_environment_exception,
    raise_missing_pip_binary_exception,
    raise_missing_python_binary_exception
)

from .constants import NAME


def main(args: List[str]) -> ExitCode:
    current_dir: str = get_current_dir()
    if not os.path.isfile(os.path.abspath(current_dir + "/" + CAOS_YAML_FILE_NAME)):
        raise_missing_yaml_exception()

    venv_name: str = get_virtual_environment_from_yaml()

    if not os.path.isdir(os.path.abspath(current_dir + "/" + venv_name)):
        raise_missing_virtual_environment_exception(env_name=venv_name)

    if is_win_os():
        pip_path: str = PIP_PATH_VENV_WIN.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, venv_name)
        python_path: str = PYTHON_PATH_VENV_WIN.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, venv_name)
    elif is_posix_os():
        pip_path: str = PIP_PATH_VENV_POSIX.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, venv_name)
        python_path: str = PYTHON_PATH_VENV_POSIX.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, venv_name)

    if not os.path.isfile(pip_path):
        raise_missing_pip_binary_exception(env_name=venv_name)
    if not os.path.isfile(python_path):
        raise_missing_python_binary_exception(env_name=venv_name)

    if args:
        caos_command_print(
            command=NAME,
            message=WARNING_MESSAGE("The update command does not support arguments")
        )

    dependencies: Dependencies = get_dependencies_from_yaml()

    is_unittest: bool = True if isinstance(sys.stdout, StringIO) else False

    if "pip" in dependencies:
        if "pip" == dependencies.get("pip")["pip_ready_version"]:
            dep: str = "pip"
        else:
            dep: str = "pip{}".format(dependencies.get("pip")["pip_ready_version"])

        caos_command_print(
            command=NAME,
            message=INFO_MESSAGE("Updating PIP...")
        )

        del dependencies["pip"]

        install_pip_process: subprocess.CompletedProcess = subprocess.run(
            [python_path, "-m", "pip", "install", "--force-reinstall", dep],
            stdout=subprocess.PIPE if is_unittest else sys.stdout,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        if install_pip_process.returncode != 0:
            caos_command_print(
                command=NAME,
                message=WARNING_MESSAGE("PIP could not be updated")
            )
        else:
            caos_command_print(
                command=NAME,
                message=SUCCESS_MESSAGE("PIP was successfully updated")
            )

    if not dependencies:
        caos_command_print(
            command=NAME,
            message=INFO_MESSAGE("No dependencies to install")
        )
        return ExitCode(0)

    deps: List[str] = []
    for dep_name, dep_version in dependencies.items():
        if dep_name == dep_version["pip_ready_version"]:
            dep = dep_name
        elif dep_version["pip_ready_version"].endswith(".whl") or dep_version["pip_ready_version"].endswith(".dist-info") or dep_version["pip_ready_version"].endswith(".tar.gz"):
            dep = dep_version["pip_ready_version"]
        else:
            dep = "{}{}".format(dep_name, dep_version["pip_ready_version"])

        deps.append(dep)

    caos_command_print(
        command=NAME,
        message=INFO_MESSAGE("Installing dependencies...")
    )

    install_deps_process: subprocess.CompletedProcess = subprocess.run(
        [python_path, "-m", "pip", "install", "--force-reinstall"] + deps,
        stdout=subprocess.PIPE if is_unittest else sys.stdout,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    if install_deps_process.returncode != 0:
        caos_command_print(
            command=NAME,
            message=ERROR_MESSAGE("It was not possible to install the dependencies")
        )

        return ExitCode(install_deps_process.returncode)

    caos_command_print(
        command=NAME,
        message=SUCCESS_MESSAGE("All dependencies have been installed")
    )

    return ExitCode(0)
