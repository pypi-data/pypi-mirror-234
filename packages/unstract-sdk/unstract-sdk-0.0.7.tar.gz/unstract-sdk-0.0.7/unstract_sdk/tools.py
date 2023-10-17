import datetime
import json
import os
from hashlib import md5
from typing import Any


class UnstractToolUtils:
    """Utility class for Unstract tools.

    A utility class to make writing Unstract tools easier. It provides
    methods to return the JSON schema, properties, icon, and log
    messages. It also provides methods to stream the JSON schema,
    properties, icon, log messages, cost, single step messages, and
    results using the Unstract protocol to stdout.
    """

    def __init__(self, log_level: str = "INFO") -> None:
        """
        Args:
            log_level (str): The log level for filtering of log messages.
            The default is INFO.
                Allowed values are DEBUG, INFO, WARN, ERROR, and FATAL.

        """
        self.log_level = log_level
        self.start_time = datetime.datetime.now()

    def elapsed_time(self) -> float:
        """Returns the elapsed time since the utility tool was created."""

        return (datetime.datetime.now() - self.start_time).total_seconds()

    def spec(self, spec_file: str = "config/json_schema.json") -> str:
        """Returns the JSON schema of the tool.

        Args:
            spec_file (str): The path to the JSON schema file.
            The default is config/json_schema.json.
        Returns:
            str: The JSON schema of the tool.
        """

        with open(spec_file) as f:
            spec = json.load(f)
            compact_json = json.dumps(spec, separators=(",", ":"))
            return compact_json

    def stream_spec(self, spec: str) -> None:
        """Streams JSON schema of the tool using the Unstract protocol SPEC to
        stdout.

        Args:
            spec (str): The JSON schema of the tool.
            Typically returned by the spec() method.

        Returns:
            None
        """
        record = {
            "type": "SPEC",
            "spec": spec,
            "emitted_at": datetime.datetime.now().isoformat(),
        }
        print(json.dumps(record))

    def properties(self, properties_file: str = "config/properties.json") -> str:
        """Returns the properties of the tool.

        Args:
            properties_file (str): The path to the properties file.
            The default is config/properties.json.
        Returns:
            str: The properties of the tool.
        """
        with open(properties_file) as f:
            properties = json.load(f)
            compact_json = json.dumps(properties, separators=(",", ":"))
            return compact_json

    def stream_properties(self, properties: str) -> None:
        """Streams the properties of the tool using the Unstract protocol
        PROPERTIES to stdout.

        Args:
            properties (str): The properties of the tool.
            Typically returned by the properties() method.
        Returns:
            None
        """
        record = {
            "type": "PROPERTIES",
            "properties": properties,
            "emitted_at": datetime.datetime.now().isoformat(),
        }
        print(json.dumps(record))

    def icon(self, icon_file: str = "config/icon.svg") -> str:
        """Returns the icon of the tool.

        Args:
            icon_file (str): The path to the icon file. The default is config/icon.svg.
        Returns:
            str: The icon of the tool.
        """
        with open(icon_file) as f:
            icon = f.read()
            return icon

    def stream_icon(self, icon: str) -> None:
        """Streams the icon of the tool using the Unstract protocol ICON to
        stdout.

        Args:
            icon (str): The icon of the tool. Typically returned by the icon() method.
        Returns:
            None
        """
        record = {
            "type": "ICON",
            "icon": icon,
            "emitted_at": datetime.datetime.now().isoformat(),
        }
        print(json.dumps(record))

    def stream_log(self, log: str, level: str = "INFO") -> None:
        """Streams a log message using the Unstract protocol LOG to stdout.

        Args:
            log (str): The log message.
            level (str): The log level. The default is INFO.
                Allowed values are DEBUG, INFO, WARN, ERROR, and FATAL.
        Returns:
            None
        """
        levels = ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"]
        if levels.index(level) < levels.index(self.log_level):
            return
        record = {
            "type": "LOG",
            "level": level,
            "log": log,
            "emitted_at": datetime.datetime.now().isoformat(),
        }
        print(json.dumps(record))

    def stream_cost(self, cost: float, cost_units: str) -> None:
        """Streams the cost of the tool using the Unstract protocol COST to
        stdout.

        Args:
            cost (float): The cost of the tool.
            cost_units (str): The cost units of the tool.
        Returns:
            None
        """
        record = {
            "type": "COST",
            "cost": cost,
            "cost_units": cost_units,
            "emitted_at": datetime.datetime.now().isoformat(),
        }
        print(json.dumps(record))

    def stream_single_step_message(self, message: str) -> None:
        """Streams a single step message using the Unstract protocol
        SINGLE_STEP_MESSAGE to stdout.

        Args:
            message (str): The single step message.
        Returns:
            None
        """
        record = {
            "type": "SINGLE_STEP_MESSAGE",
            "message": message,
            "emitted_at": datetime.datetime.now().isoformat(),
        }
        print(json.dumps(record))

    def stream_result(self, result: dict[Any, Any]) -> None:
        """Streams the result of the tool using the Unstract protocol RESULT to
        stdout.

        Args:
            result (dict): The result of the tool. Refer to the Unstract protocol
            for the format of the result.
        Returns:
            None
        """
        record = {
            "type": "RESULT",
            "result": result,
            "emitted_at": datetime.datetime.now().isoformat(),
        }
        print(json.dumps(record))

    def handle_static_command(self, command: str) -> None:
        """Handles a static command.

        Used to handle commands that do not require any processing. Currently,
        the only supported static commands are
        SPEC, PROPERTIES, and ICON.

        This is used by the Unstract SDK to handle static commands.
        It is not intended to be used by the tool. The tool
        stub will automatically handle static commands.

        Args:
            command (str): The static command.
        Returns:
            None
        """
        if command == "SPEC":
            self.stream_spec(self.spec())
        elif command == "PROPERTIES":
            self.stream_properties(self.properties())
        elif command == "ICON":
            self.stream_icon(self.icon())
        else:
            raise ValueError(f"Unknown command {command}")

    def get_env_or_die(self, env_key: str) -> str:
        """Returns the value of an env variable.

        If its empty or None, raises an error and exits

        Args:
            env_key (str): Key to retrieve

        Returns:
            str: Value of the env
        """
        env_value = os.environ.get(env_key)
        if env_value is None or env_value == "":
            self.stream_log(f"Env variable {env_key} is required", "ERROR")
            exit(1)
        return env_value

    @staticmethod
    def hash_str(string_to_hash: str, hash_method: str = "md5") -> str:
        """Computes the hash for a given input string.

        Useful to hash strings needed for caching and other purposes.
        Hash method defaults to "md5"

        Args:
            string_to_hash (str): String to be hashed
            hash_method (str): Hash hash_method to use, supported ones
                - "md5"

        Returns:
            str: Hashed string
        """
        if hash_method == "md5":
            return str(md5(string_to_hash.encode()).hexdigest())
        else:
            raise ValueError(f"Unsupported hash_method: {hash_method}")
