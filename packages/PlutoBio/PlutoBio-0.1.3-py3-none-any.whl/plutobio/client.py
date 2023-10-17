import requests
from typing import Union
import os
import uuid

from .plots import Plot, Plots
from .assay_data import AssayData
from .sample_data import SampleData
from .analysis import Analysis
from .attachments import Attachment
from .pipelines import Pipelines
from .projects import Project
from .results import Results
from .experiments import Experiment, Experiments
from .download_upload import DownloadUploadHandler
from .settings import DEFAULT_TMP_PATH
import pandas as pd
import requests


class PlutoClient:
    """Base class for Pluto API access"""

    def __init__(self, token: str, test_client=None) -> None:
        self._experiment = Experiment(client=self)
        self._plots = Plot(client=self)
        self._assay_data = AssayData(client=self)
        self._sample_data = SampleData(client=self)
        self._attachment = Attachment(client=self)
        self._analysis = Analysis(client=self)
        self._pipelines = Pipelines(client=self)
        self._project = Project(client=self)
        self._results = Results(client=self)
        self._download_upload = DownloadUploadHandler(client=self)
        self._token = token
        self._base_url = os.environ.get("PLUTO_API_URL", "https://api.pluto.bio")
        self._test_client = test_client

    def _make_request(
        self, method: str, endpoint: str, params: dict = None, data: dict = None
    ) -> dict:
        """
        Make a generic HTTP request to the API.

        :param method: HTTP method (e.g., GET, POST, PUT, DELETE).
        :type method: str
        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param params: Query parameters to be included in the request, defaults to None.
        :type params: dict, optional
        :param data: JSON data to be sent in the request body, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the request to the API is not successful.
        """
        url = f"{self._base_url}/{endpoint}/"

        # For django testing we need to use the django client
        if self._test_client:
            request_headers = {
                "HTTP_AUTHORIZATION": f"Token {self._token}",
            }
            response = self._test_client.get(url, data=params, **request_headers)

        else:
            request_headers = {
                "AUTHORIZATION": f"Token {self._token}",
            }

            response = requests.request(
                method, url, params=params, json=data, headers=request_headers
            )

            # response.raise_for_status()  # Raise an exception if the request was not successful

        if response.status_code == 400:
            raise Exception(f"Bad request: {response.content}")

        return response

    def get(self, endpoint: str, params: dict = None) -> dict:
        """
        Make a GET request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param params: Query parameters to be included in the GET request, defaults to None.
        :type params: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the GET request to the API is not successful.
        """
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: dict = None) -> dict:
        """
        Make a POST request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param data: Data payload to be sent in the POST request, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the POST request to the API is not successful.
        """
        return self._make_request("POST", endpoint, data=data)

    def delete(self, endpoint: str, data: dict = None) -> dict:
        """
        Make a DELETE request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param data: Data payload to be sent in the DELETE request, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the DELETE request to the API is not successful.
        """
        return self._make_request("DELETE", endpoint, data=data)

    def put(self, endpoint: str, data: dict = None) -> dict:
        """
        Make a PUT request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param data: Data payload to be sent in the PUT request, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the PUT request to the API is not successful.
        """
        return self._make_request("PUT", endpoint, data=data)

    def patch(self, endpoint: str, data: dict = None) -> dict:
        """
        Make a PATCH request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param data: Data payload to be sent in the PATCH request, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the PATCH request to the API is not successful.
        """
        return self._make_request("PATCH", endpoint, data=data)

    def list_projects(self):
        return self._project.list()

    def get_project(self, project_id: Union[str, uuid.UUID]):
        """Retrieves details for a specific project based on its uuid or pluto ID.

        Args:
            project_id (str or uuid): The pluto id or object uuid of the project to retrieve.

        Returns:
            Project Object: Project object.
        """
        return self._project.get(project_id=project_id)

    def list_experiments(self) -> Experiments:
        """Lists all projects.

        Returns:
            list: List of projects.
        """
        return self._experiment.list()

    def get_experiment(self, experiment_id: Union[str, uuid.UUID]) -> Experiment:
        """Retrieves details for a specific project based on its uuid or pluto ID.

        Args:
            experiment_id (str or uuid): The pluto id or object uuid of the experiment to retrieve.

        Returns:
            dict: Experiment details.
        """
        return self._experiment.get(experiment_id)

    def list_plots(self, experiment_id: Union[str, uuid.UUID]) -> Plots:
        return self._plots.list(experiment_id)

    def get_plot(
        self, experiment_id: Union[str, uuid.UUID], plot_id: Union[str, uuid.UUID]
    ) -> Plot:
        return self._plots.get(experiment_id=experiment_id, plot_id=plot_id)

    def get_plot_data(
        self, experiment_id: Union[str, uuid.UUID], plot_id: Union[str, uuid.UUID]
    ) -> pd.DataFrame:
        return self._plots.data(experiment_id=experiment_id, plot_id=plot_id)

    def get_assay_data(
        self, experiment_id: Union[str, uuid.UUID], folder_path: str = DEFAULT_TMP_PATH
    ) -> pd.DataFrame:
        return self._assay_data.get(experiment_id, folder_path=folder_path)

    def get_sample_data(
        self, experiment_id: Union[str, uuid.UUID], folder_path: str = DEFAULT_TMP_PATH
    ) -> pd.DataFrame:
        return self._sample_data.get(experiment_id, folder_path=folder_path)

    def download_bam_files(
        self,
        experiment_id: Union[str, uuid.UUID],
        file_id: Union[str, uuid.UUID],
        folder_path: str = DEFAULT_TMP_PATH,
    ):
        return self._pipelines.download_bam_files(
            experiment_id, file_id=file_id, folder_path=folder_path
        )

    def download_qc_report(
        self, experiment_id: Union[str, uuid.UUID], folder_path: str = DEFAULT_TMP_PATH
    ):
        return self._pipelines.download_qc_report(experiment_id, folder_path)

    def list_attachments(self, experiment_id: Union[str, uuid.UUID]):
        return self._attachment.list(experiment_id)

    def download_attachments(
        self,
        experiment_id: Union[str, uuid.UUID],
        file_id: Union[str, uuid.UUID],
        folder_path: str = DEFAULT_TMP_PATH,
    ):
        return self._attachment.download(
            experiment_id, file_id, folder_path=folder_path
        )

    def add_plot(
        self,
        experiment_id: Union[str, uuid.UUID],
        plot_id: Union[str, uuid.UUID] = None,
        file_path: str = DEFAULT_TMP_PATH,
        plot_data: str = None,
        methods: str = None,
    ):
        return self._plots.post(experiment_id, plot_id, file_path, plot_data, methods)

    def download_file(
        self, experiment_id: Union[str, uuid.UUID], file_id: Union[str, uuid.UUID]
    ):
        return self._download_upload.download_file(experiment_id, file_id)

    def upload_file(
        self, experiment_id: Union[str, uuid.UUID], file_path: str = DEFAULT_TMP_PATH
    ):
        return self._download_upload.upload_file(experiment_id, file_path)
