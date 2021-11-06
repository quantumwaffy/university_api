import datetime

from django.contrib.postgres.aggregates import ArrayAgg
from django.core.mail import send_mail

from api import models
from university_api import settings
from university_api.celery import app


@app.task
def send_lecture_schedule_to_email():
    tomorrow_day = datetime.date.today() + datetime.timedelta(days=1)
    schedule = (
        models.LectureGroup.objects.select_related("lecture", "group", "auditorium")
        .filter(
            start_datetime__range=[
                datetime.datetime.combine(tomorrow_day, datetime.time.min),
                datetime.datetime.combine(tomorrow_day, datetime.time.max),
            ],
            group_id__isnull=False,
            lecture_id__isnull=False,
            auditorium_id__isnull=False,
            group__students__email__isnull=False,
        )
        .values("group__name", "lecture__name", "auditorium__number", "start_datetime")
        .annotate(student_emails=ArrayAgg("group__students__email"))
    )
    if schedule:
        dict_schedule = {
            obj["group__name"]: {"student_emails": obj["student_emails"], "lectures": []} for obj in schedule
        }
        list(
            map(
                lambda obj: dict_schedule[obj["group__name"]]["lectures"].append(
                    {obj["lecture__name"]: {obj["auditorium__number"]: obj["start_datetime"]}}
                ),
                schedule,
            )
        )
        for group_name, group_info in dict_schedule.items():
            message_text = "Good evening. Tomorrow these lectures are waiting for you:\n"
            for lecture in group_info.get("lectures"):
                for lecture_name, lecture_info in lecture.items():
                    message_text += f"\nLecture: {lecture_name}\n"
                    for auditory_name, lecture_start_datetime in lecture_info.items():
                        message_text += (
                            f"Auditorium number: {auditory_name}\n"
                            f"Starting at {lecture_start_datetime.strftime('%H:%M')}\n"
                        )
            message_text += "\nSee you tomorrow!\n"
            email_status = send_mail(
                f"Tomorrow's lecture schedule ({tomorrow_day.strftime('%d.%m.%Y')})",
                message_text,
                settings.EMAIL_HOST_USER,
                group_info.get("student_emails"),
                fail_silently=True,
            )
            print(f"E-mails for the group {group_name} have been sent successfully!") if email_status == 1 else print(
                f"Error when sending e-mails to a group {group_name}..."
            )
    print(f"No lectures are scheduled for tomorrow ({tomorrow_day.strftime('%d.%m.%Y')})")
