from django import forms
from django.utils import timezone


class AvailabilityForm(forms.Form):
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    check_out = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    guest_count = forms.IntegerField(
        min_value=1
    )

    def clean(self):
        cleaned_data = super().clean()

        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in and check_out:

            if check_in < timezone.now().date():
                raise forms.ValidationError(
                    "Check-in date cannot be in the past."
                )

            if check_out <= check_in:
                raise forms.ValidationError(
                    "Check-out date must be after check-in date."
                )

        return cleaned_data