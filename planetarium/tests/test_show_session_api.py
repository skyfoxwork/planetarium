from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, re_path

from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import (
    AstronomyShow, ShowTheme,
    PlanetariumDome,
    ShowSession,
)
from planetarium.serializers import (
    ShowSessionListSerializer,
    ShowSessionDetailSerializer,
)

SHOW_SESSION_URL = reverse("planetarium:show-session-list")

def sample_show_session(**params):
    planetarium_dome = PlanetariumDome.objects.create(
        name="Main Dome", rows=20, seats_in_row=20
    )

    astronomy_show = AstronomyShow.objects.create(
        title="Show", description="Description", image=None
    )

    theme = ShowTheme.objects.create(name="Theme")
    astronomy_show.theme.add(theme)

    defaults = {
        "show_time": "2022-06-02 14:00:00",
        "astronomy_show": astronomy_show,
        "planetarium_dome": planetarium_dome,
    }

    defaults.update(params)

    return ShowSession.objects.create(**defaults)


def detail_url(astronomy_show_id):
    return reverse("planetarium:show-session-detail", args=[astronomy_show_id])


class UnauthenticatedShowSessionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SHOW_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowSessionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_list_show_sessions(self):
        sample_show_session()
        sample_show_session()

        res = self.client.get(SHOW_SESSION_URL)

        show_sessions = ShowSession.objects.all()

        serializer = ShowSessionListSerializer(show_sessions, many=True)

        for show_session_data in serializer.data:
            show_session_data.update({"tickets_available": show_session_data["planetarium_dome_capacity"]})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_retrieve_show_session_detail(self):
        show_session = sample_show_session()

        url = detail_url(show_session.id)
        res = self.client.get(url)

        show_session_db =  ShowSession.objects.get(pk=show_session.id)
        serializer = ShowSessionDetailSerializer(show_session_db)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_show_session_forbidden(self):
        sample_show_session()

        payload = {
            "astronomy_show": 1,
            "planetarium_dome": 1,
            "show_time": "2024-12-25 20:00:00"
        }
        res = self.client.post(SHOW_SESSION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAstronomyShowSessionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_astronomy_show(self):
        sample_show_session()

        payload = {
            "astronomy_show": 1,
            "planetarium_dome": 1,
            "show_time": "2024-12-25 20:00:00"
        }
        res = self.client.post(SHOW_SESSION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
