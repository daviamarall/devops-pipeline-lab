"""DevOps Pipeline Lab — sample FastAPI service.

Small on purpose: the value of this repository is the CI/CD pipeline around it
(lint, tests, Docker build, image scanning and registry push via GitHub Actions).
"""

from __future__ import annotations

import os
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

app = FastAPI(
    title="DevOps Pipeline Lab",
    version=APP_VERSION,
    description="Sample service used to demonstrate build, test, scan and deploy automation.",
    contact={"name": "Davi Amaral", "url": "https://github.com/daviamarall"},
)


class Item(BaseModel):
    """A simple inventory item."""

    name: str = Field(..., min_length=1, max_length=80, examples=["widget"])
    price: float = Field(..., ge=0, examples=[9.99])


# In-memory storage — intentionally simple (no external dependencies).
_items: dict[str, Item] = {}


@app.get("/", tags=["info"], summary="Service metadata")
def root() -> dict:
    return {
        "service": "devops-pipeline-lab",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "time": datetime.now(UTC).isoformat(),
    }


@app.get("/healthz", tags=["health"], summary="Liveness probe")
def healthz() -> dict:
    return {"status": "healthy"}


@app.get("/readyz", tags=["health"], summary="Readiness probe")
def readyz() -> dict:
    return {"status": "ready"}


@app.get("/items", tags=["items"], summary="List items")
def list_items() -> dict:
    return {"count": len(_items), "items": _items}


@app.put(
    "/items/{item_id}",
    tags=["items"],
    status_code=status.HTTP_201_CREATED,
    summary="Create or update an item",
)
def upsert_item(item_id: str, item: Item) -> Item:
    _items[item_id] = item
    return item


@app.get("/items/{item_id}", tags=["items"], summary="Get an item by id")
def get_item(item_id: str) -> Item:
    if item_id not in _items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return _items[item_id]


@app.delete(
    "/items/{item_id}",
    tags=["items"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
)
def delete_item(item_id: str) -> None:
    _items.pop(item_id, None)
