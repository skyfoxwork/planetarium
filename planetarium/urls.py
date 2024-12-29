from django.urls import path, include

from rest_framework import routers

from planetarium.views import (
    AstronomyShowViewSet,
    ShowThemeViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    ReservationViewSet,
)


router = routers.DefaultRouter()

router.register("themes", ShowThemeViewSet, basename="theme")
router.register(
    "planetarium-domes",
    PlanetariumDomeViewSet,
    basename="planetarium-dome"
)
router.register(
    "astronomy-shows",
    AstronomyShowViewSet,
    basename="astronomy-show"
)
router.register("show-sessions", ShowSessionViewSet, basename="show-session")
router.register("reservations", ReservationViewSet, basename="reservation")

urlpatterns = router.urls

app_name = "planetarium"
