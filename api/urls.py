from django.urls import path

from api import views

urlpatterns = [
    path("auditorium/list/", views.AuditoriumListView.as_view()),
    path("auditorium/detail/<int:auditorium_id>/", views.AuditoriumRetrieveUpdateDestroyView.as_view()),
    path("auditorium/detail/create/", views.AuditoriumCreateView.as_view()),
    path("group/list/", views.GroupListView.as_view()),
    path("group/detail/<int:group_id>/", views.GroupRetrieveUpdateDestroyView.as_view()),
    path("group/detail/create/", views.GroupCreateView.as_view()),
]
