from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CustomerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword",
            "first_name": "John",
            "last_name": "Doe",
        }

    def test_customer_login(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        response = self.client.post(
            "/api/auth/",
            data={
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    def test_customer_profile(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        self.client.force_authenticate(user=user)
        response = self.client.get("/api/users/me/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("email" in response.data)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_customer_logout(self):
        user = User.objects.create_user(**self.user_data)
        refresh_token = RefreshToken.for_user(user)
        self.client.force_authenticate(user=user)

        refresh_response = self.client.post("/api/users/token/refresh/", follow=True)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        access_token = refresh_response.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_customer_list(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        response = self.client.get("/api/users/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        self.assertTrue(len(response.data) > 0)

    def test_customer_retrieval(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        response = self.client.get(f"/api/users/{user.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("email" in response.data)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_customer_deletion(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        response = self.client.delete(f"/api/users/{user.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
