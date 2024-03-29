# Generated by Django 4.2.2 on 2023-07-01 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0003_remove_company_create_date_company_creation_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('model', models.CharField(max_length=100)),
                ('market_launch_date', models.DateField()),
                ('company', models.ManyToManyField(related_name='products', to='company.company')),
            ],
        ),
    ]
