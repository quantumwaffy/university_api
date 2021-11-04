from rest_framework import generics

from api import models, serializers


class AuditoriumParamsMixin:
    serializer_class = serializers.AuditoriumSerializer
    queryset = models.Auditorium.objects.all()


class GroupParamsMixin:
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()


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
