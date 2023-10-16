from plutobio import PlutoClient
import os
import pytest


@pytest.fixture
def client():
    return PlutoClient(token=os.environ["API_TOKEN"])


def test_successful_get_request(client):
    response = client.get("lab/experiments/")


def test_successful_post_request(client):
    response = client.get("lab/experiments/")


def test_successful_put_request(client):
    response = client.get("lab/experiments/")


def test_successful_delete_request(client):
    response = client.get("lab/experiments/")


def test_invalid_endpoint(client):
    pass


def test_unauthorized_endpoint(client):
    pass
