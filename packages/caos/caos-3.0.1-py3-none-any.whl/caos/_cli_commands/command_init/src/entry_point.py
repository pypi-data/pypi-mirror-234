import os
import re
import sys
import subprocess
from typing import List
from caos._internal.types import ExitCode
from caos._internal.utils.working_directory import get_current_dir
from caos._internal.utils.yaml import get_virtual_environment_from_yaml
from caos._internal.utils.os import is_posix_os, is_win_os
from caos._internal.console import caos_command_print, INFO_MESSAGE, WARNING_MESSAGE, SUCCESS_MESSAGE
from caos._internal.exceptions import InvalidVirtualEnvironmentFormat, MissingBinaryException
from caos._internal.constants import (
    CAOS_YAML_FILE_NAME, DEFAULT_VIRTUAL_ENVIRONMENT_NAME, VIRTUAL_ENVIRONMENT_NAME_REGEX,
    PYTHON_PATH_VENV_WIN, PYTHON_PATH_VENV_POSIX, PIP_PATH_VENV_WIN, PIP_PATH_VENV_POSIX
)
from caos._cli_commands.raise_exceptions import raise_missing_python_binary_exception
from .exceptions import CreateVirtualEnvironmentException, OverrideYamlConfigurationException
from .constants import NAME, _CAOS_YAML_TEMPLATE, _CAOS_YAML_TEMPLATE_SIMPLE


def create_caos_yaml(current_dir: str, env_name: str, caos_yaml_template: str = None):
    """
    Raises:
        InvalidVirtualEnvironmentFormat
        OpenCaosFileException
        InvalidCaosFileFormat
        WrongKeyTypeInYamlFile
        InvalidVirtualEnvironmentFormat
        OverrideYamlConfigurationException
    """
    if not caos_yaml_template:
        caos_yaml_template = _CAOS_YAML_TEMPLATE
    caos_yml_path: str = os.path.abspath(current_dir + "/" + CAOS_YAML_FILE_NAME);
    if os.path.isfile(caos_yml_path):
        env_name_in_yaml = get_virtual_environment_from_yaml()

        if env_name and env_name != env_name_in_yaml:
            raise OverrideYamlConfigurationException(
                "To use a different virtual environment edit the respective key within the '{CAOS_YAML}' file "
                "and then execute 'caos init' "
                    .format(CAOS_YAML=CAOS_YAML_FILE_NAME)
            )

        caos_command_print(
            command=NAME,
            message=INFO_MESSAGE("The '{CAOS_YAML}' file already exists".format(CAOS_YAML=CAOS_YAML_FILE_NAME))
        )
        return

    caos_command_print(command=NAME, message=INFO_MESSAGE("Creating '{CAOS_YAML}'...").format(CAOS_YAML=CAOS_YAML_FILE_NAME))

    if not env_name:
        env_name = DEFAULT_VIRTUAL_ENVIRONMENT_NAME

    if not re.match(pattern=VIRTUAL_ENVIRONMENT_NAME_REGEX, string=env_name):
        raise InvalidVirtualEnvironmentFormat(
            "\nThe virtual environment name must be a string of alphanumeric characters."
            "\nInvalid characters include: '`\".,;:+-~!@#$%^&*()<>=?"
        )

    with open(file=caos_yml_path, mode="w") as caos_yml_file:
        caos_yml_file.write(
            caos_yaml_template.format(VENV_NAME=env_name)
        )

    caos_command_print(
        command=NAME,
        message=SUCCESS_MESSAGE("'{CAOS_YAML}' created".format(CAOS_YAML=CAOS_YAML_FILE_NAME))
    )
    return


def create_virtual_env(current_dir:str):
    """
    Raises:
        OpenCaosFileException
        InvalidCaosFileFormat
        WrongKeyTypeInYamlFile
        CreateVirtualEnvironmentException
        MissingBinaryException
    """
    env_name = get_virtual_environment_from_yaml()
    env_path : str = os.path.abspath(current_dir + "/" + env_name);
    if os.path.isdir(env_path):
        caos_command_print(
            command=NAME,
            message=INFO_MESSAGE("The virtual environment already exists so a new one won't be created")
        )

    else:
        caos_command_print(command=NAME, message=INFO_MESSAGE("Creating a new virtual environment..."))
        create_env_process: subprocess.CompletedProcess = subprocess.run(
            [sys.executable, "-m", DEFAULT_VIRTUAL_ENVIRONMENT_NAME, os.path.abspath(get_current_dir()+"/"+env_name)],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True
        )

        if create_env_process.returncode != 0:
            raise CreateVirtualEnvironmentException(create_env_process.stderr)

        caos_command_print(command=NAME, message=SUCCESS_MESSAGE("A new virtual environment was created"))

    if is_win_os():
        pip_path: str = PIP_PATH_VENV_WIN.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, env_name)
        python_path: str = PYTHON_PATH_VENV_WIN.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, env_name)

    if is_posix_os():
        pip_path: str = PIP_PATH_VENV_POSIX.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, env_name)
        python_path: str = PYTHON_PATH_VENV_POSIX.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, env_name)

    if not os.path.isfile(pip_path):
        caos_command_print(
            command=NAME,
            message=WARNING_MESSAGE("The virtual environment does not have a 'pip' binary")
        )

    if not os.path.isfile(python_path):
        raise_missing_python_binary_exception(env_name=env_name)


def main(args: List[str]) -> ExitCode:
    virtual_env_name: str = args[0] if len(args) >= 1 else None
    current_dir: str = get_current_dir()

    simple_yaml_template = None
    simple_init_args= ('--simple', '-s', '-S')
    if virtual_env_name in simple_init_args:
        simple_yaml_template = _CAOS_YAML_TEMPLATE_SIMPLE
        virtual_env_name = None
    create_caos_yaml(current_dir=current_dir, env_name=virtual_env_name, caos_yaml_template=simple_yaml_template)
    if not simple_yaml_template:
        create_virtual_env(current_dir=current_dir)
    return ExitCode(0)