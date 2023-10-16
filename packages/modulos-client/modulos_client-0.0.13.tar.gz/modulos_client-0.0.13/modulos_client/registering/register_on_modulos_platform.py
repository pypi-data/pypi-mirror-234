# --------------------------------------------------- #
# Copyright (C) 2023 Modulos AG. All rights reserved. #
# --------------------------------------------------- #
import io
import json
import mimetypes
import os
import pickle
from typing import Any, Dict, Tuple

import pandas as pd
import requests

from modulos_client import config as config_utils


def _get_authorization_header() -> Dict[str, str]:
    """Get the authorization header.

    Returns:
        Dict[str, str]: The authorization header.
    """
    with config_utils.get_modulos_config() as config:
        profile = config.get_active_profile()
        token = profile.token
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def _get_host() -> str:
    """Get the host.

    Returns:
        str: The host.
    """
    with config_utils.get_modulos_config() as config:
        profile = config.get_active_profile()
        host = profile.host
    return host


def register_artifact_file(artifact_id: str, path_to_file: str):
    """Register an artifact on the Modulos platform.

    Args:
        artifact_id (str): The artifact ID.
        path_to_file (str): The path to the file.
    """
    host = _get_host()
    headers = _get_authorization_header()
    api_url = f"{host}/api/artifacts/{artifact_id}/upload"

    with open(path_to_file, "rb") as f:
        file = {
            "file": (
                os.path.basename(path_to_file),
                f,
                mimetypes.guess_type(path_to_file)[0] or "application/octet-stream",
            )
        }
        try:
            response = requests.post(api_url, files=file, headers=headers)
        except requests.exceptions.ConnectionError:
            print("Upload failed. Could not connect to the platform.")
            return None
    if response.status_code == 401:
        print(
            "Upload failed. There was an issue with the authorization. "
            "Please login again."
        )
        return None
    if response.ok:
        print("Upload successful")
        return None
    else:
        print(f"Upload failed: {response.text}")
        return None


def register_artifact_result(
    artifact_id: str, result: pd.DataFrame | Dict[str, Any] | Any, file_name: str
):
    """Register an artifact on the Modulos platform. It is uploaded as a file using
    the given name. The file type is determined by the file extension if possible.

    Args:
        artifact_id (str): The artifact ID.
        result (pd.DataFrame | Dict[str, Any] | str | Any): The result.
        filename (str): The name of the result.
    """
    host = _get_host()
    headers = _get_authorization_header()
    api_url = f"{host}/api/artifacts/{artifact_id}/upload"

    mimetype = mimetypes.guess_type(file_name)[0]

    if mimetype == "text/csv":
        if isinstance(result, pd.DataFrame):
            str_buffer = io.StringIO()
            result.to_csv(str_buffer, index=False)
            str_buffer.seek(0)
            file: Dict[str, Tuple[str, io.StringIO | io.BytesIO, str]] = {
                "file": (
                    file_name,
                    str_buffer,
                    mimetype,
                )
            }
        elif isinstance(result, dict):
            try:
                result_json = json.dumps(result)
            except Exception:
                raise Exception("Could not convert result to JSON.")
            df = pd.read_json(result_json)
            str_buffer = io.StringIO()
            df.to_csv(str_buffer, index=False)
            str_buffer.seek(0)
            file = {
                "file": (
                    file_name,
                    str_buffer,
                    mimetype,
                )
            }
        else:
            raise Exception(
                "Result must be a pandas DataFrame or a dict if it saved as a CSV "
                "file."
            )
    elif mimetype == "application/json":
        if isinstance(result, dict):
            try:
                result_json = json.dumps(result)
            except Exception:
                raise Exception("Could not convert result to JSON.")
            str_buffer = io.StringIO()
            str_buffer.write(result_json)
            str_buffer.seek(0)
            file = {
                "file": (
                    file_name,
                    str_buffer,
                    mimetype,
                )
            }
        elif isinstance(result, pd.DataFrame):
            try:
                result_json = result.to_json()
            except Exception:
                raise Exception("Could not convert result to JSON.")
            str_buffer = io.StringIO()
            str_buffer.write(result_json)
            str_buffer.seek(0)
            file = {
                "file": (
                    file_name,
                    str_buffer,
                    mimetype,
                )
            }
        else:
            raise Exception(
                "Result must be a pandas DataFrame or a dict if it saved as a JSON "
                "file."
            )
    elif mimetype == "text/plain":
        if isinstance(result, str):
            str_buffer = io.StringIO()
            str_buffer.write(result)
            str_buffer.seek(0)
            file = {
                "file": (
                    file_name,
                    str_buffer,
                    mimetype,
                )
            }
        else:
            raise Exception("Result must be a string if it saved as a text file.")
    else:
        if file_name.endswith(".pkl"):
            byte_buffer = io.BytesIO()
            pickle.dump(result, byte_buffer)
            byte_buffer.seek(0)
            file = {
                "file": (
                    file_name,
                    byte_buffer,
                    "application/octet-stream",
                )
            }
        else:
            raise Exception(
                "Result can be saved as a csv, text file or json file. If that is not "
                "possible, use a <name>.pkl as filename and the result is saved as "
                "pickle file."
            )

    try:
        response = requests.post(api_url, files=file, headers=headers)
    except requests.exceptions.ConnectionError:
        print("Upload failed. Could not connect to the platform.")
        return None
    if response.status_code == 401:
        print(
            "Upload failed. There was an issue with the authorization. "
            "Please login again."
        )
        return None
    if response.status_code == 200:
        print("Upload successful")
        return None
    else:
        print(f"Upload failed: {response.text}")
        return None
