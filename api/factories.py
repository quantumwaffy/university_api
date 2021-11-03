import factory

from . import models


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Group

    name = factory.Sequence(lambda n: f"Gr_{n}")


class AuditoriumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Auditorium

    number = factory.Sequence(lambda n: f"Aud_{n}")


class LectureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Lecture

    name = factory.Sequence(lambda n: f"Lecture_{n}")


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Student

    name = factory.Faker("name")
    email = factory.LazyAttribute(lambda person: "{}@gmail.com".format(person.name.lower().replace(" ", "_")))


class LectureGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LectureGroup
