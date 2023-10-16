from plutobio import PlutoClient
import os
import pytest
import django
from django.test import Client

from user.tests.factories import UserFactory
from lab.tests.factories import (
    ProjectFactory,
    ExperimentFactory,
    PlotFactory,
    ExperimentTypeFactory,
    CompletedSimpleExperiment,
)
from auth.models import PlutoToken
from improved_permissions.shortcuts import assign_role
from lab.roles import ExperimentEditor, ProjectOwner

from lab.models import (
    ANALYSIS_TYPE_ASSAY_SUMMARY,
    ANALYSIS_TYPE_ASSAY_SUMMARY_CPM_NORMALIZED,
    ANALYSIS_TYPE_DIFFERENTIAL_EXPRESSION,
    ANALYSIS_TYPE_IMAGE_ANALYSIS,
    ANALYSIS_TYPE_PRINCIPAL_COMPONENTS_ANALYSIS,
    ANALYSIS_TYPE_GENE_SET_ENRICHMENT_ANALYSIS,
    ANALYSIS_TYPE_SURVIVAL_ANALYSIS,
    ANALYSIS_TYPE_UMAP_ANALYSIS,
    ANALYSIS_TYPE_CLUSTERING_ANALYSIS,
)

django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pluto.settings")


@pytest.fixture
def test_client():
    """Fixture for Django test client."""
    return Client()


@pytest.fixture
def project(user):
    """Fixture for creating a project."""
    project = ProjectFactory()
    assign_role(user, ProjectOwner, project)
    return project


@pytest.fixture
def user():
    """Fixture for creating a test user."""
    password = "Password1"
    return UserFactory(email="foo@example.com", password=password)


@pytest.fixture
def experiment(project, user, simple_experiment_type):
    """Fixture for creating an experiment."""
    return ExperimentFactory(
        project=project, created_by=user, type=simple_experiment_type
    )


@pytest.fixture
def pluto_client(test_client, user, experiment):
    """Fixture for creating a Pluto client."""
    # assign_role(user, ExperimentEditor, experiment)
    access_token = PlutoToken.objects.create(user=user)
    return PlutoClient(token=access_token.key, test_client=test_client)


@pytest.fixture
def assay_summary_plot(experiment):
    """Fixture for creating a plot"""
    plot = PlotFactory(experiment=experiment, analysis_type=ANALYSIS_TYPE_ASSAY_SUMMARY)
    return plot


@pytest.fixture
def simple_experiment_type():
    return ExperimentTypeFactory(shortname="simple")


@pytest.fixture
def simple_experiment_completed(user):
    experiment = CompletedSimpleExperiment()
    assign_role(user, ExperimentEditor, experiment)
    return experiment
