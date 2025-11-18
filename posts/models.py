import json

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_month_list(value):
    """
    ['2월', '3월'] 형태의 문자열 목록인지 검증합니다.
    """
    if not isinstance(value, list):
        raise ValidationError(
            _('이 필드는 월(month) 문자열 목록이어야 합니다. (예: ["2월", "3월"])')
        )

    valid_months = [f"{i}월" for i in range(1, 13)]
    for item in value:
        if not isinstance(item, str) or item not in valid_months:
            raise ValidationError(
                _("%(item)s 는 유효한 월 형식이 아닙니다. 유효한 형식: 1월 ~ 12월"),
                params={"item": item},
            )


class Post(models.Model):
    """
    동아리/팀 모집 공고 게시글 모델.
    지원 기간과 활동 기간은 월 목록(JSONField)으로 저장됩니다.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recruitment_posts",
        verbose_name="작성자",
    )

    club_name = models.CharField(max_length=100, verbose_name="동아리/팀 이름")

    application_months = models.JSONField(
        verbose_name="지원 기간 (월)",
        help_text='배열 형태로 지원이 가능한 월을 입력하세요. 예: ["2월", "3월"]',
        validators=[validate_month_list],
    )

    activity_months = models.JSONField(
        verbose_name="주요 활동 기간 (월)",
        help_text='배열 형태로 활동이 이루어지는 월을 입력하세요. 예: ["2월", "3월", "4월"]',
        validators=[validate_month_list],
    )

    description = models.TextField(verbose_name="동아리 상세 설명")

    eligibility = models.TextField(
        blank=True,
        verbose_name="신청 자격",
        help_text="예: 특정 학과, 특정 개발 레벨 이상 등",
    )

    recruitment_fields = models.TextField(
        verbose_name="모집 분야", help_text="예: 백엔드, 프론트엔드, 디자이너"
    )

    review_link = models.URLField(
        max_length=200, blank=True, null=True, verbose_name="이전 활동 후기 링크"
    )

    is_published = models.BooleanField(default=False, verbose_name="게시글 공개 여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="최근 수정일")

    class Meta:
        db_table = "posts"
        verbose_name = "모집 공고"
        verbose_name_plural = "모집 공고 목록"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.club_name}] 모집 공고"

    def get_application_months_display(self):
        """지원 기간을 보기 좋게 문자열로 반환"""
        if self.application_months:
            return ", ".join(self.application_months)
        return "기간 미정"

    def get_activity_months_display(self):
        """활동 기간을 보기 좋게 문자열로 반환"""
        if self.activity_months:
            return ", ".join(self.activity_months)
        return "기간 미정"
