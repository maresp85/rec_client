import smtplib
import ssl

from django.core.mail.backends.smtp import EmailBackend


class PatchedEmailBackend(EmailBackend):
    """
    Custom email backend para Titan/Hostinger.
    Resuelve problemas de compatibilidad SSL con smtp.titan.email.
    """

    def open(self):
        if self.connection:
            return False

        try:
            context = ssl.create_default_context()
            context.set_ciphers('DEFAULT')

            if self.use_ssl:
                self.connection = smtplib.SMTP_SSL(
                    self.host,
                    self.port,
                    timeout=self.timeout,
                    context=context,
                )
            else:
                self.connection = smtplib.SMTP(
                    self.host,
                    self.port,
                    timeout=self.timeout,
                )
                if self.use_tls:
                    self.connection.starttls(context=context)

            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True
        except Exception:
            if self.fail_silently:
                return False
            raise
