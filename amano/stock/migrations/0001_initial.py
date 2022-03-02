# Generated by Django 3.2.11 on 2022-03-02 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_agregado', models.DateTimeField(auto_now_add=True)),
                ('nombre', models.CharField(max_length=100)),
                ('precio_venta', models.FloatField()),
                ('categoria', models.CharField(default='Vajilla', max_length=100)),
                ('slug', models.SlugField(default='product', max_length=250, unique_for_date='fecha_agregado')),
            ],
        ),
    ]
