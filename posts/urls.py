from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.posts_list, name="posts_list"),
    path("type/<str:type_code>/", views.posts_type_list, name="posts_type_list"),
    path("detail/<int:post_id>/", views.posts_detail, name="posts_detail"),
    path("ajax_list/", views.posts_ajax_list, name="posts_ajax_list"),
]
