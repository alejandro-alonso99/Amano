from django import forms
from .models import ManualMove, Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('slug',)

class ChangePriceForm(forms.Form):
    amount = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder':'ej. 15 = 15%'}))

class ChangePriceWithAmountForm(forms.Form):
    ind_amount = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder':'ej. 900'}))

class ManualmoveForm(forms.ModelForm):

    class Meta:
        model = ManualMove
        fields = '__all__'
        
