from itertools import product
from django.db import models
from amano.utils import unique_slug_generator
from django.urls import reverse

class Product(models.Model):
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=100)
    precio_venta = models.FloatField()
    categoria = models.CharField(max_length=100, default='Vajilla')
    slug = models.SlugField(max_length=250,unique_for_date='fecha_agregado', default='product')

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, self.nombre, self.slug)
        super(Product, self).save(*args,**kwargs)


    def get_absolute_url(self):
        return reverse ('stock:product_detail',
                                        args=[self.fecha_agregado.day,
                                                self.fecha_agregado.month,
                                                self.fecha_agregado.year,
                                                self.slug])

    def __str__(self):
        return str(self.nombre) 

    
    def calculate_stock(self):
        
        pass

class ManualMove(models.Model):

    TYPE_CHOICES = (
        ('agregar','Agregar'),
        ('quitar','Quitar'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tipo = models.CharField(choices=TYPE_CHOICES, max_length=7)
    cantidad = models.PositiveIntegerField()