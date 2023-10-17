from plutobio import PlutoClient
import os
import pytest


@pytest.mark.django_db
def test_list_experiments(pluto_client: PlutoClient, experiment):
    """Test to check if experiments can be listed."""
    fetched_experiment = pluto_client.list_experiments()
    assert (fetched_experiment) != 0, "Response was not successful"


@pytest.mark.django_db
def test_get_valid_experiment(pluto_client: PlutoClient, experiment):
    """Test to check if experiments can be listed."""
    fetched_experiment = pluto_client.get_experiment(experiment.uuid)
    assert (fetched_experiment) != 0, "Response was not successful"


@pytest.mark.django_db
def test_get_invalid_uuid_format(pluto_client: PlutoClient):
    """Test to fetch an experiment with an invalid UUID format."""
    with pytest.raises(HTTPError) as exc_info:
        fetched_experiment = pluto_client.get_experiment("not_a_valid_uuid")
        assert fetched_experiment == None
