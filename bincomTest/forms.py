from django import forms
from .models import Lga

class LGASearchForm(forms.Form):
    lga = forms.ModelChoiceField(
        queryset=Lga.objects.all(), 
        label="Select LGA"
    )