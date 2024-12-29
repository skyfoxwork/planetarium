from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import PlanetariumDome
from planetarium.serializers import PlanetariumDomeSerializer

PLANETARIUM_DOME_URL = reverse("planetarium:planetarium-dome-list")

def sample_planetarium_dome(**params):
    defaults = {
        "name": "Main Dome",
        "rows": 20,
        "seats_in_row": 10,
    }
    defaults.update(params)

    return PlanetariumDome.objects.create(**defaults)


class UnauthenticatedPlanetariumDomeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLANETARIUM_DOME_URL)
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
        sample_planetarium_dome()
        sample_planetarium_dome()

        res = self.client.get(PLANETARIUM_DOME_URL)

        theme = PlanetariumDome.objects.order_by("id")
        serializer = PlanetariumDomeSerializer(theme, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_theme_detail_should_be_404(self):
        theme = sample_planetarium_dome()
        res = self.client.get(PLANETARIUM_DOME_URL + f"/{theme.id}/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_theme_forbidden(self):
        payload = {
            "name": "Main Dome",
            "rows": 20,
            "seats_in_row": 10,
        }
        res = self.client.post(PLANETARIUM_DOME_URL, payload)

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
            "name": "Main Dome",
            "rows": 20,
            "seats_in_row": 10,
        }
        res = self.client.post(PLANETARIUM_DOME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
