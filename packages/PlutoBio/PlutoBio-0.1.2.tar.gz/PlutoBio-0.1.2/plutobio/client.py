import requests

import os


from .plots import Plot
from .assay_data import AssayData
from .sample_data import SampleData
from .analysis import Analysis
from .attachments import Attachment
from .pipelines import Pipelines
from .projects import Project
from .results import Results
from .experiments import Experiment
from .download_upload import DownloadUploadHandler
from .settings import DEFAULT_TMP_PATH


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

    def _make_request(self, method, endpoint, params=None, data=None):
        """
        Make a generic HTTP request to the API.

        :param method: HTTP method (GET, POST, PUT, DELETE, etc.).
        :type method: str
        :param endpoint: API endpoint.
        :type endpoint: str
        :param params: Query parameters.
        :type params: dict, optional
        :param data: Request data.
        :type data: dict, optional
        :return: JSON response.
        :rtype: dict
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

            response.raise_for_status()  # Raise an exception if the request was not successful

        return response.json()

    def get(self, endpoint, params=None):
        """
        Make a GET request to the API.

        :param endpoint: API endpoint.
        :type endpoint: str
        :param params: Query parameters.
        :type params: dict, optional
        :return: JSON response.
        :rtype: dict
        """
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint, data=None):
        """
        Make a POST request to the API.

        :param endpoint: API endpoint.
        :type endpoint: str
        :param data: Request data.
        :type data: dict, optional
        :return: JSON response.
        :rtype: dict
        """
        return self._make_request("POST", endpoint, data=data)

    def delete(self, endpoint, data=None):
        """
        Make a DELETE request to the API.

        :param endpoint: API endpoint.
        :type endpoint: str
        :param data: Request data.
        :type data: dict, optional
        :return: JSON response.
        :rtype: dict
        """
        return self._make_request("DELETE", endpoint, data=data)

    def put(self, endpoint, data=None):
        """
        Make a PUT request to the API.

        :param endpoint: API endpoint.
        :type endpoint: str
        :param data: Request data.
        :type data: dict, optional
        :return: JSON response.
        :rtype: dict
        """
        return self._make_request("PUT", endpoint, data=data)

    def patch(self, endpoint, data=None):
        """
        Make a PATCH request to the API.

        :param endpoint: API endpoint.
        :type endpoint: str
        :param data: Request data.
        :type data: dict, optional
        :return: JSON response.
        :rtype: dict
        """
        return self._make_request("PATCH", endpoint, data=data)

    def list_projects(self):
        return self._project.list()

    def get_project(self, project_id):
        return self._project.get(project_id=project_id)

    def list_experiments(self):
        return self._experiment.list()

    def get_experiment(self, experiment_id: str):
        return self._experiment.get(experiment_id)

    def list_plots(self, experiment_id):
        return self._plots.list(experiment_id)

    def get_plot(self, experiment_id, plot_id):
        return self._plots.get(experiment_id=experiment_id, plot_id=plot_id)

    def get_plot_data(self, experiment_id, plot_id):
        return self._plots.data(experiment_id=experiment_id, plot_id=plot_id)

    def get_assay_data(self, experiment_id, folder_path=DEFAULT_TMP_PATH):
        return self._assay_data.get(experiment_id, folder_path=folder_path)

    def get_sample_data(self, experiment_id, folder_path=DEFAULT_TMP_PATH):
        return self._sample_data.get(experiment_id, folder_path=folder_path)

    def download_bam_files(self, experiment_id, file_id, folder_path=DEFAULT_TMP_PATH):
        return self._pipelines.download_bam_files(
            experiment_id, file_id=file_id, folder_path=folder_path
        )

    def download_qc_report(self, experiment_id, folder_path=DEFAULT_TMP_PATH):
        return self._pipelines.download_qc_report(experiment_id, folder_path)

    def list_attachments(self, experiment_id):
        return self._attachment.list(experiment_id)

    def download_attachments(
        self, experiment_id, file_id, folder_path=DEFAULT_TMP_PATH
    ):
        return self._attachment.download(
            experiment_id, file_id, folder_path=folder_path
        )

    def add_plot(
        self,
        experiment_id,
        plot_id=None,
        file_path=DEFAULT_TMP_PATH,
        plot_data=None,
        methods=None,
    ):
        return self._plots.post(experiment_id, plot_id, file_path, plot_data, methods)

    def download_file(self, experiment_id, file_id):
        return self._download_upload.download_file(experiment_id, file_id)

    def upload_file(self, experiment_id, file_path=DEFAULT_TMP_PATH):
        return self._download_upload.upload_file(experiment_id, file_path)
