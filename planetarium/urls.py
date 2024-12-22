from django.urls import path, include
from planetarium.views import AstronomyShowView
from rest_framework import routers

router = routers.DefaultRouter()

router.register("astronomy-shows", AstronomyShowView)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium"
