from textwrap import dedent
from types import ModuleType
from caos import __VERSION__
from caos._internal.console import CAOS_CONSOLE_LOGO
from caos._internal.utils.commands import get_commands


def show_help() -> None:
    """"Print the available documentation for the existing commands"""
    _HEADER: str = dedent('''  
        DESCRIPTION
            A simple dependency management tool and tasks executor for Python projects

        PROGRAM INFORMATION
            --help or -h
                Shows documentation about the available arguments and their usage
            --version, -v or -V
                Shows the currently installed version
                
        ARGUMENTS''')

    print(dedent(CAOS_CONSOLE_LOGO)[1:] + (" " * 28) + "v{}".format(__VERSION__))
    print(_HEADER)

    _COMMAMD_HELP_FORMAT: str = dedent('''\
        {COMMAND_NAME}
            Description:
    {COMMAND_DESCRIPTION}                
            Usage Example:\
    ''')

    command_module: ModuleType
    for command_module in get_commands():
        print(_COMMAMD_HELP_FORMAT.format(
            COMMAND_NAME=command_module.NAME.strip(),
            COMMAND_DESCRIPTION=command_module.DESCRIPTION
        ))

        print(command_module.CLI_USAGE_EXAMPLE)