from .settings import (
    DATA_ANALYSIS_OPTIONS_ENUM,
    DATA_ANALYSIS_OPTIONS,
    DEFAULT_TMP_PATH,
)
import pandas as pd
from typing import TYPE_CHECKING
import math
from .log_handler import download_upload_logger
import time
import os

if TYPE_CHECKING:
    from . import PlutoClient


class AssayData:
    def __init__(self, client: "PlutoClient") -> None:
        self._client = client

    def get(
        self, experiment_id, is_cache=True, raw=False, folder_path=DEFAULT_TMP_PATH
    ):
        # TODO: Allow Caching
        # TODO: Implement Download Assay_Data
        # TODO: Load Assay_Data
        response = self._client.get(f"lab/experiments/{experiment_id}/assay-data")
        if raw:
            return response

        if (
            os.path.exists(os.path.join(folder_path, f"{experiment_id}_assay_data.csv"))
            and is_cache
        ):
            df = pd.read_csv(
                os.path.join(folder_path, f"{experiment_id}_assay_data.csv")
            )
            return df

        count = response["count"]

        offset = math.ceil(count / 1000)

        df: pd.DataFrame(index=range(count), columns=len(response["headers"]))
        match DATA_ANALYSIS_OPTIONS:
            case DATA_ANALYSIS_OPTIONS_ENUM.PANDAS:
                df = pd.DataFrame(response["items"], columns=response["headers"])

        is_user_updated = False
        start_time = time.time()
        update_interval = 1  # Update progress every 1 second
        for step in range(1, offset):
            # TODO: Increase Items Retrived
            data = {"offset": step * 1000, "limit": 1000}
            response = self._client.get(
                f"lab/experiments/{experiment_id}/assay-data", params=data
            )
            partial_df = pd.DataFrame(response["items"], columns=response["headers"])
            df = pd.concat([df, partial_df], ignore_index=True)

            current_time = time.time()
            if current_time - start_time >= update_interval:
                is_user_updated = True
                download_upload_logger.info(
                    f"Getting assay data {round((step * 1000/count)*100)}%"
                )
                start_time = current_time

        if is_user_updated:
            download_upload_logger.info(f"Done 100%")

        os.makedirs(folder_path, exist_ok=True)
        # Save the file as a csv
        df.to_csv(
            os.path.join(folder_path, f"{experiment_id}_assay_data.csv"), index=False
        )

        return df
