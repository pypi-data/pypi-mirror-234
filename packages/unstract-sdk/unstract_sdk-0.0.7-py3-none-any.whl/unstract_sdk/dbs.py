import os
from typing import Any

import requests
from unstract_sdk.constants import DbConnectorKeys, PlatformServiceKeys
from unstract_sdk.tools import UnstractToolUtils

from pandora_core.connectors.databases import connectors
from pandora_core.connectors.databases.pandora_db import PandoraDB


class UnstractToolDB:
    """Class to handle DB connectors for Unstract Tools.

    Notes:
        - PLATFORM_API_KEY environment variable is required.
    """

    def __init__(
        self,
        utils: UnstractToolUtils,
        platform_host: str,
        platform_port: str,
    ) -> None:
        """
        Args:
            utils (UnstractToolUtils): _description_
            platform_host (str): _description_
            platform_port (str): _description_

        Notes:
            - PLATFORM_API_KEY environment variable is required.
            - The platform_host and platform_port are the
                host and port of the platform service.
        """
        self.utils = utils
        if platform_host[-1] == "/":
            self.base_url = f"{platform_host[:-1]}:{platform_port}"
        self.base_url = f"{platform_host}:{platform_port}/db"
        self.bearer_token = os.environ.get(PlatformServiceKeys.PLATFORM_API_KEY)
        self.db_connectors = connectors

    def get_engine(self, tool_instance_id: str) -> Any:
        """
        1. Get the connection settings (including auth for db)
        from platform service using the tool_instance_id
        2. Create PandoraDB based object using the settings
            2.1 Find the type of the database (From Connector Registry)
            2.2 Create the object using the type
            (derived class of PandoraDB) (Mysql/Postgresql/Bigquery/Snowflake/...)
        3. Send Object.get_engine() to the caller
        """
        url = f"{self.base_url}/connector_instance"
        query_params = {
            DbConnectorKeys.TOOL_INSTANCE_ID: tool_instance_id,
        }
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        response = requests.get(url, headers=headers, params=query_params)
        if response.status_code == 200:
            connector_data: dict[str, Any] = response.json()
            connector_id = connector_data.get(DbConnectorKeys.CONNECTOR_ID)
            connector_instance_id = connector_data.get(DbConnectorKeys.ID)
            settings = connector_data.get(DbConnectorKeys.CONNECTOR_METADATA)
            self.utils.stream_log(
                "Successfully retrieved connector settings "
                f"for connector: {connector_instance_id}"
            )
            if connector_id in self.db_connectors:
                connector = self.db_connectors[connector_id]["metadata"]["connector"]
                connector_calss: PandoraDB = connector(settings)
                return connector_calss.get_engine()
            else:
                self.utils.stream_log(
                    f"engine not found for connector: {connector_id}", level="ERROR"
                )
                return None

        elif response.status_code == 404:
            self.utils.stream_log(
                f"connector not found for: for tool instance {tool_instance_id}",
                level="ERROR",
            )
            return None

        else:
            self.utils.stream_log(
                (
                    f"Error while retrieving connector "
                    "for tool instance: "
                    f"{tool_instance_id} / {response.reason}"
                ),
                level="ERROR",
            )
            return None
