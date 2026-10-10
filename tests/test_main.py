"""Tests for the DevOps Pipeline Lab API."""

from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_root_returns_service_metadata() -> None:
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "devops-pipeline-lab"
    assert "version" in body


def test_healthz() -> None:
    assert client.get("/healthz").json() == {"status": "healthy"}


def test_readyz() -> None:
    assert client.get("/readyz").json() == {"status": "ready"}


def test_item_lifecycle() -> None:
    payload = {"name": "widget", "price": 9.99}

    created = client.put("/items/42", json=payload)
    assert created.status_code == 201
    assert created.json() == payload

    fetched = client.get("/items/42")
    assert fetched.status_code == 200
    assert fetched.json() == payload

    listing = client.get("/items")
    assert listing.status_code == 200
    assert listing.json()["count"] >= 1


def test_get_missing_item_returns_404() -> None:
    assert client.get("/items/does-not-exist").status_code == 404


def test_delete_item() -> None:
    client.put("/items/tmp", json={"name": "tmp", "price": 1.0})
    assert client.delete("/items/tmp").status_code == 204
    assert client.get("/items/tmp").status_code == 404


def test_invalid_payload_returns_422() -> None:
    response = client.put("/items/bad", json={"name": "", "price": -1})
    assert response.status_code == 422
