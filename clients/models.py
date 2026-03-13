from django.conf import settings
from django.db import models


class ApprovalCodeEmailLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
    )
    credit_id = models.IntegerField(verbose_name='ID del Crédito')
    approval_code = models.CharField(max_length=50, verbose_name='Código de Aprobación')
    credit_value = models.CharField(max_length=50, verbose_name='Valor del Crédito')
    email_to = models.EmailField(verbose_name='Correo Destino')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Envío')
    success = models.BooleanField(default=True, verbose_name='Enviado Exitosamente')

    class Meta:
        verbose_name = 'Log de Correo - Código de Aprobación'
        verbose_name_plural = 'Logs de Correos - Códigos de Aprobación'
        ordering = ['-sent_at']

    def __str__(self):
        return f'{self.email_to} - Crédito #{self.credit_id} - {self.approval_code} ({self.sent_at:%Y-%m-%d %H:%M})'
