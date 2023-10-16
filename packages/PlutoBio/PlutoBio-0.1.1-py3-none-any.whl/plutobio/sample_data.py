from .settings import (
    DATA_ANALYSIS_OPTIONS_ENUM,
    DATA_ANALYSIS_OPTIONS,
    DEFAULT_TMP_PATH,
)
import pandas as pd
from typing import TYPE_CHECKING
import math
import os
from .log_handler import download_upload_logger
import time
from . import api_endpoints

if TYPE_CHECKING:
    from . import PlutoClient


class SampleData:
    def __init__(self, client: "PlutoClient") -> None:
        self._client = client

    def get(
        self, experiment_id, folder_path=DEFAULT_TMP_PATH, raw=False, is_cache=True
    ):
        response = self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/sample-data"
        )
        if raw:
            return response

        if (
            os.path.exists(
                os.path.join(folder_path, f"{experiment_id}_sample_data.csv")
            )
            and is_cache
        ):
            df = pd.read_csv(
                os.path.join(folder_path, f"{experiment_id}_sample_data.csv")
            )
            return df

        count = response["count"]

        offset = math.ceil(count / 100)

        df: pd.DataFrame = pd.DataFrame(columns=response["headers"])
        match DATA_ANALYSIS_OPTIONS:
            case DATA_ANALYSIS_OPTIONS_ENUM.PANDAS:
                df = pd.DataFrame(response["items"], columns=response["headers"])

        is_user_updated = False
        start_time = time.time()
        update_interval = 1  # Update progress every 1 second
        for step in range(1, offset):
            data = {"offset": step * 100, "limit": 100}
            response = self._client.get(
                f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/sample-data",
                params=data,
            )
            partial_df = pd.DataFrame(response["items"], columns=response["headers"])
            df = pd.concat([df, partial_df], ignore_index=True)

            current_time = time.time()
            if current_time - start_time >= update_interval:
                is_user_updated = True
                download_upload_logger.info(
                    f"Getting sample data {round((step/offset)*100)}%"
                )
                start_time = current_time

        if is_user_updated:
            download_upload_logger.info(f"Done 100%")

        os.makedirs(folder_path, exist_ok=True)
        # Save the file as a csv
        df.to_csv(
            os.path.join(folder_path, f"{experiment_id}_sample_data.csv"), index=False
        )

        return df
