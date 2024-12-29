from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import Reservation
from planetarium.serializers import ReservationListSerializer


RESERVATION_SESSION_URL = reverse("planetarium:reservation-list")


class UnauthenticatedReservationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RESERVATION_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowSessionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_list_reservation(self):
        Reservation.objects.create(user=self.user)
        Reservation.objects.create(user=self.user)

        res = self.client.get(RESERVATION_SESSION_URL)

        reservation = Reservation.objects.all()

        serializer = ReservationListSerializer(reservation, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)


    def test_retrieve_test_list_reservation_detail_should_be_404(self):
        reservation = Reservation.objects.create(user=self.user)
        res = self.client.get(RESERVATION_SESSION_URL + f"/{reservation.id}/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
