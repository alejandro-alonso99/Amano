from django.db import models
from stock.models import Product
from amano.utils import unique_slug_generator
from django.urls import reverse

class Purchases(models.Model):

    proveedor = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField(default=0)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=50)
    precio_unidad = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250,unique_for_date='fecha')
    
    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, self.proveedor, self.slug)
        super(Purchases, self).save(*args,**kwargs)

    def calculate_total(self):

        return int(self.cantidad) * int(self.precio_unidad)
    
    def get_absolute_url(self):
        return reverse ('purchases:purchase_detail',
                                        args=[self.fecha.day,
                                                self.fecha.month,
                                                self.fecha.year,
                                                self.slug])
    def __str__(self):

        return str(self.proveedor) + ' ' + self.fecha.strftime("%d-%m-%Y")

    class Meta:
        ordering = ('-fecha',)


    def get_category(self):

        product_category = self.producto.categoria

        return product_category

