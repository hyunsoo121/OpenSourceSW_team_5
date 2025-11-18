from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "club_name", "author", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("club_name", "description", "recruitment_fields")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
