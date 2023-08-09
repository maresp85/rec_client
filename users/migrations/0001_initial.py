# Generated by Django 4.1.7 on 2023-08-05 17:31

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='pais')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'país',
                'verbose_name_plural': 'paises',
            },
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='nombre')),
                ('mobile_phone', models.CharField(max_length=64, verbose_name='teléfono')),
            ],
            options={
                'verbose_name': 'empresa',
                'verbose_name_plural': 'empresas',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='ciudad')),
                ('is_active', models.BooleanField(default=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.country', verbose_name='país')),
            ],
            options={
                'verbose_name': 'ciudad',
                'verbose_name_plural': 'ciudades',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('client_id', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='cliente id')),
                ('first_name', models.CharField(max_length=128, verbose_name='nombre')),
                ('last_name', models.CharField(max_length=128, verbose_name='apellidos')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('document_type', models.CharField(blank=True, max_length=10, null=True, verbose_name='tipo de documento')),
                ('document_number', models.CharField(max_length=26, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9]+$', message='Ingresa números o letras')], verbose_name='documento')),
                ('address', models.CharField(max_length=120, verbose_name='dirección domicilio')),
                ('address_payment', models.CharField(max_length=120, verbose_name='dirección de cobro')),
                ('mobile_number', models.CharField(max_length=20, verbose_name='teléfono celular')),
                ('created_from_server', models.BooleanField(default=False, verbose_name='creado desde el server')),
                ('referred_code', models.CharField(blank=True, max_length=24, null=True, verbose_name='código referido')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='fecha creación')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.city', verbose_name='ciudad')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.enterprise', verbose_name='empresa')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'usuarios',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]