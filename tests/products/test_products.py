import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.products.models import Product


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient, test_user):
    response = await client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 100,
            "user_id": test_user.id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["description"] == "Test Description"
    assert data["price"] == 100
    assert data["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient, test_user, session: AsyncSession):
    product = Product(
        name="Test Product",
        description="Test Description",
        price=100,
        user_id=test_user.id,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)

    response = await client.get(f"/products/{product.id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product.name
    assert data["description"] == product.description
    assert data["price"] == product.price
    assert data["user_id"] == product.user_id


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient, test_user, session: AsyncSession):
    product = Product(
        name="Test Product",
        description="Test Description",
        price=100,
        user_id=test_user.id,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)

    response = await client.put(
        f"/products/{product.id}/",
        json={
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 150,
            "user_id": test_user.id,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["description"] == "Updated Description"
    assert data["price"] == 150
    assert data["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_update_product_partial(
    client: AsyncClient, test_user, session: AsyncSession
):
    product = Product(
        name="Test Product",
        description="Test Description",
        price=100,
        user_id=test_user.id,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)

    response = await client.patch(
        f"/products/{product.id}/",
        json={"name": "Partially Updated Product"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Partially Updated Product"
    assert data["description"] == product.description
    assert data["price"] == product.price
    assert data["user_id"] == product.user_id


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient, test_user, session: AsyncSession):
    product = Product(
        name="Test Product",
        description="Test Description",
        price=100,
        user_id=test_user.id,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)

    response = await client.delete(f"/products/{product.id}/")
    assert response.status_code == 204

    # Проверка, что продукт действительно удален
    response = await client.get(f"/products/{product.id}/")
    assert response.status_code == 404
