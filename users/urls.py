from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
]
