# Generated by Django 3.2.11 on 2022-01-19 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='precio_unidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='purchases',
            name='slug',
            field=models.SlugField(max_length=250, unique_for_date='fecha'),
        ),
    ]