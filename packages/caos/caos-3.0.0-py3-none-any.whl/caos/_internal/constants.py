import os
import re
from enum import Enum
from caos._internal.utils.working_directory import get_current_dir

_CURRENT_DIR = get_current_dir()

DEFAULT_VIRTUAL_ENVIRONMENT_NAME: str = "venv"
VIRTUAL_ENVIRONMENT_NAME_REGEX: str = r"^(\w)+$"
PYTHON_PATH_VENV_POSIX = os.path.abspath(_CURRENT_DIR+"/"+DEFAULT_VIRTUAL_ENVIRONMENT_NAME+"/bin/python")
PYTHON_PATH_VENV_WIN = os.path.abspath(_CURRENT_DIR+"/"+DEFAULT_VIRTUAL_ENVIRONMENT_NAME+"/Scripts/python.exe")
PIP_PATH_VENV_POSIX = os.path.abspath(_CURRENT_DIR+"/"+DEFAULT_VIRTUAL_ENVIRONMENT_NAME+"/bin/pip")
PIP_PATH_VENV_WIN = os.path.abspath(_CURRENT_DIR+"/"+DEFAULT_VIRTUAL_ENVIRONMENT_NAME+"/Scripts/pip.exe")

CAOS_YAML_FILE_NAME = "caos.yml"


class ValidDependencyVersionRegex(Enum):
    MAJOR_MINOR_PATCH = re.compile(r"^(?P<update_type>(\^|\~))?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")  # (^| ~) X.X.X
    MAJOR_MINOR = re.compile(r"^(?P<update_type>(\^|\~))?(?P<major>\d+)\.(?P<minor>\d+)$")  # (^| ~) X.X
    MAJOR = re.compile(r"^(?P<update_type>(\^|\~))?(?P<major>\d+)$")  # (^| ~) X
    LATEST = re.compile(r"^(latest|LATEST)$")  # latest or LATEST
    WHEEL = re.compile(r"^(?P<wheel>((.+?)-(?P<version>.*?)))((-(\d[^-]*?))?-(.+?)-(.+?)-(.+?))(\.whl|\.dist-info)$")
    TARGZ = re.compile(r"^(.*)(.tar.gz)$")
