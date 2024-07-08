# import os
# import unittest
# from unittest.mock import patch
#
# from fastapi.testclient import TestClient
#
# from core.conftest import SQLALCHEMY_DATABASE_URL
# from main import app


import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestErrorHandling(unittest.TestCase):

    def test_read_nonexistent_user(self):
        # Попытка получить данные несуществующего пользователя
        response = client.get("/users/999")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "User 999 not found")

    def test_delete_nonexistent_user(self):
        # Попытка удалить несуществующего пользователя
        response = client.delete("/users/999")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "User not found")

    def test_create_user_with_duplicate_email(self):
        # Создаем пользователя с email
        response = client.post(
            "/users/", json={"name": "Alice", "email": "alice@example.com"}
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["email"], "alice@example.com")

        # Попытка создать пользователя с таким же email
        response = client.post(
            "/users/", json={"name": "Alice2", "email": "alice@example.com"}
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"], "Email already registered")


if __name__ == "__main__":
    unittest.main()


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
