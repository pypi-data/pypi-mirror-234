from plutobio import PlutoClient
import os

# List experiments
pc = PlutoClient(token=os.environ["API_TOKEN"])


def test_list_experiments():
    # Get experiment
    experiment = pc.list_experiments()
    assert len(experiment) != 0, "Response was not successful"


def test_get_experiment():
    # Get experiment
    experiment = pc.get_experiment(experiment_id="1")
    print(experiment)


# def test_create_experiment():
#     # Create experiment
#     experiment = pc.create_experiment()
#     print(experiment)

# def test_delete_experiment():
#     # Delete experiment
#     experiment = pc.delete_experiment(experiment_id="1")
#     print(experiment)

if __name__ == "__main__":
    test_list_experiments()
    test_get_experiment()

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
