import time
import pytest
from fastapi.testclient import TestClient
from app.main import app, TickManager


@pytest.fixture(scope="function", autouse=True)
def setup_tick_manager():
    """Ensure tick_manager is reset before each test."""
    app.state.tick_manager = TickManager()


client = TestClient(app)


def test_post_tick_success():
    """Tests if posting a tick returns 201 when within 60 seconds."""
    response = client.post(
        "/v1/ticks",
        json={
            "instrument": "IBM.N",
            "price": 143.82,
            "timestamp": int(time.time() * 1000),  # Current timestamp in ms
        },
    )
    assert response.status_code == 201


def test_post_tick_old():
    """Tests if posting an old tick returns 204."""
    response = client.post(
        "/v1/ticks",
        json={
            "instrument": "IBM.N",
            "price": 143.82,
            "timestamp": int((time.time() - 61) * 1000),  # 61 seconds old
        },
    )
    assert response.status_code == 204


def test_get_statistics_empty():
    """Tests if statistics return zero values when no ticks are in the last 60 seconds."""
    response = client.get("/v1/statistics")
    assert response.status_code == 200
    assert response.json() == {"avg": 0.0, "max": 0.0, "min": 0.0, "count": 0}


def test_get_statistics_with_ticks():
    """Tests if statistics return correct values when ticks are present."""
    client.post(
        "/v1/ticks",
        json={
            "instrument": "IBM.N",
            "price": 150.0,
            "timestamp": int(time.time() * 1000),
        },
    )
    client.post(
        "/v1/ticks",
        json={
            "instrument": "IBM.N",
            "price": 100.0,
            "timestamp": int(time.time() * 1000),
        },
    )
    response = client.get("/v1/statistics")
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 2
    assert data["avg"] == 125.0
    assert data["max"] == 150.0
    assert data["min"] == 100.0


def test_get_statistics_per_instrument():
    """Tests statistics for a specific instrument."""
    client.post(
        "/v1/ticks",
        json={
            "instrument": "AAPL.N",
            "price": 200.0,
            "timestamp": int(time.time() * 1000),
        },
    )
    response = client.get("/v1/statistics/AAPL.N")
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 1
    assert data["avg"] == 200.0
    assert data["max"] == 200.0
    assert data["min"] == 200.0


def test_old_ticks_are_removed():
    """Tests if old ticks are removed after 60 seconds and not included in statistics."""
    client.post(
        "/v1/ticks",
        json={
            "instrument": "IBM.N",
            "price": 175.0,
            "timestamp": int((time.time() - 61) * 1000),
        },
    )
    response = client.get("/v1/statistics/IBM.N")
    assert response.status_code == 200
    assert response.json()["count"] == 0  # Old tick should be ignored


def test_concurrent_requests():
    """Tests handling of concurrent tick submissions."""
    from concurrent.futures import ThreadPoolExecutor

    def post_tick():
        return client.post(
            "/v1/ticks",
            json={
                "instrument": "TSLA.N",
                "price": 800.0,
                "timestamp": int(time.time() * 1000),
            },
        )

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: post_tick(), range(10)))

    assert all(res.status_code == 201 for res in results)

    response = client.get("/v1/statistics/TSLA.N")
    assert response.json()["count"] == 10  # All 10 ticks should be counted
