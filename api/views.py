from rest_framework import generics

from api import models, serializers


class AuditoriumParamsMixin:
    serializer_class = serializers.AuditoriumSerializer
    queryset = models.Auditorium.objects.all()


class GroupParamsMixin:
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()


class StudentParamsMixin:
    serializer_class = serializers.StudentSerializer
    queryset = models.Student.objects.all()


class LectureParamsMixin:
    serializer_class = serializers.LectureSerializer
    queryset = models.Lecture.objects.all()


class ScheduleParamsMixin:
    serializer_class = serializers.ScheduleSerializer
    queryset = models.LectureGroup.objects.all()


class AuditoriumListView(AuditoriumParamsMixin, generics.ListAPIView):
    pass


class AuditoriumCreateView(AuditoriumParamsMixin, generics.CreateAPIView):
    pass


class AuditoriumRetrieveUpdateDestroyView(AuditoriumParamsMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "auditorium_id"


class GroupListView(GroupParamsMixin, generics.ListAPIView):
    pass


class GroupCreateView(GroupParamsMixin, generics.CreateAPIView):
    pass


class GroupRetrieveUpdateDestroyView(GroupParamsMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "group_id"


class StudentListView(StudentParamsMixin, generics.ListAPIView):
    pass


class StudentCreateView(StudentParamsMixin, generics.CreateAPIView):
    pass


class StudentRetrieveUpdateDestroyView(StudentParamsMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "student_id"


class LectureListView(LectureParamsMixin, generics.ListAPIView):
    pass


class LectureCreateView(LectureParamsMixin, generics.CreateAPIView):
    pass


class LectureRetrieveUpdateDestroyView(LectureParamsMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "lecture_id"


class ScheduleListView(ScheduleParamsMixin, generics.ListAPIView):
    pass


class ScheduleCreateView(ScheduleParamsMixin, generics.CreateAPIView):
    pass


class ScheduleRetrieveUpdateDestroyView(ScheduleParamsMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "schedule_id"
