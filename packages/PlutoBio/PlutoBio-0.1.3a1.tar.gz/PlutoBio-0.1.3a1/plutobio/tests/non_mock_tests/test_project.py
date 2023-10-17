from plutobio import PlutoClient
import os
import pytest


@pytest.mark.django_db
def test_get_project(pluto_client: PlutoClient, project):
    # This test will not work because we don't allow the API to get this info.
    """Test to check if experiments can be listed."""
    fetched_experiment = pluto_client.get_project(project.uuid)
    assert len(fetched_experiment) != 0, "Response was not successful"


@pytest.mark.django_db
def test_list_projects(pluto_client: PlutoClient):
    """Test to check if experiments can be listed."""
    fetched_experiment = pluto_client.list_projects()
    assert len(fetched_experiment) != 0, "Response was not successful"


if __name__ == "__main__":
    pc = PlutoClient(token=os.environ["API_TOKEN"])
    test_list_projects(pc)
    # test_get_experiment(pc)
