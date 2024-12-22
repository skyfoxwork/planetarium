from rest_framework import viewsets

from planetarium.models import AstronomyShow
from planetarium.serializers import AstronomyShowSerializer


class AstronomyShowView(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related("theme")
    serializer_class = AstronomyShowSerializer
