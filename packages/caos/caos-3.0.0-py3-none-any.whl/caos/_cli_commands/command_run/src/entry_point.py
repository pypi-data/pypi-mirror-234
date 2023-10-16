import os
import sys
import ast
import subprocess
from io import StringIO
from typing import List
from caos._internal.types import ExitCode
from caos._internal.utils.working_directory import get_current_dir
from caos._internal.utils.os import is_win_os
from caos._internal.utils.yaml import get_tasks_from_yaml, Tasks
from caos._internal.constants import CAOS_YAML_FILE_NAME
from caos._internal.exceptions import MissingYamlException
from caos._internal.console import caos_command_print, WARNING_MESSAGE
from .exceptions import MissingTaskArgument, TaskNotFound, StepExecutionError
from .constants import NAME


def main(args: List[str], cwd_step: str = None, env_step: dict = None) -> ExitCode:
    current_dir: str = get_current_dir()
    if not os.path.isfile(os.path.abspath(current_dir + "/" + CAOS_YAML_FILE_NAME)):
        raise MissingYamlException("No '{}' file found. Try running first 'caos init'".format(CAOS_YAML_FILE_NAME))

    if len(args) < 1:
        raise MissingTaskArgument("No task name to execute was given")

    task_name: str = args[0]

    available_tasks: Tasks = get_tasks_from_yaml()

    if not task_name in available_tasks:
        raise TaskNotFound("No task named '{}' was found".format(task_name))

    if len(args) > 1:
        caos_command_print(
            command=NAME,
            message=WARNING_MESSAGE("The tasks can't receive arguments")
        )

    steps: List[str] = available_tasks[task_name]

    caos_context_env_file = ".caos_context_env_file.tmp"

    caos_context_env_command = \
        f"import os;" + \
        f"os.environ['_CAOS_CWD'] = os.getcwd();" + \
        f"file = open(r'{os.path.abspath(os.getcwd()+'/'+caos_context_env_file)}', 'w');" + \
        f"file.write(str(dict(os.environ)));" + \
        f"file.close();"

    added_caos_commands = f'{sys.executable} -c "{caos_context_env_command}"'

    is_unittest: bool = True if isinstance(sys.stdout, StringIO) else False

    for step in steps:
        if step in available_tasks:
            main(args=[step], cwd_step=cwd_step, env_step=env_step)
            continue

        # The current Unittest for this redirects the stdout to a StringIO() buffer, which is not compatible with
        # subprocess, so for this scenario a subprocess.PIPE is used instead of the sys.stdout to be able to capture
        # the output in the unittests
        step_process: subprocess.CompletedProcess = subprocess.run(
            f"{step} && {added_caos_commands}",
            stdout=subprocess.PIPE if is_unittest else sys.stdout,
            stderr=subprocess.STDOUT,
            stdin=sys.stdin,
            cwd=cwd_step,
            env=env_step,
            universal_newlines=True,
            shell=True
        )

        if is_unittest and step_process.stdout:
            print(step_process.stdout)

        if step_process.returncode != 0:
            if os.path.isfile(caos_context_env_file):
                os.remove(caos_context_env_file)
            raise StepExecutionError("Within the task '{}' the step '{}' returned a non zero exit code"
                                     .format(task_name, step))

        if os.path.isfile(caos_context_env_file):
            if is_win_os():
                os.system(f"attrib +h {caos_context_env_file}")

            with open(caos_context_env_file, 'r') as f:
                env_step = ast.literal_eval(f.read())
                cwd_step = env_step["_CAOS_CWD"]

            os.remove(caos_context_env_file)

    return ExitCode(0)
