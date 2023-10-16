![Pluto Biosciences](https://cdn.bfldr.com/2Q1IPX6I/at/9tqz7c44mmwwqwqmbv2swjcw/pluto_bio_logo?format=auto=height=60)

# Pluto Python SDK: `py-pluto`

A Python Software Development Kit (SDK) for interacting with the [Pluto Bio](https://pluto.bio), a cloud computational biology platform.

Other resources:

- [Pluto.bio](https://pluto.bio)
- [Pluto R Package](https://github.com/pluto-biosciences/pluto-sdk-R).

- [Pluto API](https://docs.pluto.bio)

## Table of Contents

- [Installation](#installation)
  - [Using pip](#using-pip)
  - [Local Installation](#local-installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Initialize the Client](#initialize-the-client)
  - [Experiment Operations](#experiment-operations)
  - [Sample and Assay Data](#sample-and-assay-data)
  - [Plot Operations](#plot-operations)
  - [Attachment Operations](#attachment-operations)
- [Examples](#examples)
  - [Uploading a plot to Pluto Experiment using plotly](#example--uploading-a-plot-to-pluto-experiment-using-plotly)
  - [Update an already existing plot in an experiment](#example--update-an-already-existing-plot-in-an-experiment)
  - [List your experiments](#example--list-your-experiments)
  - [List attachments in an experiment](#example--list-attachments-in-an-experiment)
- [Development](#development)
  - [Build Distribution Package](#build-distribution-package)
  - [Install from Source](#install-from-source)
- [Help & Support](#help-and-support)

## Installation

### Using pip

To install the SDK using pip, run the following command:

```bash
pip install PyPluto
```

### Local Installation

For a local setup, you can use a Python virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Create an API key and set the environment variables to interact with the Pluto Bio platform. You can find your api token in the Pluto platform or visit [this help article](https://help.pluto.bio/en/articles/creating-your-api-token).

```bash
export PLUTO_API_URL=<API_URL>
export API_TOKEN=<API_TOKEN>
```

## Usage

### Initialize the Client

To start interacting with the Pluto Bio API, initialize the client with your API token.

```python
from plutobio import PlutoClient

pluto_bio = PlutoClient(token="YOUR_PLUTO_API_TOKEN")
```

### Experiment Operations

#### List Experiments

```python
experiments = pluto_bio.list_experiments()
```

#### Get a Specific Experiment

```python
experiment = pluto_bio.get_experiment("EXPERIMENT_UUID")
```

### Sample and Assay Data

#### Get Sample Data

```python
sample_data = pluto_bio.get_sample_data("EXPERIMENT_UUID", folder_path="data")
```

#### Get Assay Data

```python
assay_data = pluto_bio.get_assay_data("EXPERIMENT_UUID", folder_path="data")
```

### Plot Operations

#### List Plots

```python
plots = pluto_bio.list_plots("EXPERIMENT_UUID")
```

#### Get Data from a Plot

```python
plot_data = pluto_bio.get_plot_data("EXPERIMENT_UUID", "PLOT_UUID")
```

### Attachment Operations

#### List Attachments

```python
attachments = pluto_bio.list_attachments("EXPERIMENT_UUID")
```

#### Download Attachments

```python
attachment = pluto_bio.download_attachments("EXPERIMENT_UUID", "ATTACHMENT_UUID", folder_path="data")
```

#### Download QC report

```python
qc_report = pluto_bio.download_qc_report("PLX128193", folder_path="data")
```

#### Download BAM files

```python
bam_files = pluto_bio.download_bam_files("PLX128193", _bam_uuid, folder_path="data")
```

_Note: File will show up locally in your machine in a folder called data in the same directory where you ran the script_

## Examples

### Example : Uploading a plot to Pluto Experiment using plotly

```python
import plotly.graph_objects as go
from plotly.offline import plot

# Let's say we have the following plot

fruits = ["Apples", "Bananas", "Cherries", "Dates"]
quantities = [
    10,
    20,
    15,
    7,
]


# Create a bar plot
fig = go.Figure(
    data=[
        go.Bar(
            x=fruits,
            y=quantities,
            marker_color="red"
        )
    ]
)

# Customize the layout
fig.update_layout(
    title="Fruit Quantities",
    xaxis=dict(title="Fruit"),
    yaxis=dict(title="Quantity"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

plot(fig, filename="bar_plot.html", auto_open=False)

pc.add_plot(
    _experiment_uuid,
    file_path="bar_plot.html",
)


```

### Example : Update an already existing plot in an experiment

To update an existing plot in your experiment, you will need the figure uuid. To find out the uuid click on the 3 dots in the figure, and select the option methods. The uuid that you want is under plot analysis ID.

```python
import plotly.graph_objects as go
from plotly.offline import plot

# Let's say we have the following plot

fruits = ["Apples", "Bananas", "Cherries", "Dates"]
quantities = [
    10,
    20,
    15,
    7,
]


# Create a bar plot
fig = go.Figure(
    data=[
        go.Bar(
            x=fruits,
            y=quantities,
            marker_color="red"
        )
    ]
)

# Customize the layout
fig.update_layout(
    title="Fruit Quantities",
    xaxis=dict(title="Fruit"),
    yaxis=dict(title="Quantity"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

plot(fig, filename="bar_plot.html", auto_open=False)

pc.add_plot(
    _experiment_uuid,
    file_path="bar_plot.html",
    plot_id=<PLOT_UUID>  # example "6511b617-9a0e-4a61-bf30-a1f1eea7a2a4",
)


```

### Example : List your experiments

```python
from plutobio import PlutoClient
pluto_bio = PlutoClient(token="YOUR_PLUTO_API_TOKEN")

experiments = pluto_bio.list_experiments()

experiments = pluto_bio.list_experiments()
for experiment in experiments:
    print(f"Pluto ID: {experiment} | Name: {experiments[experiment].name}")


>>>> Pluto ID: PLX128193 | Name: Novel therapeutics inhibiting viral replication in SARS-CoV-2
>>>> Pluto ID: PLX122909 | Name: testing
>>>> Pluto ID: PLX004016 | Name: test-analysis-btn
>>>> Pluto ID: PLX176024 | Name: New test title
>>>> Pluto ID: PLX175808 | Name: Testing banners
>>>> Pluto ID: PLX169820 | Name: Iowa Test - Copy of Copy of PLX160374: Cut and Run TM ET H3K16Ac
>>>> Pluto ID: PLX174997 | Name: Copy of Iowa Test - Copy of Copy of PLX160374: Cut and Run TM ET H3K16Acdaf
```

### Example : List attachments in an experiment

```
from plutobio import PlutoClient
pluto_bio = PlutoClient(token="YOUR_PLUTO_API_TOKEN")

attachments = pluto_bio.list_attachments("PLX128193")
for attachment in attachments:
    print(f"Filename: {attachment.filename} | UUID: {attachment.uuid}")

>>>> Filename: SRR4238351_subsamp.fastq.gz | UUID: 634cd346-4674-4f3c-97ea-d17cf146453b
```

---

## Development

### Build Distribution Package

To build a distribution package, navigate to the project's root directory and run:

```bash
python setup.py sdist bdist_wheel
```

### Install from Source

It's recommended to use a virtual environment to install the Pluto SDK package from source.

```bash
python -m venv .venv
source .venv/bin/activate
pip install git+ssh://github.com/pluto-biosciences/py-pluto.git@VERSION_TAG
```

## Help and Support

For additional assistance please visit our [knowledge base](https://help.pluto.bio) or submit a support request via the [help portal](https://help.pluto.bio).
