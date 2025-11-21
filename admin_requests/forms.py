from django import forms

from .models import AdminRequest


class AdminRequestForm(forms.ModelForm):
    class Meta:
        model = AdminRequest
        fields = ["request_type", "title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "input", "placeholder": "요청 제목"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "textarea",
                    "rows": 8,
                    "placeholder": "요청 내용을 입력하세요.",
                }
            ),
        }


class AdminReviewForm(forms.ModelForm):
    class Meta:
        model = AdminRequest
        fields = ["status", "review_comment"]
        widgets = {
            "review_comment": forms.Textarea(attrs={"class": "textarea", "rows": 4}),
        }
