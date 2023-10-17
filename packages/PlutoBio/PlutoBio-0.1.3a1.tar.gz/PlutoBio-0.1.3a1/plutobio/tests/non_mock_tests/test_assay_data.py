from plutobio import PlutoClient
import os
import pytest


@pytest.mark.django_db
def test_get_assay_data(pluto_client: PlutoClient, simple_experiment_completed):
    """Test to check if experiments can be listed."""
    fetched_assay_data = pluto_client.get_assay_data(simple_experiment_completed.uuid)
    assert len(fetched_assay_data) != 0, "Response was not successful"


if __name__ == "__main__":
    pass
