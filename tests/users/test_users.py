from tests.conftest import BaseTest, client


class TestUserCRUD(BaseTest):

    def test_create_user(self):
        # Проверяем успешное создание нового пользователя
        response = client.post(
            "/users/",
            json={
                "username": "TestUser",
                "email": "test.user@example.com",
                "hashed_password": "password123",
            },
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["username"], "TestUser")
        self.assertEqual(data["email"], "test.user@example.com")
        # Проверяем, что hashed_password не возвращается в ответе
        self.assertNotIn("hashed_password", data)  # Проверяем отсутствие поля hashed_password в ответе

    def test_read_user(self):
        # Проверяем возможность чтения данных пользователя
        response = client.post(
            "/users/",
            json={
                "username": "TestUser",
                "email": "test.user@example.com",
                "hashed_password": "password123",
            },
        )
        self.assertEqual(response.status_code, 201)
        user_id = response.json()["id"]

        response = client.get(f"/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["username"], "TestUser")
        self.assertEqual(data["email"], "test.user@example.com")
        # Проверяем, что hashed_password не возвращается в ответе
        self.assertNotIn("hashed_password", data)

    def test_update_user(self):
        # Проверяем возможность обновления данных пользователя
        response = client.post(
            "/users/",
            json={
                "username": "UpdateUser",
                "email": "update.user@example.com",
                "hashed_password": "password789",
            },
        )
        self.assertEqual(response.status_code, 201)
        user_id = response.json()["id"]

        response = client.put(
            f"/users/{user_id}",
            json={
                "username": "UpdatedUser",
                "email": "updated.user@example.com",
                "hashed_password": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["username"], "UpdatedUser")
        self.assertEqual(data["email"], "updated.user@example.com")
        self.assertEqual(data["hashed_password"], "newpassword123")

    def test_delete_user(self):
        # Проверяем возможность удаления пользователя
        response = client.post(
            "/users/",
            json={
                "username": "DeleteUser",
                "email": "delete.user@example.com",
                "hashed_password": "password000",
            },
        )
        self.assertEqual(response.status_code, 201)
        user_id = response.json()["id"]

        response = client.delete(f"/users/{user_id}")
        self.assertEqual(response.status_code, 204)

