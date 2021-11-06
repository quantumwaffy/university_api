from django.urls import path

from api import views

urlpatterns = [
    path("auditorium/list/", views.AuditoriumListView.as_view(), name="auditorium_list"),
    path(
        "auditorium/detail/<int:auditorium_id>/",
        views.AuditoriumRetrieveUpdateDestroyView.as_view(),
        name="auditorium_detail",
    ),
    path("auditorium/create/", views.AuditoriumCreateView.as_view(), name="auditorium_create"),
    path("group/list/", views.GroupListView.as_view(), name="group_list"),
    path("group/detail/<int:group_id>/", views.GroupRetrieveUpdateDestroyView.as_view(), name="group_detail"),
    path("group/create/", views.GroupCreateView.as_view(), name="group_create"),
    path("student/list/", views.StudentListView.as_view(), name="student_list"),
    path("student/detail/<int:student_id>/", views.StudentRetrieveUpdateDestroyView.as_view(), name="student_detail"),
    path("student/create/", views.StudentCreateView.as_view(), name="student_create"),
    path("lecture/list/", views.LectureListView.as_view(), name="lecture_list"),
    path("lecture/detail/<int:lecture_id>/", views.LectureRetrieveUpdateDestroyView.as_view(), name="lecture_detail"),
    path("lecture/create/", views.LectureCreateView.as_view(), name="lecture_create"),
    path("schedule/list/", views.ScheduleListView.as_view(), name="schedule_list"),
    path(
        "schedule/detail/<int:schedule_id>/", views.ScheduleRetrieveUpdateDestroyView.as_view(), name="schedule_detail"
    ),
    path("schedule/create/", views.ScheduleCreateView.as_view(), name="schedule_create"),
    path("get-date-schedule/", views.ScheduleListViewSet.as_view({"post": "list"}), name="get_date_schedule"),
]
