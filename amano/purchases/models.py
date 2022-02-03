from pyexpat import model
from django.db import models
from amano.utils import unique_slug_generator


class Purchases(models.Model):

    proveedor = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField(default=0)
    producto = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    precio_unidad = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250,unique_for_date='fecha')

    def __str__(self):
        return str(self.proveedor) + ' ' + str(self.fecha)
    
    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, self.proveedor, self.slug)
        super(Purchases, self).save(*args,**kwargs)

    def calculate_total(self):

        return int(self.cantidad) * int(self.precio_unidad)
    
    class Meta:
        ordering = ('-fecha',)
