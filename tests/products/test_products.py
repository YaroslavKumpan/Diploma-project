import pytest
from httpx import AsyncClient

from core.models import Base
from main import app
from core.models.db_helper import test_db_helper as db_helper


@pytest.fixture(autouse=True, scope="module")
async def setup_test_db():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def product_data():
    return {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 100,
        "user_id": 1
    }


@pytest.mark.asyncio
async def test_create_product(async_client, product_data):
    response = await async_client.post("/products/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["user_id"] == product_data["user_id"]


@pytest.mark.asyncio
async def test_get_product(async_client, product_data):
    response = await async_client.post("/products/", json=product_data)
    assert response.status_code == 201
    product_id = response.json()["id"]

    response = await async_client.get(f"/products/{product_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["user_id"] == product_data["user_id"]


@pytest.mark.asyncio
async def test_delete_product(async_client, product_data):
    response = await async_client.post("/products/", json=product_data)
    assert response.status_code == 201
    product_id = response.json()["id"]

    response = await async_client.delete(f"/products/{product_id}/")
    assert response.status_code == 204

    response = await async_client.get(f"/products/{product_id}/")
    assert response.status_code == 404
