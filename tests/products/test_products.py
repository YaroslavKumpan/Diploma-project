from tests.conftest import BaseTest, client


class TestProductCRUD(BaseTest):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        # Создаем пользователя с id=1
        response = client.post(
            "/users/",
            json={
                "username": "TestUser",
                "email": "test.user@example.com",
                "hashed_password": "password123",
            },
        )
        assert response.status_code == 201
        self.user_id = response.json()["id"]

    def test_create_product(self):
        response = client.post(
            "/products/",
            json={
                "name": "Test Product",
                "description": "A product for testing.",
                "price": 100,
                "user_id": self.user_id  # Используем созданного пользователя
            },
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["name"], "Test Product")
        self.assertEqual(data["description"], "A product for testing.")
        self.assertEqual(data["price"], 100)
        self.assertEqual(data["user_id"], self.user_id)

    def test_read_product(self):
        response = client.post(
            "/products/",
            json={
                "name": "Test Product",
                "description": "A product for testing.",
                "price": 100,
                "user_id": self.user_id
            },
        )
        self.assertEqual(response.status_code, 201)
        product_id = response.json()["id"]

        response = client.get(f"/products/{product_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test Product")
        self.assertEqual(data["description"], "A product for testing.")
        self.assertEqual(data["price"], 100)
        self.assertEqual(data["user_id"], self.user_id)

    def test_update_product(self):
        response = client.post(
            "/products/",
            json={
                "name": "Update Product",
                "description": "Product to be updated.",
                "price": 200,
                "user_id": self.user_id
            },
        )
        self.assertEqual(response.status_code, 201)
        product_id = response.json()["id"]

        response = client.put(
            f"/products/{product_id}",
            json={
                "name": "Updated Product",
                "description": "Updated description.",
                "price": 250,
                "user_id": self.user_id  # Обязательно добавьте user_id при обновлении
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Updated Product")
        self.assertEqual(data["description"], "Updated description.")
        self.assertEqual(data["price"], 250)

    def test_delete_product(self):
        response = client.post(
            "/products/",
            json={
                "name": "Delete Product",
                "description": "Product to be deleted.",
                "price": 300,
                "user_id": self.user_id
            },
        )
        self.assertEqual(response.status_code, 201)
        product_id = response.json()["id"]

        response = client.delete(f"/products/{product_id}")
        self.assertEqual(response.status_code, 204)
