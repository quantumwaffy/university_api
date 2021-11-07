from django.db import models


class Group(models.Model):
    name = models.CharField(verbose_name="Group name", max_length=8, unique=True)


class Student(models.Model):
    name = models.CharField(verbose_name="Student name", max_length=100)
    email = models.EmailField(verbose_name="E-mail")
    group = models.ForeignKey(Group, related_name="students", on_delete=models.SET_NULL, null=True)


class Lecture(models.Model):
    name = models.CharField(verbose_name="Lecture name", max_length=20, unique=True)
    group = models.ManyToManyField(Group, through="LectureGroup", through_fields=("lecture", "group"))


class Auditorium(models.Model):
    number = models.CharField(verbose_name="Auditorium number", max_length=8, unique=True)
    capacity = models.IntegerField(verbose_name="Auditorium capacity")


class LectureGroup(models.Model):
    lecture = models.ForeignKey(Lecture, related_name="lectures", on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, related_name="groups", on_delete=models.SET_NULL, null=True)
    auditorium = models.ForeignKey(Auditorium, related_name="audiences", on_delete=models.SET_NULL, null=True)
    start_datetime = models.DateTimeField(verbose_name="Start lecture")

    class Meta:
        ordering = ["start_datetime"]
