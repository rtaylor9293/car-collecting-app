from django import forms
from .models import CarDate

class CarDateForm(forms.ModelForm):
    class Meta:
        model = CarDate
        fields = ['date', 'present']
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
        }
