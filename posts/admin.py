from django.contrib import admin

from .forms import PostAdminForm
from .models import Post, PostReviewLink


class PostReviewLinkInline(admin.TabularInline):
    model = PostReviewLink
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    exclude = ("author",)
    inlines = [PostReviewLinkInline]

    list_display = (
        "__str__",
        "name",
        "type",
        "author",
        "is_published",
        "created_at",
        "get_application_months_display",
        "get_recruitment_fields_display",
        "get_required_dev_levels_display",
        "get_review_links_display",
    )

    # 🔥🔥 체크박스 저장 핵심 로직 — admin에서만 수행 🔥🔥
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user

        super().save_model(request, obj, form, change)
