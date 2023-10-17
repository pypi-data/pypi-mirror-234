import argparse
import json
from json import JSONDecodeError
from typing import Any

from unstract_sdk.tools import UnstractToolUtils


def run(
    params: dict[str, Any],
    settings: dict[str, Any],
    project_guid: str,
    utils: UnstractToolUtils,
) -> None:
    MOUNTED_FSSPEC_DIR_INPUT = "/mnt/unstract/fs_input/"  # noqa: F841
    MOUNTED_FSSPEC_DIR_OUTPUT = "/mnt/unstract/fs_output/"  # noqa: F841
    # -------------- TODO: Add your code here ----------------
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", type=str, help="Command to execute", required=True)
    parser.add_argument(
        "--params", type=str, help="Parameters to use in RUN command", required=False
    )
    parser.add_argument(
        "--settings", type=str, help="Settings to be used", required=False
    )
    parser.add_argument("--project-guid", type=str, help="Project GUID", required=False)
    parser.add_argument(
        "--log-level", type=str, help="Log level", required=False, default="ERROR"
    )
    args = parser.parse_args()
    command = str.upper(args.command)

    unstract_tools_util = UnstractToolUtils(args.log_level)

    if command == "SPEC" or command == "PROPERTIES" or command == "ICON":
        unstract_tools_util.handle_static_command(command)
    elif command == "RUN":
        if args.params is None:
            unstract_tools_util.stream_log(
                "--params are required for RUN command", "ERROR"
            )
            exit(1)
        try:
            params = json.loads(args.params)
        except JSONDecodeError:
            unstract_tools_util.stream_log("Params are not valid JSON", "ERROR")
            exit(1)

        if args.settings is None:
            unstract_tools_util.stream_log(
                "--settings are required for RUN command", "ERROR"
            )
            exit(1)
        try:
            print(args.settings)
            settings = json.loads(args.settings)
        except JSONDecodeError:
            unstract_tools_util.stream_log("Settings are not valid JSON", "ERROR")
            exit(1)

        if args.project_guid is None:
            unstract_tools_util.stream_log(
                "--project-guid is required for RUN command", "ERROR"
            )
            exit(1)

        run(params, settings, args.project_guid, unstract_tools_util)
    else:
        unstract_tools_util.stream_log("Command not supported", "ERROR")
        exit(1)
