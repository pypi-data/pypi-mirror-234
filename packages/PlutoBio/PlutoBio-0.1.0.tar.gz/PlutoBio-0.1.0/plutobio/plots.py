from .settings import DATA_ANALYSIS_OPTIONS_ENUM, DATA_ANALYSIS_OPTIONS
import pandas as pd
from typing import TYPE_CHECKING, Union
import math
from . import utlis
from .settings import DEFAULT_TMP_PATH
from . import api_endpoints
import os

if TYPE_CHECKING:
    from . import PlutoClient


class Plots(list):
    def __init__(self, client: "PlutoClient") -> None:
        super().__init__()  # Initialize the list
        self._client = client


class Plot:
    def __init__(self, client: "PlutoClient") -> None:
        self._client = client

    def list(self, experiment_id: str, raw=False):
        response = self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/plots"
        )
        if raw:
            return response

        plots = Plots(self._client)
        for plot in response["items"]:
            plot_as_object = utlis.to_class(Plot(self._client), plot)
            plots.append(plot_as_object)

        return plots

    def get(self, experiment_id: str, plot_id: str, raw=False):
        response = self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/plots/{plot_id}"
        )
        if raw:
            return response
        return utlis.to_class(Plot(self._client), response)

    def data(self, experiment_id: str, plot_id: str, raw=False):
        response = self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/plots/{plot_id}/data"
        )
        if raw:
            return response

        count = response["count"]

        offset = math.ceil(count / 100)

        df: pd.DataFrame(index=range(count), columns=len(response["headers"]))
        match DATA_ANALYSIS_OPTIONS:
            case DATA_ANALYSIS_OPTIONS_ENUM.PANDAS:
                df = pd.DataFrame(response["items"], columns=response["headers"])

        for step in range(1, offset):
            data = {"offset": step * 100, "limit": 100}
            response = self._client.get(
                f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/plots/{plot_id}/data",
                params=data,
            )
            partial_df = pd.DataFrame(response["items"], columns=response["headers"])
            df = pd.concat([df, partial_df], ignore_index=True)

        return df

    def post(
        self,
        experiment_id: str,
        plot_id: str = None,
        file_path: str = DEFAULT_TMP_PATH,
        plot_data: Union[pd.DataFrame, str] = None,
        methods: str = None,
    ):
        plot_uuid = ""
        analysis_uuid = ""
        if plot_id is not None:
            analysis_response = self.get(experiment_id, plot_id, raw=True)
            analysis_uuid = analysis_response["analysis"]["uuid"]
            plot_uuid = plot_id
        else:
            create_figure = self._client.post(
                f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/plots",
                data={
                    "analysis_type": "external",
                    "display_type": "html",
                    "status": "published",
                },
            )
            plot_uuid = create_figure["uuid"]

            analysis_data = {
                "analysis_type": "external",
                "name": f"{os.path.basename(file_path)}",
                "methods": methods,
            }

            if plot_data is not None:
                analysis_data["results"] = os.path.basename(plot_data)

            create_analysis = self._client.post(
                f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/analyses",
                data=analysis_data,
            )
            analysis_uuid = create_analysis["uuid"]

        upload_response = self._client._download_upload.upload_file(
            experiment_id, analysis_uuid, file_path
        )

        if plot_data is not None:
            if isinstance(plot_data, pd.DataFrame):
                temp_file_path = os.path.join(DEFAULT_TMP_PATH, "plot_data.csv")
                plot_data.to_csv(temp_file_path, index=False)

                upload_post_data_response = self._client._download_upload.upload_file(
                    experiment_id, analysis_uuid, temp_file_path
                )

                os.remove(temp_file_path)
            else:
                upload_post_data_response = self._client._download_upload.upload_file(
                    experiment_id, analysis_uuid, plot_data
                )

        # TODO: We need to add a safe for the upload response. In case it fails, we need to be able to
        # remove the analysis that we created

        # TODO: We need to have a post validation after files are uploaded

        response = self._client.put(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/plots/{plot_uuid}",
            data={"analysis_id": analysis_uuid},
        )

        return response
