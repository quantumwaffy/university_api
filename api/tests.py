import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api import models, serializers


class ApiTests(APITestCase):
    def auth(self):
        user = User.objects.create_user("testapi", "12345")
        self.client.force_authenticate(user)

    def setUp(self) -> None:
        self.auditorium = models.Auditorium.objects.create(number="A1", capacity=22)
        self.group = models.Group.objects.create(name="Gr1")
        self.student = models.Student.objects.create(name="St_test", email="st_test@gmail.com", group=self.group)
        self.lecture = models.Lecture.objects.create(name="Lec1")
        self.schedule = models.LectureGroup.objects.create(
            auditorium=self.auditorium,
            group=self.group,
            lecture=self.lecture,
            start_datetime=datetime.datetime(2021, 10, 7, 14, 0),
        )

    def test_auditorium_list(self):
        url = reverse("auditorium_list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), models.Auditorium.objects.count())

    def test_auditorium_retrieve(self):
        url = reverse("auditorium_detail", kwargs={"auditorium_id": self.auditorium.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializers.AuditoriumSerializer(self.auditorium).data))

    def test_auditorium_update_with_auth(self):
        self.auth()
        url = reverse("auditorium_detail", kwargs={"auditorium_id": self.auditorium.pk})
        data = {"number": "A2", "capacity": 25}
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Auditorium.objects.first().number, data.get("number"))
        self.assertEqual(models.Auditorium.objects.first().capacity, data.get("capacity"))

    def test_auditorium_update_without_auth(self):
        url = reverse("auditorium_detail", kwargs={"auditorium_id": self.auditorium.pk})
        data = {"number": "A2", "capacity": 25}
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auditorium_destroy_with_auth(self):
        self.auth()
        url = reverse("auditorium_detail", kwargs={"auditorium_id": self.auditorium.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Auditorium.objects.count(), 0)

    def test_auditorium_destroy_without_auth(self):
        url = reverse("auditorium_detail", kwargs={"auditorium_id": self.auditorium.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auditorium_create_with_auth(self):
        self.auth()
        url = reverse("auditorium_create")
        data = {"number": "A4", "capacity": 26}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Auditorium.objects.last().number, data.get("number"))
        self.assertEqual(models.Auditorium.objects.last().capacity, data.get("capacity"))

    def test_auditorium_create_without_auth(self):
        url = reverse("auditorium_create")
        data = {"number": "A4", "capacity": 26}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auditorium_create_exists(self):
        self.auth()
        url = reverse("auditorium_create")
        data = {"number": "A1", "capacity": 26}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_group_list(self):
        url = reverse("group_list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), models.Group.objects.count())

    def test_group_retrieve(self):
        url = reverse("group_detail", kwargs={"group_id": self.group.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializers.GroupSerializer(self.group).data))

    def test_group_update_with_auth(self):
        self.auth()
        url = reverse("group_detail", kwargs={"group_id": self.group.pk})
        data = {"name": "Gr2"}
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Group.objects.first().name, data.get("name"))

    def test_group_update_without_auth(self):
        url = reverse("group_detail", kwargs={"group_id": self.group.pk})
        data = {"name": "Gr2"}
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_group_destroy_with_auth(self):
        self.auth()
        url = reverse("group_detail", kwargs={"group_id": self.group.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Group.objects.count(), 0)

    def test_group_destroy_without_auth(self):
        url = reverse("group_detail", kwargs={"group_id": self.group.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_group_create_with_auth(self):
        self.auth()
        url = reverse("group_create")
        data = {"name": "Gr2"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Group.objects.last().name, data.get("name"))

    def test_group_create_without_auth(self):
        url = reverse("group_create")
        data = {"name": "Gr2"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_group_create_exists(self):
        self.auth()
        url = reverse("group_create")
        data = {"name": "Gr1"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_student_list(self):
        url = reverse("student_list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), models.Student.objects.count())

    def test_student_retrieve(self):
        url = reverse("student_detail", kwargs={"student_id": self.student.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializers.StudentSerializer(self.student).data))

    def test_student_update_with_auth(self):
        self.auth()
        url = reverse("student_detail", kwargs={"student_id": self.student.pk})
        data = {"name": "St_test1", "email": "st_test1@gmail.com"}
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Student.objects.first().name, data.get("name"))
        self.assertEqual(models.Student.objects.first().email, data.get("email"))

    def test_student_update_without_auth(self):
        url = reverse("student_detail", kwargs={"student_id": self.student.pk})
        data = {"name": "St_test1", "email": "st_test1@gmail.com"}
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student_destroy_with_auth(self):
        self.auth()
        url = reverse("student_detail", kwargs={"student_id": self.student.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Student.objects.count(), 0)

    def test_student_destroy_without_auth(self):
        url = reverse("student_detail", kwargs={"student_id": self.student.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student_create_with_auth(self):
        self.auth()
        url = reverse("student_create")
        group_name = models.Group.objects.create(name="Gr2").name
        data = {"name": "St_test1", "email": "st_test1@gmail.com", "group": group_name}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Student.objects.last().name, data.get("name"))
        self.assertEqual(models.Student.objects.last().email, data.get("email"))
        self.assertEqual(models.Student.objects.last().group.name, data.get("group"))

    def test_student_create_without_auth(self):
        url = reverse("student_create")
        group_name = models.Group.objects.create(name="Gr2").name
        data = {"name": "St_test1", "email": "st_test1@gmail.com", "group": group_name}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lecture_list(self):
        url = reverse("lecture_list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), models.Lecture.objects.count())

    def test_lecture_retrieve(self):
        url = reverse("lecture_detail", kwargs={"lecture_id": self.lecture.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializers.LectureSerializer(self.lecture).data))

    def test_lecture_update_with_auth(self):
        self.auth()
        url = reverse("lecture_detail", kwargs={"lecture_id": self.lecture.pk})
        data = {"name": "Lec2"}
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Lecture.objects.first().name, data.get("name"))

    def test_lecture_update_without_auth(self):
        url = reverse("lecture_detail", kwargs={"lecture_id": self.lecture.pk})
        data = {"name": "Lec2"}
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lecture_destroy_with_auth(self):
        self.auth()
        url = reverse("lecture_detail", kwargs={"lecture_id": self.lecture.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Lecture.objects.count(), 0)

    def test_lecture_destroy_without_auth(self):
        url = reverse("lecture_detail", kwargs={"lecture_id": self.lecture.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lecture_create_with_auth(self):
        self.auth()
        url = reverse("lecture_create")
        data = {"name": "Lec2"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Lecture.objects.last().name, data.get("name"))

    def test_lecture_create_without_auth(self):
        url = reverse("lecture_create")
        data = {"name": "Lec2"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lecture_create_exists(self):
        self.auth()
        url = reverse("lecture_create")
        data = {"name": "Lec1"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_schedule_list(self):
        url = reverse("schedule_list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), models.LectureGroup.objects.count())

    def test_schedule_retrieve(self):
        url = reverse("schedule_detail", kwargs={"schedule_id": self.schedule.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializers.ScheduleSerializer(self.schedule).data))

    def test_schedule_update_with_auth(self):
        self.auth()
        url = reverse("schedule_detail", kwargs={"schedule_id": self.schedule.pk})
        group_name = models.Group.objects.create(name="Gr2").name
        lecture_name = models.Lecture.objects.create(name="Lec2").name
        auditorium_number = models.Auditorium.objects.create(number="A2", capacity=55).number
        data = {
            "group": group_name,
            "lecture": lecture_name,
            "auditorium": auditorium_number,
            "start_datetime": datetime.datetime(2021, 10, 8, 11, 0),
        }
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.LectureGroup.objects.first().group.name, data.get("group"))
        self.assertEqual(models.LectureGroup.objects.first().lecture.name, data.get("lecture"))
        self.assertEqual(models.LectureGroup.objects.first().auditorium.number, data.get("auditorium"))
        self.assertEqual(models.LectureGroup.objects.first().start_datetime, data.get("start_datetime"))

    def test_schedule_update_without_auth(self):
        url = reverse("schedule_detail", kwargs={"schedule_id": self.schedule.pk})
        group_name = models.Group.objects.create(name="Gr2").name
        lecture_name = models.Lecture.objects.create(name="Lec2").name
        auditorium_number = models.Auditorium.objects.create(number="A2", capacity=55).number
        data = {
            "group": group_name,
            "lecture": lecture_name,
            "auditorium": auditorium_number,
            "start_datetime": datetime.datetime(2021, 10, 8, 11, 0),
        }
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_schedule_destroy_with_auth(self):
        self.auth()
        url = reverse("schedule_detail", kwargs={"schedule_id": self.schedule.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.LectureGroup.objects.count(), 0)

    def test_schedule_destroy_without_auth(self):
        url = reverse("schedule_detail", kwargs={"schedule_id": self.schedule.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_schedule_create_with_auth(self):
        self.auth()
        url = reverse("schedule_create")
        group_name = models.Group.objects.create(name="Gr2").name
        lecture_name = models.Lecture.objects.create(name="Lec2").name
        auditorium_number = models.Auditorium.objects.create(number="A2", capacity=55).number
        data = {
            "group": group_name,
            "lecture": lecture_name,
            "auditorium": auditorium_number,
            "start_datetime": datetime.datetime(2021, 10, 8, 11, 0),
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.LectureGroup.objects.last().group.name, data.get("group"))
        self.assertEqual(models.LectureGroup.objects.last().lecture.name, data.get("lecture"))
        self.assertEqual(models.LectureGroup.objects.last().auditorium.number, data.get("auditorium"))
        self.assertEqual(models.LectureGroup.objects.last().start_datetime, data.get("start_datetime"))

    def test_schedule_create_without_auth(self):
        url = reverse("schedule_create")
        group_name = models.Group.objects.create(name="Gr2").name
        lecture_name = models.Lecture.objects.create(name="Lec2").name
        auditorium_number = models.Auditorium.objects.create(number="A2", capacity=55).number
        data = {
            "group": group_name,
            "lecture": lecture_name,
            "auditorium": auditorium_number,
            "start_datetime": datetime.datetime(2021, 10, 8, 11, 0),
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_date_schedule(self):
        url = reverse("get_date_schedule")
        data = {"schedule_date": datetime.date(2021, 10, 7), "schedule_group": self.group.name}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_date_schedule_without_date(self):
        url = reverse("get_date_schedule")
        data = {"schedule_group": self.group.name}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_date_schedule_with_incorrect_date(self):
        url = reverse("get_date_schedule")
        data = {"schedule_date": self.schedule.start_datetime, "schedule_group": self.group.name}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_date_schedule_without_group(self):
        url = reverse("get_date_schedule")
        data = {"schedule_date": self.schedule.start_datetime.date()}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_date_schedule_with_not_exists_group(self):
        url = reverse("get_date_schedule")
        data = {"schedule_group": "Gr2", "schedule_date": self.schedule.start_datetime.date()}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
