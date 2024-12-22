from rest_framework import viewsets

from planetarium.models import (
    AstronomyShow,
    ShowTheme,
)

from planetarium.serializers import (
    AstronomyShowSerializer,
    ShowThemeSerializer,
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related("theme")
    serializer_class = AstronomyShowSerializer
