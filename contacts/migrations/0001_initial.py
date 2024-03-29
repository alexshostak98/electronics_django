# Generated by Django 4.2.2 on 2023-07-01 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0002_alter_company_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=60)),
                ('city', models.CharField(max_length=150)),
                ('street', models.CharField(max_length=150)),
                ('house_number', models.CharField(max_length=50)),
            ],
            options={
                'unique_together': {('country', 'city', 'street', 'house_number')},
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, default='main email', max_length=150)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'unique_together': {('email', 'description')},
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contacts.address')),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('email', models.ManyToManyField(to='contacts.email')),
            ],
        ),
    ]
