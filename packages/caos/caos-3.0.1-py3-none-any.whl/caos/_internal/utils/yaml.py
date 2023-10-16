import os
import re
from caos._third_party.pyyaml_5_3_1 import yaml
from caos._internal.constants import CAOS_YAML_FILE_NAME, VIRTUAL_ENVIRONMENT_NAME_REGEX
from caos._internal.utils.working_directory import get_current_dir
from caos._internal.utils.dependencies import generate_pip_ready_dependency
from caos._internal.exceptions import (
    OpenCaosFileException, InvalidCaosFileFormat, MissingKeyInYamlFile,
    WrongKeyTypeInYamlFile, InvalidVirtualEnvironmentFormat
)

from typing import List, Dict, Any

Dependencies = Dict[str, Dict[str, str]]
_TasksYaml = Dict[Any, List[str]]
Tasks = Dict[str, List[str]]


class CaosYaml:
    virtual_environment: str
    dependencies: Dependencies
    tasks: Tasks


def read_caos_yaml() -> CaosYaml:
    """
    Raises:
        OpenCaosFileException
        InvalidCaosFileFormat
    """
    try:
        yaml_path: str = os.path.abspath(get_current_dir() + "/" + CAOS_YAML_FILE_NAME)
        with open(file=yaml_path, mode="r") as caos_file:
            caos_file_content: str = caos_file.read()
    except Exception as e:
        raise OpenCaosFileException(str(e))

    try:
        caos_yaml: CaosYaml = yaml.load(stream=caos_file_content, Loader=yaml.FullLoader)
    except RecursionError as e:
        raise RecursionError("Maximum recursion depth exceeded")
    except Exception as e:
        raise InvalidCaosFileFormat("The file does not contain valid YAML syntax: " + str(e))

    return caos_yaml


def get_virtual_environment_from_yaml() -> str:
    """
    Raises:
        OpenCaosFileException
        InvalidCaosFileFormat
        WrongKeyTypeInYamlFile
        InvalidVirtualEnvironmentFormat
    """
    caos_yaml: CaosYaml = read_caos_yaml()
    if "virtual_environment" not in caos_yaml:
        raise MissingKeyInYamlFile(
            "The 'virtual_environment' key is not present in the '{}' file".format(CAOS_YAML_FILE_NAME)
        )

    virtual_environment: str = caos_yaml.get("virtual_environment")

    if not isinstance(virtual_environment, str):
        raise WrongKeyTypeInYamlFile("The 'virtual_environment' key must be a string")

    if not re.match(pattern=VIRTUAL_ENVIRONMENT_NAME_REGEX, string=virtual_environment):
        raise InvalidVirtualEnvironmentFormat(
            "\nThe virtual environment name must be a string of alphanumeric characters."
            "\nInvalid characters include: '`\".,;:+-~!@#$%^&*()<>=?"
        )

    return virtual_environment


def get_dependencies_from_yaml() -> Dependencies:
    """
    Raises:
        OpenCaosFileException
        InvalidCaosFileFormat
        WrongKeyTypeInYamlFile
        InvalidDependencyVersionFormat
        UnexpectedError
    """
    caos_yaml: CaosYaml = read_caos_yaml()
    if "dependencies" not in caos_yaml:
        raise MissingKeyInYamlFile(
            "The 'dependencies' key is not present in the '{}' file".format(CAOS_YAML_FILE_NAME)
        )

    dependencies: Dependencies = caos_yaml.get("dependencies")

    if not isinstance(dependencies, dict):
        raise WrongKeyTypeInYamlFile("The 'dependencies' key must be a dictionary")

    result_dependencies: Dependencies = {}
    for dependency_name, version in dependencies.items():
        result_dependencies[str(dependency_name).lower()] = {
            "pip_ready_version": generate_pip_ready_dependency(dependency_name, version),
            "user_requested_version": version
        }

    return result_dependencies


def get_tasks_from_yaml() -> Tasks:
    """
    Raises:
        OpenCaosFileException
        InvalidCaosFileFormat
        WrongKeyTypeInYamlFile
        UnexpectedError
    """
    caos_yaml: CaosYaml = read_caos_yaml()
    if "tasks" not in caos_yaml:
        raise MissingKeyInYamlFile(
            "The 'tasks' key is not present in the '{}' file".format(CAOS_YAML_FILE_NAME)
        )

    tasks: _TasksYaml = caos_yaml.get("tasks")

    if not isinstance(tasks, dict):
        raise WrongKeyTypeInYamlFile("The 'tasks' key must be a dictionary")

    result_tasks: Tasks = {}
    for task_name, list_of_steps in tasks.items():
        if not isinstance(list_of_steps, list):
            raise WrongKeyTypeInYamlFile("The task '{}' must contain a list of steps to execute".format(task_name))

        result_tasks[str(task_name)] = [str(step) for step in list_of_steps]

    return result_tasks
