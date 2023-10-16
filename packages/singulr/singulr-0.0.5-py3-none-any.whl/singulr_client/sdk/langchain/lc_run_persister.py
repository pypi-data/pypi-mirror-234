# Created by msinghal at 04/10/23
from __future__ import annotations
import os
import pandas as pd
import time
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
if os.environ.get('LOG_FOLDER'):
    folder_path = os.environ.get('LOG_FOLDER')
else:
    folder_path = "/tmp"

# set logger
from singulr_client.common import log_config
log_config.configure_logger(folder_path=folder_path, is_console_logging=True, is_debug_enabled=False)
logger = log_config.singulr_sdk

# read local .env file
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from typing import (
    Any,
    DefaultDict,
    Dict,
    Optional,
    cast,
)

from singulr_client.common.env_utils import get_runtime_environment


def _serialize_json(obj: Any) -> str:
    """Serialize an object to JSON.

    Parameters
    ----------
    obj : Any
        The object to serialize.

    Returns
    -------
    str
        The serialized JSON string.

    Raises
    ------
    TypeError
        If the object type is not serializable.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return str(obj)


class LCRunPersister(object):
    """Client for interacting with the Singulr SDK"""

    def create_run(
            self,
            name: str,
            inputs: Dict[str, Any],
            run_type: str,
            *,
            execution_order: Optional[int] = None,
            **kwargs: Any,
    ) -> Optional[Dict[str, str]]:
        """
        Create a new run.

        Parameters
        ----------
        name : str
            The name of the run.
        inputs : Dict[str, Any]
            The inputs for the run.
        run_type : str
            The type of the run.
        execution_order : Optional[int], optional
            The execution order of the run, by default None.
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        Optional[Dict[str, str]]
            A dictionary with a message indicating the status of the run creation.

        Raises
        ------
        Exception
            If the specified folder location does not exist.
        """
        project_name = kwargs.pop(
            "project_name",
            kwargs.pop(
                "session_name",
                os.environ.get(
                    # TODO: Deprecate LANGCHAIN_SESSION
                    "LANGCHAIN_PROJECT",
                    os.environ.get("LANGCHAIN_SESSION", "default"),
                ),
            ),
        )
        run_create = {
            **kwargs,
            "session_name": project_name,
            "name": name,
            "inputs": inputs,
            "run_type": run_type,
            "execution_order": execution_order if execution_order is not None else 1,
        }
        run_extra = cast(dict, run_create.setdefault("extra", {}))
        runtime = run_extra.setdefault("runtime", {})

        runtime_env = get_runtime_environment()
        run_extra["runtime"] = {**runtime_env, **runtime}
        print("...saving run {}".format(run_create))
        file_name = str(run_create["id"]) + "-" + str(int(time.time()))
        df = pd.DataFrame.from_dict([run_create])
        df = df.astype(str)
        if os.environ.get('LANGCHAIN_RUN_STORAGE_LOCATION'):
            if not os.path.exists(os.environ.get('LANGCHAIN_RUN_STORAGE_LOCATION')):
                logger.info("Folder location does not exist. Environment variable LANGCHAIN_RUN_STORAGE_LOCATION is incorrect.")
                return {"message": "Run created successfully"}
            directory_path = os.environ.get('LANGCHAIN_RUN_STORAGE_LOCATION') + "/create_events"
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            df.to_parquet(directory_path + "/{}.parquet".format(file_name), engine='pyarrow')
        return {"message": "Run created successfully"}

    def update_run(
            self,
            run_id: str,
            **kwargs: Any,
    ) -> Optional[Dict[str, str]]:
        """
        Update an existing run.

        Parameters
        ----------
        run_id : str
            The ID of the run to update.
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        Optional[Dict[str, str]]
            A dictionary with a message indicating the status of the run update.

        Raises
        ------
        Exception
            If the specified folder location does not exist.
        """
        print("...updating run {}".format(run_id))
        file_name = str(kwargs["id"]) + "-" + str(int(time.time()))
        df = pd.DataFrame.from_dict([kwargs])
        df = df.astype(str)
        if os.environ.get('LANGCHAIN_RUN_STORAGE_LOCATION'):
            if not os.path.exists(os.environ.get('LANGCHAIN_RUN_STORAGE_LOCATION')):
                logger.info("Folder location does not exist. Environment variable LANGCHAIN_RUN_STORAGE_LOCATION is incorrect.")
                return {"message": f"Run {run_id} updated successfully"}
            directory_path = os.environ.get('LANGCHAIN_RUN_STORAGE_LOCATION') + "/update_events"
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            df.to_parquet(directory_path + "/{}.parquet".format(file_name), engine='pyarrow')
        return {"message": f"Run {run_id} updated successfully"}
