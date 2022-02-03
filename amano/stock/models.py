from django.db import models

class Product(models.Model):
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()