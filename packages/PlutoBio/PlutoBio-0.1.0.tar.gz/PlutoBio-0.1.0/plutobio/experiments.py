from typing import TYPE_CHECKING
from . import utlis
from . import api_endpoints

if TYPE_CHECKING:
    from . import PlutoClient


class Experiments(dict):
    def __init__(self, client: "PlutoClient") -> None:
        super().__init__()  # Initialize the dictionary
        self._client = client


class Experiment:
    def __init__(self, client: "PlutoClient") -> None:
        self._client = client
        self.uuid = ""
        self.pluto_id = ""
        self.name = ""
        self.description = ""
        self.markdown_long_description = ""

    def list(self, raw=False):
        response = self._client.get(f"{api_endpoints.APIEndpoints.experiments}")
        if raw:
            return response

        experiments = Experiments(self._client)
        for experiment in response["items"]:
            experiment_as_object = utlis.to_class(Experiment(self._client), experiment)
            experiments[experiment_as_object.pluto_id] = experiment_as_object

        return experiments

    def get(self, experiment_id: str, raw=False):
        response = self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}"
        )
        if raw:
            return response
        return utlis.to_class(Experiment(self._client), response)

    def list_plots(self, experiment_id: str):
        return self._client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/plots"
        )

    def get_assay_data(self):
        return self._client._assay_data.get()

    def get_sample_data(self):
        return self._client._sample_data.get()

    def get_plot(self, plot_id):
        return self._client._plots.get(plot_id=plot_id)

    def __repr__(self) -> str:
        return f"{self.name}"
