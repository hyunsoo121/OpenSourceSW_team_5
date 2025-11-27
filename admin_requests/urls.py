from django.urls import path

from . import views

app_name = "admin_request"

urlpatterns = [
    path("", views.request_list, name="request_list"),
    path("detail/<int:request_id>/", views.request_detail, name="request_detail"),
    path("create/", views.request_create, name="request_create"),
    path("edit/<int:request_id>/", views.request_edit, name="request_edit"),
    path("delete/<int:request_id>/", views.request_delete, name="request_delete"),
]
