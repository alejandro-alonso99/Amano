from django.db import models
from amano.utils import unique_slug_generator
from django.urls import reverse
from stock.models import Product

class Sale(models.Model):

    TYPE_CHOICES = (
        ('pintado','Pintado'),
        ('en blanco','En blanco'),
    )

    fecha = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique_for_date='fecha')
    tipo = models.CharField(max_length=100, choices=TYPE_CHOICES, default='pintado')
    sena = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.cliente) + ' ' + self.fecha.strftime("%d-%m-%Y")
    
    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, self.cliente, self.slug)
        super(Sale, self).save(*args,**kwargs)

    
    def get_absolute_url(self):
        return reverse ('sales:sale_detail',
                                        args=[self.fecha.day,
                                                self.fecha.month,
                                                self.fecha.year,
                                                self.slug])

    class Meta:
        ordering = ('-fecha',)
    
    def calculate_total(self):

        sale_product_unit_price = self.product.precio_venta

        sale_total = float(sale_product_unit_price) * float(self.cantidad)
    
        return  sale_total
    
    def get_unit_price(self):

        sale_product_unit_price = self.product.precio_venta

        return sale_product_unit_price
    
    def get_category(self):

        sale_product_category = self.product.categoria

        return sale_product_category
