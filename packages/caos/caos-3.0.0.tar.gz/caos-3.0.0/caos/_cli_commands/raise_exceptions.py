from caos._internal.constants import CAOS_YAML_FILE_NAME
from caos._internal.exceptions import MissingYamlException, MissingBinaryException, MissingVirtualEnvironmentException


def raise_missing_yaml_exception() -> None:
    raise MissingYamlException(
        "No '{}' file found. Try running first 'caos init'".format(CAOS_YAML_FILE_NAME)
    )


def raise_missing_virtual_environment_exception(env_name: str) -> None:
    raise MissingVirtualEnvironmentException(
        "No virtual environment '{}' could be found. "
        "Try running first 'caos init'".format(env_name)
    )


def raise_missing_pip_binary_exception(env_name: str) -> None:
    raise MissingBinaryException(
        "The virtual environment does not have a 'pip' binary. "
        "Try deleting the folder '{}' and run 'caos init'".format(env_name)
    )


def raise_missing_python_binary_exception(env_name: str) -> None:
    raise MissingBinaryException(
        "The virtual environment does not have a 'python' binary. "
        "Try deleting the folder '{}' and run 'caos init'".format(env_name)
    )