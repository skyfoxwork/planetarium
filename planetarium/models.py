from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from planetarium.utils import astronomy_show_image_path


class PlanetariumDome(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[
            MaxLengthValidator(
                255,
                "The planetarium name must not exceed 255 characters."
            ),
            MinLengthValidator(
                1,
                "The planetarium name cannot be empty."
            )
        ]
    )
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    @staticmethod
    def validate_rows_and_seats(rows, seats_in_row):
        if rows <= 0:
            raise ValidationError(
                {"rows": "The number of rows must be a positive integer."}
            )
        if seats_in_row <= 0:
            raise ValidationError(
                {
                    "seats_in_row": (
                        "The number of seats per row "
                        "must be a positive integer."
                    )
                }
            )

    def clean(self):
        PlanetariumDome.validate_rows_and_seats(self.rows, self.seats_in_row)

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(PlanetariumDome, self).save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def __str__(self):
        return self.name


class ShowTheme(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[
            MaxLengthValidator(
                255,
                "The theme name must not exceed 255 characters."
            ),
            MinLengthValidator(
                1,
                "The theme name cannot be empty."
            )
        ]
    )

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(
        max_length=255,
        validators=[
            MaxLengthValidator(
                255,
                "The astronomy show title must not exceed 255 characters."
            ),
            MinLengthValidator(
                1,
                "The astronomy show title cannot be empty."
            )
        ]
    )
    description = models.TextField()
    theme = models.ManyToManyField(ShowTheme, blank=True, related_name="shows")
    image = models.ImageField(null=True, upload_to=astronomy_show_image_path)

    def __str__(self):
        return self.title


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        AstronomyShow,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    planetarium_dome = models.ForeignKey(
        PlanetariumDome,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    show_time = models.DateTimeField()

    def __str__(self):
        return self.astronomy_show.title + " " + str(self.show_time)


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        ShowSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    @staticmethod
    def validate_ticket(row, seat, planetarium_dome, error_to_raise):
        for (
                ticket_attr_value, ticket_attr_name, planetarium_dome_attr_name
        ) in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(planetarium_dome, planetarium_dome_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {planetarium_dome_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.show_session.planetarium_dome,
            ValidationError,
        )

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (
            f"{str(self.show_session)} (row: {self.row}, seat: {self.seat})"
        )

    class Meta:
        unique_together = ("show_session", "row", "seat")
        ordering = ["row", "seat"]
