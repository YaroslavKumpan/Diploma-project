# import os
# import unittest
# from unittest.mock import patch
#
# from fastapi.testclient import TestClient
#
# from core.conftest import SQLALCHEMY_DATABASE_URL
# from main import app
from tests.conftest import client, BaseTest


class TestErrorHandling(BaseTest):
    async def test_create_user_with_duplicate_email(self):
        response = await client.post(
            "/users/",
            json={
                "username": "Alina",
                "email": "alina@example.com",
                "hashed_password": "hdjshfjhds",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "alina@example.com"

        response = await client.post(
            "/users/",
            json={
                "username": "Alina2",
                "email": "alina@example.com",
                "hashed_password": "hdjshfjhds",
            },
        )
        assert response.status_code == 422
        data = response.json()
        assert data["detail"] == "Email already registered"

# class TestAPI(unittest.TestCase):
#
#     def setUp(self):
#         # Установите предварительные условия для тестов, например, создание тестовых данных.
#         self.client = TestClient(app)
#
#     def test_create_user(self):
#         url = self.client.app.url_path_for("create_user", item_id=1)
#         response = self.client.post(
#             url, json={"name": "Alice", "email": "alice@example.com"}
#         )
#         self.assertEqual(response.status_code, 201)
#
#         data = response.json()
#         self.assertEqual(data["name"], "Alice")
#         self.assertEqual(data["email"], "alice@example.com")
#         self.assertIn("id", data)
#
#     def test_read_user(self):
#         # Сначала создаем пользователя для теста получения
#         response = self.client.post(
#             "/users/", json={"name": "Bob", "email": "bob@example.com"}
#         )
#         user_id = response.json()["id"]
#
#         with (
#             patch(
#                 "models.User.get_full_info", return_value="user_info"
#             ) as mock_get_full_info,
#             patch("models.User.get_mega_full_info") as mock_get_mega_full_info,
#         ):
#             # Тестируем получение пользователя
#             response = self.client.get(f"/users/{user_id}")
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(data["name"], "Bob")
#         self.assertEqual(data["email"], "bob@example.com")
#         self.assertEqual(data["id"], user_id)
#         print(data)
#         mock_get_full_info.assert_called()
#         mock_get_mega_full_info.assert_not_called()
#
#     def test_delete_user(self):
#         # Сначала создаем пользователя для теста удаления
#         response = self.client.post(
#             "/users/", json={"name": "Charlie", "email": "charlie@example.com"}
#         )
#         user_id = response.json()["id"]
#
#         # Тестируем удаление пользователя
#         response = self.client.delete(f"/users/{user_id}")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()["detail"], "User deleted")
#
#         # Убеждаемся, что пользователь был удален
#         response = self.client.get(f"/users/{user_id}")
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json()["detail"], "User not found")
#
#     def tearDown(self):
#         if os.path.exists(SQLALCHEMY_DATABASE_URL):
#             os.remove(SQLALCHEMY_DATABASE_URL)
#
#
# class TestValidation(unittest.TestCase):
#
#     def setUp(self):
#         # Установите предварительные условия для тестов, например, создание тестовых данных.
#         self.client = TestClient(app)
#
#     def test_create_user_with_missing_name(self):
#         # Попытка создания пользователя без имени
#         response = self.client.post("/users/", json={"email": "alice@example.com"})
#         self.assertEqual(response.status_code, 422)
#         data = response.json()
#         self.assertIn("detail", data)
#         self.assertEqual(data["detail"][0]["loc"], ["body", "name"])
#         self.assertEqual(data["detail"][0]["msg"], "field required")
#
#     def test_create_user_with_invalid_email(self):
#         # Попытка создания пользователя с некорректным email
#         response = self.client.post(
#             "/users/", json={"name": "Alice", "email": "invalid-email"}
#         )
#         self.assertEqual(response.status_code, 422)
#         data = response.json()
#         self.assertIn("detail", data)
#         self.assertEqual(data["detail"][0]["loc"], ["body", "email"])
#         self.assertEqual(data["detail"][0]["msg"], "value is not a valid email address")
#
#     def test_create_user_with_missing_email(self):
#         # Попытка создания пользователя без email
#         response = self.client.post("/users/", json={"name": "Alice"})
#         self.assertEqual(response.status_code, 422)
#         data = response.json()
#         self.assertIn("detail", data)
#         self.assertEqual(data["detail"][0]["loc"], ["body", "email"])
#         self.assertEqual(data["detail"][0]["msg"], "field required")
#
#     def test_create_user_with_empty_body(self):
#         # Попытка создания пользователя с пустым телом запроса
#         response = self.client.post("/users/", json={})
#         self.assertEqual(response.status_code, 422)
#         data = response.json()
#         self.assertIn("detail", data)
#
#     def tearDown(self):
#         if os.path.exists(SQLALCHEMY_DATABASE_URL):
#             os.remove(SQLALCHEMY_DATABASE_URL)
#
#
# if __name__ == "__main__":
#     unittest.main()
