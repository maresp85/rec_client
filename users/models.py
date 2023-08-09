from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    client_id = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='cliente id')

    first_name = models.CharField(max_length=128, verbose_name='nombre')

    last_name = models.CharField(max_length=128, verbose_name='apellidos')

    email = models.EmailField('email address')

    document_type = models.CharField(
        blank=True, 
        max_length=10,
        null=True, 
        verbose_name='tipo de documento',
    )

    document_number = models.CharField(
        max_length=26,
        verbose_name='documento',
        validators=[
            RegexValidator(r'^[a-zA-Z0-9]+$', message='Ingresa números o letras'),
        ],
    )

    address = models.CharField(max_length=120, verbose_name='dirección domicilio')

    address_payment = models.CharField(max_length=120, verbose_name='dirección de cobro')

    mobile_number = models.CharField(
        max_length=20, 
        verbose_name='teléfono celular'
    )

    company = models.ForeignKey(
        'users.Enterprise',
        blank=True, 
        null=True, 
        on_delete=models.PROTECT,
        verbose_name='empresa',
    )

    city = models.ForeignKey(
        'users.city',
        blank=True, 
        null=True, 
        on_delete=models.PROTECT,
        verbose_name='ciudad',
    )

    created_from_server = models.BooleanField(default=False, verbose_name='creado desde el server')

    referred_code = models.CharField(
        blank=True, 
        max_length=24, 
        null=True, 
        verbose_name='código referido'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='fecha creación')

    REQUIRED_FIELDS = [
        'first_name', 
        'last_name',
        'document_number', 
        'mobile_number', 
        'city_id'
    ]

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return '{} <{}>'.format(self.full_name, self.username)

    class Meta:       
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'


class Enterprise(models.Model):
    id: int = models.AutoField(primary_key=True)

    name = models.CharField(max_length=64, verbose_name='nombre')

    mobile_phone = models.CharField(max_length=64, verbose_name='teléfono')

    def __str__(self):
        return self.name

    class Meta:       
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'


class Country(models.Model):
    name = models.CharField(max_length=64, verbose_name='pais')

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:       
        verbose_name = 'país'
        verbose_name_plural = 'paises'


class City(models.Model):
    name = models.CharField(max_length=64, verbose_name='ciudad')

    country = models.ForeignKey(
        'users.country',
        on_delete=models.PROTECT,
        verbose_name='país',
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:       
        verbose_name = 'ciudad'
        verbose_name_plural = 'ciudades'