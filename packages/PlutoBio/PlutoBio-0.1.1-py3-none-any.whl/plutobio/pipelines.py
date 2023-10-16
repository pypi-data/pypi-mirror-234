from typing import TYPE_CHECKING
import requests
from .log_handler import download_upload_logger
import time
import os
from .settings import DEFAULT_TMP_PATH
from . import api_endpoints

if TYPE_CHECKING:
    from .client import PlutoClient


class Pipelines:
    def __init__(self, client: "PlutoClient") -> None:
        self._client = client
        self.file_path = ""

    def list(self, experiment_id):
        return self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/files"
        )

    def list_bam_files(self, experiment_id):
        data = {"data_type": "bam"}
        return self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/files",
            params=data,
        )

    def download_bam_files(self, experiment_id, file_id, folder_path=DEFAULT_TMP_PATH):
        bam_files = self.list_bam_files(experiment_id)
        bam_file_name = ""
        for bam in bam_files["bam"]["items"]:
            if file_id == bam["uuid"]:
                bam_file_name = bam["filename"]
                break

        data = {"filename": bam_file_name}
        bam_file = self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/files/{file_id}/download",
            params=data,
        )

        response = requests.get(bam_file["url"], stream=True)
        total_size = int(response.headers.get("Content-Length", 0))
        downloaded_size = 0
        is_user_updated = False
        with open(os.path.join(folder_path, f"{experiment_id}"), "wb") as file:
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
                        f"Downloading bam file {round((downloaded_size/total_size)*100)}%"
                    )
                    start_time = current_time

        if is_user_updated:
            download_upload_logger.info(f"Done 100%")

    def get_qc_report(self, experiment_id):
        return self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/qc-report"
        )

    def download_qc_report(self, experiment_id, folder_path=DEFAULT_TMP_PATH):
        qc_report = self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/qc-report/download"
        )
        response = requests.get(qc_report["url"], stream=True)
        total_size = int(response.headers.get("Content-Length", 0))
        downloaded_size = 0
        is_user_updated = False
        with open(
            os.path.join(folder_path, f"{experiment_id}_QC_report.html"), "wb"
        ) as file:
            start_time = time.time()
            update_interval = 1  # Update progress every 1 second
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                downloaded_size += len(data)

                current_time = time.time()
                if current_time - start_time >= update_interval:
                    is_user_updated = True
                    download_upload_logger.info(
                        f"Downloading qc report {round((downloaded_size/total_size)*100)}%"
                    )
                    start_time = current_time

        if is_user_updated:
            download_upload_logger.info(f"Done 100%")

        qc_pipeline = Pipelines(client=self._client)
        qc_pipeline.file_path = os.path.join(
            folder_path, f"{experiment_id}_QC_report.html"
        )
        return qc_pipeline
