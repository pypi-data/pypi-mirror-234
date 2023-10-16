import sys
from types import ModuleType
from caos._internal.types import ExitCode
from caos._internal.utils.os import is_supported_os
from caos._cli_commands import help_command, version_command
from caos._internal.utils.commands import get_command
from caos._internal.console import caos_command_print, ERROR_MESSAGE


def cli_entry_point() -> ExitCode:
    """CLI entry point that calls the required commands specified by the user """
    if not is_supported_os():
        caos_command_print(command="OS Check", message=ERROR_MESSAGE("Only Windows and UNIX Like OSs are supported"))
        return ExitCode(1)

    if not sys.argv[1:]:
        caos_command_print(
            command="none",
            message=ERROR_MESSAGE("No argument given, if you need help try typing 'caos --help'")
        )
        return ExitCode(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command in ("--help", "-h"):
        help_command.show_help()

    elif command in ("--version", "-v", "-V"):
        version_command.show_version()

    else:
        requested_command: ModuleType = get_command(command=command)
        if not requested_command:
            caos_command_print(
                command=command,
                message=ERROR_MESSAGE("Unknown argument, if you need help try typing 'caos --help'")
            )
            return ExitCode(1)

        try:
            return ExitCode(requested_command.entry_point(args=args))
        except Exception as e:
            caos_command_print(command=command, message=ERROR_MESSAGE("<<{}>> {}".format(type(e).__name__, str(e))))
            return ExitCode(1)

    return ExitCode(0)
