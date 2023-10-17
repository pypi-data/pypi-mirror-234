import os

import requests
from unstract_sdk.tools import UnstractToolUtils


class UnstractToolCache:
    """Class to handle caching for Unstract Tools

    Notes:
        - PLATFORM_API_KEY environment variable is required.

    """

    def __init__(self, utils: UnstractToolUtils, platform_host: str, platform_port: int):
        """
        Args:
            utils (UnstractToolUtils): The utils object for the tool.
            platform_host (str): The host of the platform.
            platform_port (int): The port of the platform.

        Notes:
            - PLATFORM_API_KEY environment variable is required.
            - The platform_host and platform_port are the host and port of the platform service.
        """
        self.utils = utils
        self.platform_host = platform_host
        if self.platform_host[-1] == "/":
            self.platform_host = self.platform_host[:-1]
        self.platform_port = platform_port
        self.bearer_token = os.environ.get("PLATFORM_API_KEY")

    def set(self, key: str, value: str):
        """Sets the value for a key in the cache.

        Args:
            key (str): The key.
            value (str): The value.

        Returns:
            bool: Whether the operation was successful.
        """

        url = f"{self.platform_host}:{self.platform_port}/cache"
        json = {"key": key, "value": value}
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        response = requests.post(url, json=json, headers=headers)

        if response.status_code == 200:
            self.utils.stream_log(f"Successfully cached data for key: {key}")
            return True
        else:
            self.utils.stream_log(
                f"Error while caching data for key: {key} / {response.reason}", level="ERROR")
            return False

    def get(self, key: str):
        """Gets the value for a key in the cache.

        Args:
            key (str): The key.

        Returns:
            str: The value.
        """

        url = f"{self.platform_host}:{self.platform_port}/cache?key={key}"
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            self.utils.stream_log(
                f"Successfully retrieved cached data for key: {key}")
            return response.text
        elif response.status_code == 404:
            self.utils.stream_log(
                f"Data not found for key: {key}", level="WARN")
            return None
        else:
            self.utils.stream_log(f"Error while retrieving cached data for key: {key} / {response.reason}",
                                  level="ERROR")
            return None

    def delete(self, key: str):
        """Deletes the value for a key in the cache.

        Args:
            key (str): The key.

        Returns:
            bool: Whether the operation was successful.

        """
        url = f"{self.platform_host}:{self.platform_port}/cache?key={key}"
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            self.utils.stream_log(
                f"Successfully deleted cached data for key: {key}")
            return True
        else:
            self.utils.stream_log(f"Error while deleting cached data for key: {key} / {response.reason}",
                                  level="ERROR")
            return False
