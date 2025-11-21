from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class AdminRequest(models.Model):
    """
    게시글 생성 또는 수정을 관리자에게 요청하는 모델.
    """

    REQUEST_TYPE_CHOICES = [
        ("CREATE", "게시글 생성 요청"),
        ("UPDATE", "게시글 수정 요청"),
    ]

    STATUS_CHOICES = [
        ("processing", "요청 처리중"),
        ("done", "요청 처리됨"),
        ("rejected", "거절됨"),
    ]

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="admin_requests",
        verbose_name="요청자",
    )

    # 'posts.Post' 문자열 참조를 사용하여 순환 import(모듈 초기화 문제)를 피합니다.
    target_post = models.ForeignKey(
        "posts.Post",
        on_delete=models.SET_NULL,
        related_name="related_requests",
        null=True,
        blank=True,
        verbose_name="대상 게시글",
    )

    request_type = models.CharField(
        max_length=10, choices=REQUEST_TYPE_CHOICES, verbose_name="요청 유형"
    )

    title = models.CharField(max_length=255, verbose_name="요청 제목")

    content = models.TextField(verbose_name="요청 상세 내용")

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default="processing",
        verbose_name="처리 상태",
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reviewed_requests",
        null=True,
        blank=True,
        verbose_name="검토자",
    )

    review_comment = models.TextField(blank=True, verbose_name="검토 코멘트")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="요청 생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="최근 갱신일")

    class Meta:
        db_table = "admin_requests"
        verbose_name = "관리자 요청"
        verbose_name_plural = "관리자 요청 목록"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_request_type_display()} - {self.title} ({self.get_status_display()})"

    def clean(self):
        """모델 저장 전 유효성 검사 (생성 vs 수정 요청에 따른 대상 게시글 유무 검사)"""
        if self.request_type == "UPDATE" and not self.target_post:
            raise ValidationError(
                {"target_post": _("수정 요청의 경우 대상 게시글을 선택해야 합니다.")}
            )

        if self.request_type == "CREATE" and self.target_post:
            raise ValidationError(
                {"target_post": _("생성 요청의 경우 대상 게시글을 지정할 수 없습니다.")}
            )
