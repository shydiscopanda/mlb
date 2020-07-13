from django import forms
from django.forms import IntegerField

from .models import Result


class InputForm(forms.ModelForm):
    incoming_val = IntegerField(
        max_value=100000,
        min_value=-100000,
        label='Enter Value',
    )

    class Meta:
        model = Result
        fields = ['incoming_val']
