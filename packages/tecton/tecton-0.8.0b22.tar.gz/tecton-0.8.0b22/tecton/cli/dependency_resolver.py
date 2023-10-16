import os
import subprocess
import sys
import tempfile
from typing import List


PYTHON_VERSION_TO_PLATFORM = {
    "3.8": "manylinux_2_17_x86_64-cp-3.8.17-cp38",
    "3.9": "manylinux_2_17_x86_64-cp-3.9.17-cp39",
}

MISSING_REQUIREMENTS_ERROR = "Could not find a version that satisfies the requirement"
ENSURE_WHEELS_EXIST_WARNING = "Please also ensure that the package(s) have wheels (.whl) available for download in PyPI or any other repository used."


def resolve_dependencies(
    requirements_path: str, resolved_requirements_path: str, python_version: str, timeout_seconds: int
):
    """Resolve dependencies using `pex`
    Parameters:
        requirements_path(str): Path to the `requirements.txt` file
        resolved_requirements_path(str): The target path for generating the fully resolved and pinned `resolved-requirements.txt` file
        python_version(str): The python version to resolve dependencies for
        timeout_seconds(int): The timeout in seconds for the dependency resolution
    """
    if python_version not in PYTHON_VERSION_TO_PLATFORM:
        msg = f"Invalid `python_version` {python_version}. Expected one of: {list(PYTHON_VERSION_TO_PLATFORM.keys())}"
        raise ValueError(msg)
    platform = PYTHON_VERSION_TO_PLATFORM[python_version]
    with tempfile.TemporaryDirectory() as tmpdir:
        intermediate_output_path = os.path.join(tmpdir, "output")
        lock_command = _construct_lock_command(
            requirements_path=requirements_path, target_path=intermediate_output_path, platform=platform
        )
        export_command = _construct_export_command(
            target_path=intermediate_output_path,
            resolved_requirements_path=resolved_requirements_path,
            platform=platform,
        )
        _run_pex_command(command_list=lock_command, timeout_seconds=timeout_seconds)
        _run_pex_command(command_list=export_command, timeout_seconds=timeout_seconds)


def _run_pex_command(command_list: List[str], timeout_seconds: int):
    """Run the `pex` command passed as input and process any errors
    Parameters:
        command(str): The pex command to be executed
        timeout_seconds(int): The timeout in seconds for the pex command
    """
    command = [sys.executable, "-m", "tecton.cli.pex_wrapper", *command_list]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        error_message = (
            "Dependency Resolution timed out! If problem persists, please contact Tecton Support for assistance"
        )
        raise TimeoutError(error_message)
    if result.stderr:
        error_message = _parse_pex_error(result.stderr)
        raise ValueError(error_message)


def _construct_lock_command(requirements_path: str, target_path: str, platform: str) -> List[str]:
    return [
        "lock",
        "create",
        "-r",
        requirements_path,
        "--no-build",
        "--style=strict",
        "-o",
        target_path,
        "--platform",
        platform,
    ]


def _construct_export_command(target_path: str, resolved_requirements_path: str, platform: str) -> List[str]:
    return ["lock", "export", "--platform", platform, target_path, "--output", resolved_requirements_path]


def _parse_pex_error(error_string: str) -> str:
    """Parse and cleanup error messages from the `pex` command"""
    start_index = error_string.find("ERROR:")
    if start_index != -1:
        error_string = error_string[start_index:].replace("\n", " ")
    # The pex error message does not clarify that wheels must be present and so we append it to the original error message
    if MISSING_REQUIREMENTS_ERROR in error_string:
        error_string = f"{error_string}\n\n💡 {ENSURE_WHEELS_EXIST_WARNING}"
    return error_string
