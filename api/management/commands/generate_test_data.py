import datetime
import random

from django.core.management import BaseCommand
from django.db import transaction
from randomtimestamp import randomtimestamp

from api.factories import AuditoriumFactory, GroupFactory, LectureFactory, LectureGroupFactory, StudentFactory
from api.models import Auditorium, Group, Lecture, LectureGroup, Student

GROUP_COUNT = 5
AUDITORIUM_COUNT = 20
STUDENT_COUNT = 100
LECTURE_COUNT = 30
LESSON_COUNT = 200


class Command(BaseCommand):
    help = "Generates fake test data"

    @transaction.atomic
    def handle(self, *args, **options):
        models = [Student, LectureGroup, Group, Lecture, Auditorium]
        if any(api_model.objects.exists() for api_model in models):
            self.stdout.write("Deleting previous data...")
            list(map(lambda api_model: api_model.objects.all().delete(), models))
            self.stdout.write("Deleting done!")

        self.stdout.write("Creating data...")

        groups = []
        for _ in range(GROUP_COUNT):
            group = GroupFactory()
            groups.append(group)

        audiences = []
        for _ in range(AUDITORIUM_COUNT):
            auditorium = AuditoriumFactory(capacity=random.randint(0, 70))
            audiences.append(auditorium)

        lectures = []
        for _ in range(LECTURE_COUNT):
            lecture = LectureFactory()
            lectures.append(lecture)

        for _ in range(STUDENT_COUNT):
            random_group = random.choice(groups)
            StudentFactory(group=random_group)

        for _ in range(LESSON_COUNT):
            LectureGroupFactory(
                group=random.choice(groups),
                auditorium=random.choice(audiences),
                lecture=random.choice(lectures),
                start_datetime=randomtimestamp(
                    start=datetime.datetime(2021, 11, 5, 8, 0), end=datetime.datetime(2021, 12, 30, 17, 0)
                ),
            )

        self.stdout.write("Creating done!")
