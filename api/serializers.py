from rest_framework import serializers

from api import models


class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Auditorium
        fields = "__all__"


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lecture
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(queryset=models.Group.objects.all(), slug_field="name")

    class Meta:
        model = models.Student
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Group
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    lecture = serializers.SlugRelatedField(queryset=models.Lecture.objects.all(), slug_field="name")
    group = serializers.SlugRelatedField(queryset=models.Group.objects.all(), slug_field="name")
    auditorium = serializers.SlugRelatedField(queryset=models.Auditorium.objects.all(), slug_field="number")

    class Meta:
        model = models.LectureGroup
        fields = "__all__"
