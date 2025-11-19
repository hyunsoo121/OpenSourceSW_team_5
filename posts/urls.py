from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.posts_list, name="posts_list"),
    path("detail/<int:post_id>/", views.posts_detail, name="posts_detail"),
]
