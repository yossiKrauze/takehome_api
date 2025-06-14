import pytest
from app import application as app
from takehome_api.src.config.config import get_logger

logger = get_logger("test_appointment_creation")


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_book_appointment_success(client):
    response = client.post(
        "/appointment",
        json={
            "patient": {
                "first_name": "Cold",
                "last_name": "Play",
                "email": "cold.play@example.com",
                "state": "CA",
                "insurance": "Aetna"
            }
        }
    )

    assert response.status_code == 200
