# Generated by Django 4.2.3 on 2023-07-04 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0004_company_positive_debt'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='employees',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='company', to=settings.AUTH_USER_MODEL),
        ),
    ]
