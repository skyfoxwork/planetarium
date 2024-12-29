from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class UserApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpassword123",
        )
        self.token_url = reverse("user:token_obtain_pair")
        self.register_url = reverse("user:create")
        self.me_url = reverse("user:manage")
        self.client = APIClient()

    def test_register_user_success(self):
        payload = {
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.json())
        self.assertNotIn("password", response.json())
        self.assertTrue(get_user_model().objects.filter(email=payload["email"]).exists())

    def test_register_user_invalid_email(self):
        payload = {
            "email": "notanemail",
            "password": "testpassword123",
        }
        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        payload = {
            "email": self.user.email,
            "password": "testpassword123",
        }
        response = self.client.post(self.token_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_login_invalid_credentials(self):
        payload = {
            "email": self.user.email,
            "password": "wrongpassword",
        }
        response = self.client.post(self.token_url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.json())

    def test_retrieve_user_unauthorized(self):
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user_authorized(self):
        token = self.client.post(self.token_url, {
            "email": self.user.email,
            "password": "testpassword123",
        }).json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["email"], self.user.email)

    def test_update_user_profile(self):
        token = self.client.post(self.token_url, {
            "email": self.user.email,
            "password": "testpassword123",
        }).json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        payload = {"email": "updated@example.com", "password": "newpassword123"}
        response = self.client.patch(self.me_url, payload)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload["email"])
        self.assertTrue(self.user.check_password(payload["password"]))

    def test_update_user_unauthorized(self):
        payload = {"email": "updated@example.com"}
        response = self.client.patch(self.me_url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
