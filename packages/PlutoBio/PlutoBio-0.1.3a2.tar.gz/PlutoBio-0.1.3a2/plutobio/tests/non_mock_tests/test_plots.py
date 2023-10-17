from plutobio import PlutoClient
import os
import pytest


@pytest.mark.django_db
def test_list_plots(pluto_client: PlutoClient, experiment, assay_summary_plot):
    """Test to check if experiments can be listed."""
    fetched_experiment = pluto_client.list_plots(experiment.uuid)
    assert len(fetched_experiment) != 0, "Response was not successful"


@pytest.mark.django_db
def test_get_plot(pluto_client: PlutoClient, experiment, assay_summary_plot):
    """Test to check if experiments can be listed."""
    fetched_experiment = pluto_client.get_plot(experiment.uuid, assay_summary_plot.uuid)
    assert len(fetched_experiment) != 0, "Response was not successful"
