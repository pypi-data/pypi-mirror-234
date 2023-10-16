from importlib import import_module
from typing import List
from types import ModuleType
from caos._cli_commands import available_commands


def get_commands() -> List[ModuleType]:
    """Get a list of all commands available for caos to use"""
    modules:  List[ModuleType] = []
    command_name: str
    for command_name in available_commands:
        modules.append(import_module("caos._cli_commands.{}".format(command_name)))
    return modules


def get_command(command: str) -> ModuleType:
    command_module: ModuleType
    for command_module in get_commands():
        if command == command_module.NAME:
            return command_module
    return None
