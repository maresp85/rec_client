# Generated by Django 3.2.9 on 2023-08-29 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_client_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=48, null=True, verbose_name='teléfono celular'),
        ),
    ]
