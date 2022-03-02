from django import forms
from stock.models import Product
from .models import Purchases

products = Product.objects.all()

class PurchaseForm(forms.ModelForm):

    proveedor = forms.CharField(label='proveedor',widget=forms.TextInput(attrs={'placeholder':'Nombre Proveedor'}))
    cantidad = forms.IntegerField(label='cantidad',widget=forms.TextInput(attrs={'placeholder':'0000'}))
    descripcion = forms.CharField(label='descripcion',widget=forms.TextInput(attrs={'placeholder':'Descripción simple'}))
    precio_unidad = forms.IntegerField(label='precio_unidad',widget=forms.TextInput(attrs={'placeholder':'0000'}))

    class Meta:
        model = Purchases
        exclude = ('slug',)

class DateInput(forms.DateInput):
    input_type = 'date'

class SearchForm(forms.Form):
    query = forms.CharField()

class DateForm(forms.Form):
    date_query_start = forms.DateField(widget=DateInput)
    date_query_end = forms.DateField(widget=DateInput)

class DestroyObjectForm(forms.Form):
    field = forms.BooleanField(required=False)

    widgets = {
            'field': forms.HiddenInput
        }
