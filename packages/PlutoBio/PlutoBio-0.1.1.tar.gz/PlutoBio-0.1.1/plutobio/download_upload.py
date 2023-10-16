from typing import TYPE_CHECKING
from .settings import DEFAULT_TMP_PATH
import os
import requests
from .log_handler import download_upload_logger
from . import api_endpoints

if TYPE_CHECKING:
    from . import PlutoClient


class DownloadUploadHandler:
    """
    Manager class to handle upload and downloading data from pluto api.
    The manager does not interact directly with the cloud storage, rather it interacts with the pluto api to get a signed url.
    With the signed url it will then upload and download the data to that url
    """

    def __init__(self, client: "PlutoClient") -> None:
        self._client = client

    def upload_file(self, experiment_id, analysis_id, file_path=DEFAULT_TMP_PATH):
        data = {
            "analysis_type": "external",
            "origin": "python",
            "filename": f"{analysis_id}/{os.path.basename(file_path)}",
            "data_type": "external",
            "file_type": os.path.splitext(os.path.basename(file_path))[1],
            "file_size": os.path.getsize(file_path),
        }

        response = self._client.post(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/upload-sessions",
            data=data,
        )

        session_uri = response["session_url"]

        uploaded_range = ""
        headers = {"Content-Length": "0", "Content-Range": "bytes */*"}
        response = requests.put(session_uri, headers=headers)

        if 308 == response.status_code:
            if "Range" in response.headers:
                # Range will be in the format "bytes=0-x"
                uploaded_range = [
                    int(x) for x in response.headers["Range"].split("=")[1].split("-")
                ]
            else:
                uploaded_range = [0, -1]

        if not uploaded_range:
            download_upload_logger.info("Could not determine uploaded range.")
            return

        start_byte = uploaded_range[1] + 1
        with open(file_path, "rb") as f:
            f.seek(start_byte)
            file_data = f.read()

        total_size = os.path.getsize(file_path)
        headers = {
            "Content-Length": str(len(file_data)),
            "Content-Range": f"bytes {start_byte}-{total_size-1}/{total_size}",
        }

        response = requests.put(session_uri, headers=headers, data=file_data)

        # If successful, response should be 201 or 200
        if response.status_code in [200, 201]:
            download_upload_logger.info("Upload successful!")
        else:
            download_upload_logger.info(
                f"Upload failed with status code: {response.status_code}. Response: {response.text}"
            )

        return response

    def download_file(self, experiment_id, file_id):
        pass
