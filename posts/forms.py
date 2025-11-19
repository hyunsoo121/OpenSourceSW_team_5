from django import forms
from django.forms import CheckboxSelectMultiple  # 체크박스 위젯 import

from .models import (
    ELIGIBILITY_CHOICES,
    LEVEL_CHOICES,
    MONTH_CHOICES,
    RECRUITMENT_CHOICES,
    Post,
)


class PostAdminForm(forms.ModelForm):
    """
    Post 모델의 JSONField들을 Admin에서 CheckboxSelectMultiple로 입력받기 위한 폼.
    JSONField는 Django 폼 시스템에서 기본 위젯을 제공하지 않으므로,
    MultipleChoiceField로 오버라이드하여 다중 선택 목록을 제공합니다.
    """

    # 1. 지원 기간 (application_months) - MONTH_CHOICES 사용
    application_months = forms.MultipleChoiceField(
        choices=MONTH_CHOICES,
        required=False,
        widget=CheckboxSelectMultiple,
        label="지원 기간 (월)",
        help_text=Post.application_months.field.help_text,
    )

    # 2. 주요 활동 기간 (activity_months) - MONTH_CHOICES 사용
    activity_months = forms.MultipleChoiceField(
        choices=MONTH_CHOICES,
        required=False,
        widget=CheckboxSelectMultiple,
        label="주요 활동 기간 (월)",
        help_text=Post.activity_months.field.help_text,
    )

    # 3. 신청 자격 (eligibility) - ELIGIBILITY_CHOICES 사용
    eligibility = forms.MultipleChoiceField(
        choices=ELIGIBILITY_CHOICES,
        required=False,
        widget=CheckboxSelectMultiple,
        label="신청 자격 (소속)",
        help_text=Post.eligibility.field.help_text,
    )

    # 4. 모집 분야 (recruitment_fields) - RECRUITMENT_CHOICES 사용
    recruitment_fields = forms.MultipleChoiceField(
        choices=RECRUITMENT_CHOICES,
        required=False,
        widget=CheckboxSelectMultiple,
        label="모집 분야",
        help_text=Post.recruitment_fields.field.help_text,
    )

    # 5. 요구 개발 레벨 (required_dev_levels) - LEVEL_CHOICES 사용
    required_dev_levels = forms.MultipleChoiceField(
        choices=LEVEL_CHOICES,
        required=False,
        widget=CheckboxSelectMultiple,
        label="요구 개발 레벨",
        help_text=Post.required_dev_levels.field.help_text,
    )

    class Meta:
        model = Post
        fields = "__all__"

    # 폼 인스턴스 초기화 시, JSON 데이터를 MultipleChoiceField가 인식할 수 있는 리스트 형태로 변환
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 모델 인스턴스가 존재할 때 (수정 모드) JSONField의 값을 폼 필드에 로드
        if self.instance.pk:
            for field_name in [
                "application_months",
                "activity_months",
                "eligibility",
                "recruitment_fields",
                "required_dev_levels",
            ]:
                data = getattr(self.instance, field_name)
                # JSONField에 저장된 리스트를 MultipleChoiceField의 initial 값으로 설정
                self.fields[field_name].initial = data if data is not None else []

    # 폼 유효성 검사 후, clean_data를 JSONField가 기대하는 리스트 형태로 유지 (일반적으로 ModelForm이 처리함)
    # 특별한 추가 로직은 필요 없습니다. MultipleChoiceField는 리스트를 반환합니다.
