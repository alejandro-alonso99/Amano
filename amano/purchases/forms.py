from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class SearchForm(forms.Form):
    query = forms.CharField()

class DateForm(forms.Form):
    date_query = forms.DateField(widget=DateInput)