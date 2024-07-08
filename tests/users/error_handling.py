from tests.base import BaseTest, client


class TestErrorHandling(BaseTest):

    def test_read_nonexistent_user(self):
        response = client.get("/users/999")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "User 999 not found")

    def test_delete_nonexistent_user(self):
        response = client.delete("/users/999")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "User 999 not found")

    def test_create_user_with_duplicate_email(self):
        response = client.post(
            "/users/",
            json={
                "username": "Alina",
                "email": "alina@example.com",
                "hashed_password": "hdjshfjhds",
            },
        )
        self.assertEqual(response.status_code, 201)
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
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertEqual(data["detail"], "Email already registered")
