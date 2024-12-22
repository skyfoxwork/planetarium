from rest_framework import serializers

from planetarium.models import AstronomyShow


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = (
            "id",
            "title",
            "theme",
            "description",
        )
