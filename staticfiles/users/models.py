from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email address')

    document_type = models.CharField(
        blank=True, 
        max_length=10,
        null=True, 
        verbose_name='tipo de documento',
    )

    document_number = models.CharField(
        blank=True, 
        max_length=26,
        null=True,
        verbose_name='documento',
        validators=[
            RegexValidator(r'^[a-zA-Z0-9]+$', message='Ingresa números o letras'),
        ],
    )

    mobile_number = models.CharField(
        blank=True, 
        max_length=20, 
        null=True,
        verbose_name='teléfono celular'
    )   

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return '{} <{}>'.format(self.full_name, self.username)

    class Meta:       
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
