import datetime

from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

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
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuditoriumRetrieveUpdateDestroyView(AuditoriumParamsMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "auditorium_id"
    permission_classes = [IsAuthenticatedOrReadOnly]


class GroupListView(GroupParamsMixin, generics.ListAPIView):
    pass


class GroupCreateView(GroupParamsMixin, generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]


class GroupRetrieveUpdateDestroyView(GroupParamsMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "group_id"
    permission_classes = [IsAuthenticatedOrReadOnly]


class StudentListView(StudentParamsMixin, generics.ListAPIView):
    pass


class StudentCreateView(StudentParamsMixin, generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]


class StudentRetrieveUpdateDestroyView(StudentParamsMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "student_id"
    permission_classes = [IsAuthenticatedOrReadOnly]


class LectureListView(LectureParamsMixin, generics.ListAPIView):
    pass


class LectureCreateView(LectureParamsMixin, generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]


class LectureRetrieveUpdateDestroyView(LectureParamsMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "lecture_id"
    permission_classes = [IsAuthenticatedOrReadOnly]


class ScheduleListView(ScheduleParamsMixin, generics.ListAPIView):
    pass


class ScheduleCreateView(ScheduleParamsMixin, generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]


class ScheduleRetrieveUpdateDestroyView(ScheduleParamsMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "schedule_id"
    permission_classes = [IsAuthenticatedOrReadOnly]


class ScheduleListViewSet(ScheduleParamsMixin, viewsets.ModelViewSet):
    http_method_names = ["post"]

    def list(self, request, *args, **kwargs):
        request_schedule_date = request.data.get("schedule_date")
        request_schedule_group = request.data.get("schedule_group")
        if not request_schedule_date or not request_schedule_group:
            error_text = "schedule_date is required" if not request_schedule_date else "schedule_group is required"
            return Response(data={"error": error_text}, status=status.HTTP_400_BAD_REQUEST)
        group_object = get_object_or_404(models.Group, name=request_schedule_group)
        try:
            schedule_date = datetime.datetime.strptime(request_schedule_date, "%Y-%m-%d").date()
        except ValueError as e:
            raise Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            qs_response = self.queryset.filter(
                group=group_object,
                start_datetime__range=[
                    datetime.datetime.combine(schedule_date, datetime.time.min),
                    datetime.datetime.combine(schedule_date, datetime.time.max),
                ],
            )
        return Response(data=self.serializer_class(qs_response, many=True).data, status=status.HTTP_200_OK)
