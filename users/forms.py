from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User  # 커스텀 User 모델 임포트


class CustomUserCreationForm(UserCreationForm):
    """
    이전에 정의한 커스텀 User 모델을 사용하는 회원가입 폼입니다.
    AbstractUserCreationForm을 상속받아 비밀번호 확인 및 기본 유효성 검사를 자동으로 처리합니다.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        # 기본 필드 (username, password) 외에 추가된 필수 필드들을 포함합니다.
        fields = (
            "username",
            "nickname",
            "email",
            "interest_field",
            "affiliation",
            "dev_level",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 필수 필드로 지정했음에도 UserCreationForm의 기본 설정 때문에
        # required=False가 될 수 있어 명시적으로 True로 설정합니다.
        self.fields["email"].required = True
        self.fields["nickname"].required = True
