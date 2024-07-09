from tests.conftest import BaseTest, client


class TestErrorHandling(BaseTest):

    def test_read_nonexistent_user(self):
        # Проверяем обработку запроса на чтение несуществующего пользователя
        response = client.get("/users/999")
        self.assertEqual(response.status_code, 404)  # Ожидаем код ответа 404 Not Found
        data = response.json()
        self.assertEqual(data["detail"], "User 999 not found")

    def test_delete_nonexistent_user(self):
        # Проверяем обработку запроса на удаление несуществующего пользователя
        response = client.delete("/users/999")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "User 999 not found")

    def test_create_user_with_duplicate_email(self):
        # Проверяем обработку попытки создания пользователя с уже зарегистрированным email
        response = client.post(
            "/users/",
            json={
                "username": "Alina",
                "email": "alina@example.com",
                "hashed_password": "hdjshfjhds",
            },
        )
        self.assertEqual(response.status_code, 201)  # Ожидаем успешное создание пользователя
        data = response.json()
        self.assertEqual(data["email"], "alina@example.com")

        response = client.post(
            "/users/",
            json={
                "username": "Alina2",
                "email": "alina@example.com",
                "hashed_password": "hdjshfjhds",
            },
        )
        self.assertEqual(response.status_code, 422)  # Ожидаем код ответа 422 Unprocessable Entity
        data = response.json()
        self.assertEqual(data["detail"], "Email already registered")  # Проверяем сообщение об ошибке

    def test_create_user_with_duplicate_username(self):
        # Проверяем обработку попытки создания пользователя с уже зарегистрированным username
        response = client.post(
            "/users/",
            json={
                "username": "Alina",
                "email": "alina@example.com",
                "hashed_password": "hdjshfjhds",
            },
        )
        self.assertEqual(response.status_code, 201)  # Ожидаем успешное создание пользователя
        data = response.json()
        self.assertEqual(data["username"], "Alina")

        response = client.post(
            "/users/",
            json={
                "username": "Alina",
                "email": "alina1@example.com",
                "hashed_password": "hdjshfjhds",
            },
        )
        self.assertEqual(response.status_code, 422)  # Ожидаем код ответа 422 Unprocessable Entity
        data = response.json()
        self.assertEqual(data["detail"], "Username already registered")  # Проверяем сообщение об ошибке
