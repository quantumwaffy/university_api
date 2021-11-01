import datetime
import random

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
    capacity = random.randint(0, 70)


class LectureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Lecture

    name = factory.Sequence(lambda n: f"Lecture_{n}")


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Student

    name = factory.Faker("name")
    email = factory.LazyAttribute(lambda person: "{}@gmail.com".format(person.name.lower().replace(" ", "_")))
    group = factory.SubFactory(GroupFactory)


class LectureGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LectureGroup

    lecture = factory.SubFactory(LectureFactory)
    group = factory.SubFactory(GroupFactory)
    auditorium = factory.SubFactory(AuditoriumFactory)
    start_datetime = factory.Faker(
        "date_between_dates",
        date_start=datetime.datetime(2021, 10, 8, 8, 0, 0),
        date_end=datetime.datetime(2021, 10, 18, 17, 0, 0),
    )
