import json

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# =================================================================
# 🔑 공통 Choices 정의 (Post 모델용)
# =================================================================

# 1. 월 선택지 (1월 ~ 12월)
# 이 상수는 Admin 폼에서 사용됩니다.
MONTH_CHOICES = [(f"{i}월", f"{i}월") for i in range(1, 13)]
MONTH_VALUES = [val[0] for val in MONTH_CHOICES]

# 2. 모집 분야 Choices (User 모델의 INTEREST_CHOICES 재사용 또는 확장)
RECRUITMENT_CHOICES = [
    ("PM", "프로젝트/제품 관리 (PM)"),
    ("DESIGN", "디자인"),
    ("FRONTEND", "프론트엔드"),
    ("BACKEND", "백엔드"),
    ("AI_ML", "AI/머신러닝"),
]
RECRUITMENT_VALUES = [val[0] for val in RECRUITMENT_CHOICES]


# 3. 개발 레벨 Choices (User 모델의 LEVEL_CHOICES 재사용)
LEVEL_CHOICES = [
    ("NOVICE", "초심자"),
    ("INTERMEDIATE", "중급자"),
    ("ADVANCED", "고급자"),
]
LEVEL_VALUES = [val[0] for val in LEVEL_CHOICES]


# 4. 신청 자격 Choices (User 모델의 AFFILIATION_CHOICES 재사용 또는 확장)
ELIGIBILITY_CHOICES = [
    ("STUDENT", "대학생"),
    ("GRADUATE", "졸업생"),
    ("WORKER", "직장인"),
]
ELIGIBILITY_VALUES = [val[0] for val in ELIGIBILITY_CHOICES]


# =================================================================
# Post 모델
# =================================================================


class Post(models.Model):
    """
    동아리/팀 모집 공고 게시글 모델.
    다중 선택 필드는 콤마로 구분된 문자열(CharField)로 저장됩니다.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recruitment_posts",
        verbose_name="작성자",
    )

    club_name = models.CharField(max_length=100, verbose_name="동아리/팀 이름")

    # 🔑 1. 동아리 홈페이지 필드 추가
    homepage_link = models.URLField(
        max_length=200, blank=True, null=True, verbose_name="동아리/팀 홈페이지"
    )

    # 🔑 2. 월 선택지 기반으로 CharField로 변경 (콤마로 구분된 문자열 저장)
    # 룩업 시 '11월'과 같은 값이 콤마 사이에 있는지 확인하는 방식으로 사용됩니다.
    application_months = models.CharField(
        max_length=50,  # 최대 12개 월 (5자 * 12 + 콤마)
        verbose_name="지원 기간 (월)",
        help_text="미리 정의된 월 목록에서 선택하세요. (콤마로 구분된 코드)",
        blank=True,
    )

    activity_months = models.CharField(
        max_length=50,
        verbose_name="주요 활동 기간 (월)",
        help_text="미리 정의된 월 목록에서 선택하세요. (콤마로 구분된 코드)",
        blank=True,
    )

    description = models.TextField(verbose_name="동아리 상세 설명")

    # 🔑 3. 신청 자격 필드 변경 (CharField로 변경)
    eligibility = models.CharField(
        max_length=100,
        verbose_name="신청 자격 (소속)",
        help_text="미리 정의된 소속 코드 목록에서 다중 선택하세요. (콤마로 구분된 코드)",
        blank=True,
    )

    # 🔑 4. 모집 분야 필드 변경 (CharField로 변경)
    recruitment_fields = models.CharField(
        max_length=100,
        verbose_name="모집 분야",
        help_text="미리 정의된 분야 코드 목록에서 다중 선택하세요. (콤마로 구분된 코드)",
    )

    # 🔑 5. 개발 수준 필드 추가 (CharField로 변경)
    required_dev_levels = models.CharField(
        max_length=100,
        verbose_name="요구 개발 레벨",
        help_text="미리 정의된 레벨 코드 목록에서 다중 선택하세요. (콤마로 구분된 코드)",
        blank=True,
    )

    # 🔑 6. review_links 필드는 아래 PostReviewLink 모델로 대체됨

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

    # 콤마 구분 문자열 Display 메서드
    def _get_display_from_charfield(self, field_name, choices):
        """CharField에 저장된 콤마 구분 코드를 사람이 읽을 수 있는 문자열로 변환"""
        codes = getattr(self, field_name)
        if not codes:
            return "정보 미정"

        # 딕셔너리로 choices를 매핑하여 빠르게 변환
        choice_map = dict(choices)

        # 콤마로 구분된 코드를 리스트로 분리하고 trim 후 display 값으로 변환
        code_list = [c.strip() for c in codes.split(",")]
        display_values = [choice_map.get(v, v) for v in code_list]
        return ", ".join(display_values)

    def get_application_months_display(self):
        return self._get_display_from_charfield("application_months", MONTH_CHOICES)

    def get_activity_months_display(self):
        return self._get_display_from_charfield("activity_months", MONTH_CHOICES)

    def get_recruitment_fields_display(self):
        return self._get_display_from_charfield(
            "recruitment_fields", RECRUITMENT_CHOICES
        )

    def get_eligibility_display(self):
        return self._get_display_from_charfield("eligibility", ELIGIBILITY_CHOICES)

    def get_required_dev_levels_display(self):
        return self._get_display_from_charfield("required_dev_levels", LEVEL_CHOICES)

    # 🔑 review_links를 대체하는 메서드
    def get_review_links_display(self):
        """연결된 PostReviewLink 모델을 기반으로 후기 링크 개수를 반환"""
        count = self.reviews.count()
        if count == 0:
            return "후기 없음"

        # 첫 번째 링크를 가져와서 표시 (가정)
        first_review = self.reviews.first()
        if count == 1:
            return first_review.review_title if first_review else "후기 1개"

        return (
            f"{first_review.review_title if first_review else '후기'} 외 {count - 1}개"
        )


# =================================================================
# 🔑 새 모델: 활동 후기 링크 모델 (PostReviewLink)
# =================================================================


class PostReviewLink(models.Model):
    """Post와 1:N 관계를 맺는 활동 후기 링크 모델."""

    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="reviews",  # Post.reviews.all()로 접근 가능
        verbose_name="모집 공고",
    )
    review_title = models.CharField(max_length=100, verbose_name="후기 제목")
    review_url = models.URLField(max_length=200, verbose_name="후기 링크")

    class Meta:
        verbose_name = "활동 후기 링크"
        verbose_name_plural = "활동 후기 링크 목록"

    def __str__(self):
        return f"[{self.post.club_name}] {self.review_title}"
