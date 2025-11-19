# posts/admin.py

from django.contrib import admin
from django.db import models as db_models
from django.forms import CheckboxSelectMultiple

from .forms import PostAdminForm  # 새로 만든 폼 import
from .models import (  # Post 모델의 Choices 및 필드 import
    ELIGIBILITY_CHOICES,
    LEVEL_CHOICES,
    MONTH_CHOICES,
    RECRUITMENT_CHOICES,
    Post,
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 🔑 폼 클래스 연결
    form = PostAdminForm

    # list_display를 업데이트합니다 (Post 모델에 새 필드 display 메서드가 있다면).
    list_display = (
        "club_name",
        "author",
        "is_published",
        "created_at",
        "get_application_months_display",
        "get_recruitment_fields_display",  # 예시
    )
    # list_filter도 JSONField의 choices를 기반으로 필터링하도록 수정 필요 (고급 설정)
    list_filter = ("is_published",)
    search_fields = ("club_name", "description")

    # 폼에서 숨김 유지
    exclude = ("author",)

    # 🔑 JSONField에 대한 기본 위젯을 오버라이드 (forms.py에 정의했으므로 선택 사항)
    # formfield_overrides = {
    #     db_models.JSONField: {'widget': CheckboxSelectMultiple},
    # }

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            obj = Post(author=request.user)
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    # 🔑 Model의 display 메서드를 사용하여 list_display 구현
    def get_application_months_display(self, obj):
        # Post 모델에 정의된 get_application_months_display() 호출
        return obj.get_application_months_display()

    get_application_months_display.short_description = "지원 기간"

    # 모집 분야 display 메서드 예시
    def get_recruitment_fields_display(self, obj):
        return obj.get_recruitment_fields_display()

    get_recruitment_fields_display.short_description = "모집 분야"
