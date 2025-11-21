from django import forms
from django.forms import CheckboxSelectMultiple

from .models import (
    ELIGIBILITY_CHOICES,
    LEVEL_CHOICES,
    MONTH_CHOICES,
    RECRUITMENT_CHOICES,
    Post,
)


class PostAdminForm(forms.ModelForm):

    application_months = forms.MultipleChoiceField(
        choices=MONTH_CHOICES,
        widget=CheckboxSelectMultiple,
        required=False,
        label="지원 기간 (월)",
    )
    activity_months = forms.MultipleChoiceField(
        choices=MONTH_CHOICES,
        widget=CheckboxSelectMultiple,
        required=False,
        label="주요 활동 기간 (월)",
    )
    eligibility = forms.MultipleChoiceField(
        choices=ELIGIBILITY_CHOICES,
        widget=CheckboxSelectMultiple,
        required=False,
        label="신청 자격",
    )
    recruitment_fields = forms.MultipleChoiceField(
        choices=RECRUITMENT_CHOICES,
        widget=CheckboxSelectMultiple,
        required=False,
        label="모집 분야",
    )
    required_dev_levels = forms.MultipleChoiceField(
        choices=LEVEL_CHOICES,
        widget=CheckboxSelectMultiple,
        required=False,
        label="요구 개발 레벨",
    )

    class Meta:
        model = Post
        fields = "__all__"
        # help_texts expects a mapping of field names to strings
        help_texts = {f.name: "" for f in Post._meta.fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        target_fields = [
            "application_months",
            "activity_months",
            "eligibility",
            "recruitment_fields",
            "required_dev_levels",
        ]

        if self.instance and self.instance.pk:
            for field in target_fields:
                raw = getattr(self.instance, field, None)
                values = [v.strip() for v in raw.split(",")] if raw else []
                # set both field initial and form initial to ensure admin shows selections
                self.fields[field].initial = values
                self.initial[field] = values

    def clean_application_months(self):
        data = self.cleaned_data.get("application_months", [])
        return ",".join(data) if data else ""

    def clean_activity_months(self):
        data = self.cleaned_data.get("activity_months", [])
        return ",".join(data) if data else ""

    def clean_eligibility(self):
        data = self.cleaned_data.get("eligibility", [])
        return ",".join(data) if data else ""

    def clean_recruitment_fields(self):
        data = self.cleaned_data.get("recruitment_fields", [])
        return ",".join(data) if data else ""

    def clean_required_dev_levels(self):
        data = self.cleaned_data.get("required_dev_levels", [])
        return ",".join(data) if data else ""
