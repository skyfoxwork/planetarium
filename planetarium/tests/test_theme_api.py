from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import ShowTheme
from planetarium.serializers import ShowThemeSerializer

THEME_URL = reverse("planetarium:theme-list")

def sample_theme(**params):
    defaults = {
        "name": "Sample theme",
    }
    defaults.update(params)

    return ShowTheme.objects.create(**defaults)


class UnauthenticatedThemeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(THEME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedThemeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_list_astronomy_shows(self):
        sample_theme()
        sample_theme()

        res = self.client.get(THEME_URL)

        theme = ShowTheme.objects.order_by("id")
        serializer = ShowThemeSerializer(theme, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_theme_detail_should_be_404(self):
        theme = sample_theme()
        res = self.client.get(THEME_URL + f"/{theme.id}/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_theme_forbidden(self):
        payload = {
            "name": "Simple theme",
        }
        res = self.client.post(THEME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminThemeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_theme(self):
        payload = {
            "name": "Simple theme",
        }
        res = self.client.post(THEME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
