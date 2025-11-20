from django.contrib import admin

from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "nickname",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "interest_field",
        "affiliation",
        "dev_level",
    )
    search_fields = ("username", "nickname", "email")
    readonly_fields = ("date_joined",)
    ordering = ("-date_joined",)
