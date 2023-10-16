from . import api_endpoints


class Results:
    def __init__(self, client) -> None:
        self.client = client

    def list(self, experiment_id):
        return self.client.get(
            f"{api_endpoints.APIEndpoints.experiments}/{experiment_id}/plots"
        )

    def get(self):
        pass

    def create(self):
        pass

    def delete(self):
        pass
