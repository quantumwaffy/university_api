from rest_framework import serializers

from api import models


class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Auditorium
        exclude = ("id",)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        exclude = ("id",)


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lecture
        exclude = ("id",)


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LectureGroup
        exclude = ("id",)
