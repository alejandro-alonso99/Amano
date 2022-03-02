from django import forms
from .models import Recap

class RecapForm(forms.ModelForm):

    dias_trabajados = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'0000'}))

    class Meta:
        model = Recap
        fields = ['month', 'dias_trabajados']
        widgets = {
            'month' : forms.HiddenInput,
        }