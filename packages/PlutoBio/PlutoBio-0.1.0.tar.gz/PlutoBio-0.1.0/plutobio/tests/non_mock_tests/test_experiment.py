from plutobio import PlutoClient
import os
import pytest


@pytest.mark.django_db
def test_list_experiments(pluto_client: PlutoClient, experiment):
    """Test to check if experiments can be listed."""
    fetched_experiment = pluto_client.list_experiments()
    assert len(fetched_experiment) != 0, "Response was not successful"


@pytest.mark.django_db
def test_get_experiment(pluto_client: PlutoClient, experiment):
    """Test to check if experiments can be listed."""
    fetched_experiment = pluto_client.get_experiment(experiment.uuid)
    assert len(fetched_experiment) != 0, "Response was not successful"


# if __name__ == "__main__":
#     pc = PlutoClient(token=os.environ["API_TOKEN"])
#     test_list_experiments(pc)
#     # test_get_experiment(pc)

"""
Get Data tables from different experiments
Get Plots
Get Computed Assay Data
Upload new results/Custom analysis (results will be csv, an image or an html file). Uploaded
as an attachment. Save them in a different GCS Bucket, so that we can fetch it inside an iframe.
Need to get a new domain name: plutodata.bio
Add an external option on the FE so that users can upload their external analysis and see it in the
pluto app.

"""
