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
            "phone",
            "address",
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

        # 전화번호 필드 설정
        if "phone" in self.fields:
            self.fields["phone"].widget.attrs.update(
                {
                    "placeholder": "010-0000-0000",
                    "pattern": "[0-9]{3}-[0-9]{3,4}-[0-9]{4}",
                }
            )

        # 주소 필드 설정
        if "address" in self.fields:
            self.fields["address"].widget.attrs.update(
                {"placeholder": "주소를 입력해주세요"}
            )


class EditProfileForm(forms.ModelForm):
    """사용자 정보 수정 폼: username, password는 제외하고 수정 가능하도록 함"""

    class Meta:
        model = User
        fields = (
            "nickname",
            "email",
            "phone",
            "address",
            "interest_field",
            "affiliation",
            "dev_level",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # 이메일 중복 체크: 본인 제외
        if email:
            qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("이미 사용 중인 이메일입니다.")
        return email
