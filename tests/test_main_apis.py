import pytest

from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    """Fixture to provide TestClient for FastAPI app."""
    return TestClient(app)


def test_get_highest_price(client):
    """
    # Test for the highest price endpoint
    :param client: Fixture for FastAPI client
    A new :param db: Can be introduced for Fixture for injecting test-db
    """

    # Make the GET request to the endpoint
    response = client.get("/v1/stock/AAPL/highest-price")

    # Assert the status code and response
    assert response.status_code == 200
    assert response.json() == {"highest_price": 236.2201}


def test_get_highest_price_not_found(client):
    # Test when no data exists for the ticker
    response = client.get("/v1/stock/XYZ/highest-price")

    # Assert 404 error
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticker not found or no data available"}
