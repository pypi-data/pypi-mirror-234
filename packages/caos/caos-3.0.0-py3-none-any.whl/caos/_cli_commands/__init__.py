"""
DO NOT TOUCH
    This script imports all the modules available that start with the word 'command'
"""

import os.path
import pkgutil as _pkgutil
from typing import List
from caos import _cli_commands

available_commands: List[str] = []


_module_info: _pkgutil.ModuleInfo
for _module_info in _pkgutil.iter_modules(path=[os.path.dirname(_cli_commands.__file__)]):
    module_name: str = _module_info.name

    if module_name.startswith("command"):
        available_commands.append(module_name)
