from django.urls import path, include

from rest_framework import routers

from planetarium.views import (
    AstronomyShowViewSet,
    ShowThemeViewSet,
)


router = routers.DefaultRouter()

router.register("themes", ShowThemeViewSet),
router.register("astronomy-shows", AstronomyShowViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium"
