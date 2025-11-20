from django.contrib import admin

from .models import AdminRequest


def make_approved(modeladmin, request, queryset):
    queryset.update(status="approved")


def make_rejected(modeladmin, request, queryset):
    queryset.update(status="rejected")


@admin.register(AdminRequest)
class AdminRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "requester", "request_type", "status", "created_at")
    list_filter = ("status", "request_type")
    search_fields = ("title", "content", "requester__username")
    readonly_fields = ("created_at", "updated_at")
    actions = [make_approved, make_rejected]
