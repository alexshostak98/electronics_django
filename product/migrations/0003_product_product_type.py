# Generated by Django 4.2.3 on 2023-07-06 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_unique_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.CharField(default='electronics', max_length=150),
        ),
    ]
