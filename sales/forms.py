from django import forms
from .models import Sale
from stock.models import Product

products = Product.objects.all()
class SaleForm(forms.ModelForm):

    cliente = forms.CharField(label='cliente',widget=forms.TextInput(attrs={'placeholder':'Nombre cliente'}))
    cantidad = forms.IntegerField(label='cantidad',widget=forms.TextInput(attrs={'placeholder':'000000'}))
    localidad = forms.CharField(label='localidad',widget=forms.TextInput(attrs={'placeholder':'ej. Río Cuarto'}))
    descripcion = forms.CharField(label='descripcion',widget=forms.TextInput(attrs={'placeholder':'ej. Platos pintados'}))
    sena = forms.IntegerField(label='cantidad',widget=forms.TextInput(attrs={'placeholder':'10000'}))

    class Meta:
        model = Sale
        exclude = ('slug',)