import os
import unittest
from unittest.mock import patch, Mock

from fastapi.testclient import TestClient

from database import DB_PATH
from main import app


class TestAPI(unittest.TestCase):

    def setUp(self):
        # Установите предварительные условия для тестов, например, создание тестовых данных.
        self.client = TestClient(app)

    def test_create_user(self):
        url = self.client.app.url_path_for("create_user", item_id=1)
        response = self.client.post(
            url, json={"name": "Alice", "email": "alice@example.com"}
        )
        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertEqual(data["name"], "Alice")
        self.assertEqual(data["email"], "alice@example.com")
        self.assertIn("id", data)

    def test_read_user(self):
        # Сначала создаем пользователя для теста получения
        response = self.client.post(
            "/users/", json={"name": "Bob", "email": "bob@example.com"}
        )
        user_id = response.json()["id"]

        with (
            patch(
                "models.User.get_full_info", return_value="user_info"
            ) as mock_get_full_info,
            patch("models.User.get_mega_full_info") as mock_get_mega_full_info,
        ):
            # Тестируем получение пользователя
            response = self.client.get(f"/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Bob")
        self.assertEqual(data["email"], "bob@example.com")
        self.assertEqual(data["id"], user_id)
        print(data)
        mock_get_full_info.assert_called()
        mock_get_mega_full_info.assert_not_called()

    def test_delete_user(self):
        # Сначала создаем пользователя для теста удаления
        response = self.client.post(
            "/users/", json={"name": "Charlie", "email": "charlie@example.com"}
        )
        user_id = response.json()["id"]

        # Тестируем удаление пользователя
        response = self.client.delete(f"/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "User deleted")

        # Убеждаемся, что пользователь был удален
        response = self.client.get(f"/users/{user_id}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "User not found")

    def tearDown(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
