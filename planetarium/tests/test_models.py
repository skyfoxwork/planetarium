from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from planetarium.models import (
    PlanetariumDome,
    ShowTheme,
    AstronomyShow,
    ShowSession,
    Reservation,
    Ticket
)

class TestPlanetariumModels(TestCase):

    def test_planetarium_dome_str(self):
        dome = PlanetariumDome.objects.create(
            name="Test Dome", rows=10, seats_in_row=20
        )
        self.assertEqual(str(dome), "Test Dome")

    def test_planetarium_dome_capacity(self):
        dome = PlanetariumDome.objects.create(
            name="Test Dome", rows=10, seats_in_row=20
        )
        self.assertEqual(dome.capacity, 200)

    def test_planetarium_dome_validation(self):
        dome = PlanetariumDome(name="Invalid Dome", rows=-1, seats_in_row=20)
        try:
            dome.full_clean()
        except ValidationError as e:
            self.assertEqual(
                str(e.detail["rows"]),
                "The number of rows must be a positive integer."
            )

        dome = PlanetariumDome(name="Invalid Dome", rows=10, seats_in_row=-1)
        try:
            dome.full_clean()
        except ValidationError as e:
            self.assertEqual(
                str(e.detail["seats_in_row"]),
                "The number of seats per row must be a positive integer."
            )

    def test_show_theme_str(self):
        theme = ShowTheme.objects.create(name="Space Exploration")
        self.assertEqual(str(theme), "Space Exploration")

    def test_astronomy_show_str(self):
        show = AstronomyShow.objects.create(
            title="Mars Show", description="A show about Mars"
        )
        self.assertEqual(str(show), "Mars Show")

    def test_show_session_str(self):
        user = get_user_model().objects.create_user("user@example.com", "password")
        dome = PlanetariumDome.objects.create(name="Test Dome", rows=10, seats_in_row=20)
        show = AstronomyShow.objects.create(title="Mars Show", description="A show about Mars")
        session = ShowSession.objects.create(
            astronomy_show=show,
            planetarium_dome=dome,
            show_time=timezone.now()
        )
        self.assertEqual(str(session), "Mars Show " + str(session.show_time))

    def test_reservation_str(self):
        user = get_user_model().objects.create_user("user@example.com", "password")
        reservation = Reservation.objects.create(user=user)
        self.assertEqual(str(reservation), str(reservation.created_at))

    def test_ticket_str(self):
        user = get_user_model().objects.create_user("user@example.com", "password")
        dome = PlanetariumDome.objects.create(name="Test Dome", rows=10, seats_in_row=20)
        show = AstronomyShow.objects.create(title="Mars Show", description="A show about Mars")
        session = ShowSession.objects.create(
            astronomy_show=show,
            planetarium_dome=dome,
            show_time=timezone.now()
        )
        reservation = Reservation.objects.create(user=user)
        ticket = Ticket.objects.create(
            row=2,
            seat=5,
            show_session=session,
            reservation=reservation
        )
        self.assertEqual(
            str(ticket),
            f"Mars Show {str(session.show_time)} (row: 2, seat: 5)"
        )


class TestTicketValidation(TestCase):
    def test_ticket_validation_invalid_row(self):
        user = get_user_model().objects.create_user("user@example.com", "password")
        dome = PlanetariumDome.objects.create(name="Test Dome", rows=10, seats_in_row=20)
        show = AstronomyShow.objects.create(title="Mars Show", description="A show about Mars")
        session = ShowSession.objects.create(
            astronomy_show=show,
            planetarium_dome=dome,
            show_time=timezone.now()
        )
        reservation = Reservation.objects.create(user=user)

        ticket = Ticket(row=11, seat=5, show_session=session, reservation=reservation)
        try:
            ticket.full_clean()
        except ValidationError as e:
            # print(e.detail["row"])
            self.assertEqual(
                str(e.detail["row"]),
                "row number must be in available range: (1, rows): (1, 10)"
            )

    def test_ticket_validation_invalid_seat(self):
        user = get_user_model().objects.create_user("user@example.com", "password")
        dome = PlanetariumDome.objects.create(name="Test Dome", rows=10, seats_in_row=20)
        show = AstronomyShow.objects.create(title="Mars Show", description="A show about Mars")
        session = ShowSession.objects.create(
            astronomy_show=show,
            planetarium_dome=dome,
            show_time=timezone.now()
        )
        reservation = Reservation.objects.create(user=user)

        ticket = Ticket(row=2, seat=21, show_session=session, reservation=reservation)
        try:
            ticket.full_clean()
        except ValidationError as e:
            self.assertEqual(
                str(e.detail["seat"]),
                "seat number must be in available range: (1, seats_in_row): (1, 20)"
            )
