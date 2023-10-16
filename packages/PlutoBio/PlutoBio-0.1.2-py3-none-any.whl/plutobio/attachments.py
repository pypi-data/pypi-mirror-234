from .settings import DEFAULT_TMP_PATH
from typing import TYPE_CHECKING
from . import utils
import time
import os
from .log_handler import download_upload_logger
import requests
from . import api_endpoints

# TODO: Need to add results and methods to the API

if TYPE_CHECKING:
    from . import PlutoClient


class Attachments(list):
    def __init__(self, client: "PlutoClient") -> None:
        super().__init__()  # Initialize the list
        self._client = client


class Attachment:
    def __init__(self, client: "PlutoClient") -> None:
        self._client = client
        self.data_type = "attachment"
        self.uuid = ""
        self.filename = ""
        self.display_name = ""

    def list(self, experiment_id: str, raw=False):
        data = {"data_type": self.data_type}
        response = self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/files",
            params=data,
        )
        if raw:
            return response

        attachments = Attachments(self._client)
        for attachment in response["attachments"]["items"]:
            attachment_as_object = utils.to_class(Attachment(self._client), attachment)
            attachments.append(attachment_as_object)

        return attachments

    def get(self, experiment_id: str, file_id: str, raw=False):
        response = self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/attachments/{file_id}"
        )
        if raw:
            return response
        return utils.to_class(Attachment(self._client), response)

    def download(
        self,
        experiment_id: str,
        file_id: str,
        folder_path=DEFAULT_TMP_PATH,
        is_cache=True,
    ):
        attachment = self.get(experiment_id, file_id)
        # TODO: This needs to me moved to the downlaod mannager
        data = {"filename": attachment.display_name}
        attachment_download = self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/files/{file_id}/download",
            params=data,
        )

        response = requests.get(attachment_download["url"], stream=True)
        total_size = int(response.headers.get("Content-Length", 0))
        downloaded_size = 0
        is_user_updated = False
        with open(
            os.path.join(folder_path, f"{attachment.display_name}"), "wb"
        ) as file:
            start_time = time.time()
            update_interval = 1  # Update progress every 1 second
            # 8 MiB as recommended by gcs: https://cloud.google.com/storage/docs/performing-resumable-uploads
            for data in response.iter_content(chunk_size=8 * 1024 * 1024):
                file.write(data)
                downloaded_size += len(data)

                current_time = time.time()
                if current_time - start_time >= update_interval:
                    is_user_updated = True
                    download_upload_logger.info(
                        f"Downloading attachment {round((downloaded_size/total_size)*100)}%"
                    )
                    start_time = current_time

        if is_user_updated:
            download_upload_logger.info(f"Done 100%")
