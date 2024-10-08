# Generated by Django 4.1.10 on 2024-08-20 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='office_name',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='nombre oficina'),
        ),
        migrations.AddField(
            model_name='user',
            name='office_phone_number',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='teléfonos oficina'),
        ),
    ]
