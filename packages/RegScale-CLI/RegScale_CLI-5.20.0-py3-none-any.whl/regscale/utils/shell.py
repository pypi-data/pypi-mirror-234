"""Define methods for use with CLI operations."""
from subprocess import (
    check_output,
    Popen,
    PIPE,
    run,
    CalledProcessError,
)
from typing import Union
from pprint import pprint
from shlex import split as shlexsplit


def strbyte(string: str, encoding: str = "utf-8") -> bytes:
    """Convert a string to bytes

    String will have `\n` append and converted to encoding.

    :param string: the string to convert to bytes
    :param encoding: the encoding to use
    :return: a bytes object
    """
    if not string.endswith("\n"):
        string += "\n"
    return bytes(string, encoding=encoding)


# FIXME - this was useful early on -- will any of this be useful once the SDK is in-place?
def send_input_to_process_via_communicate(
    process: Popen,
    input_: str,
    encoding: str = "utf-8",
) -> tuple:
    """Send an input string to a process

    When passed a Popen process, send the input as an encoded bytes

    :param process: the Popen process
    :param input_: a string to send to the process
    :param encoding: specify the encoding
    :return: a tuple of stdout, stderr
    """
    return process.communicate(strbyte(string=input_, encoding=encoding))


def run_command(
    cmd: Union[str, list],
) -> bool:
    """Run a shell command

    Use python subprocess to run a command.

    :param cmd: a list or string of commands to execute
    :return: a bool indicating success or failure
    """
    if isinstance(cmd, str):
        cmd = shlexsplit(cmd)
    try:
        run(cmd, check=True, stdout=PIPE, stderr=PIPE)
        return True
    except CalledProcessError as exc:
        print(
            f"Command '{' '.join(cmd)}' returned with error (code {exc.returncode}): {exc.output.decode()}"
        )
        raise exc


def run_command_and_store_output(
    cmd: Union[str, list],
    output: bool = False,
) -> str:
    """Run a shell command and store the output

    Runs a simple shell command and stores the output as a string.

    :param cmd: a list or string of commands
    :param output: should pprint be used to display, defaults to False
    :return: A string of the command output
    """
    if isinstance(cmd, list):
        cmd = " ".join(cmd)
    cmd_output = check_output(cmd, shell=True, text=True)
    if output:
        pprint(f"Command output:\n{cmd_output}")
    return cmd_output


def send_input_to_process(
    process: Popen,
    input_: str,
) -> None:
    """Send an input string to a process

    When passed a Popen process, send the input as an encoded bytes

    :param process: the Popen process
    :param input_: a string to send to the process
    """
    process.stdin.write(input_)
    process.stdin.flush()


def run_command_interactively(
    cmd: Union[str, list],
    inputs: Union[str, list],
    output: bool = False,
    include_error: bool = False,
) -> str:
    """Run a command by sending inputs

    Runs a shell command and send inputs to it

    :param cmd: the initial command to invoke
    :param inputs: a single str of inputs or a list to pass to the
                   command interactively
    :param output: should output be pprinted? defaults to False
    :param include_error: should error be output as well?, default False
    :return: A string of the command output
    """
    if isinstance(cmd, list):
        cmd = " ".join(cmd)

    process = Popen(shlexsplit(cmd), stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)

    if isinstance(inputs, str):
        inputs = [inputs]

    for input_ in inputs:
        send_input_to_process(process=process, input_=input_)

    stdout, stderr = process.communicate()
    output_std = stdout or ""
    output_err = stderr or ""

    if output:
        pprint(output_std)
        if include_error:
            pprint(output_err)

    result = output_std
    if include_error:
        result += "\n" + output_err
    return result
