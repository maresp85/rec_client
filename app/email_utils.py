from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_approval_code_email(user_email: str, user_name: str, approval_code: str, credit_value: str):
    """Envía el código de aprobación del crédito por correo electrónico."""
    subject = 'TD Eléctrica - Código de Aprobación de Crédito'

    html_message = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"></head>
    <body style="margin:0; padding:0; background-color:#f0f2f5; font-family:'Inter',Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f2f5; padding:40px 0;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
              <!-- Header -->
              <tr>
                <td style="background:linear-gradient(135deg,#1e3a5f,#2d5a8e); padding:30px 40px; text-align:center;">
                  <h1 style="margin:0; color:#ffffff; font-size:24px; font-weight:700; letter-spacing:0.5px;">TD Eléctrica</h1>
                  <p style="margin:6px 0 0; color:rgba(255,255,255,0.8); font-size:13px;">Tarjeta Digital</p>
                </td>
              </tr>
              <!-- Body -->
              <tr>
                <td style="padding:36px 40px;">
                  <p style="margin:0 0 20px; color:#334155; font-size:15px; line-height:1.6;">
                    Hola <strong>{user_name}</strong>,
                  </p>
                  <p style="margin:0 0 24px; color:#334155; font-size:15px; line-height:1.6;">
                    Has solicitado un crédito por un valor de <strong>{credit_value}</strong>.
                    Para completar la aprobación, comparte el siguiente código con tu asesor:
                  </p>
                  <!-- Code Box -->
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td align="center" style="padding:20px 0;">
                        <div style="display:inline-block; background:#d1fae5; border:2px solid #6ee7b7; border-radius:10px; padding:18px 36px;">
                          <span style="font-size:28px; font-weight:700; color:#065f46; letter-spacing:3px;">{approval_code}</span>
                        </div>
                      </td>
                    </tr>
                  </table>
                  <p style="margin:24px 0 0; color:#64748b; font-size:13px; line-height:1.6; text-align:center;">
                    Este código es personal e intransferible. No lo compartas con personas ajenas al proceso de aprobación.
                  </p>
                </td>
              </tr>
              <!-- Footer -->
              <tr>
                <td style="background:#f8fafc; padding:20px 40px; border-top:1px solid #e2e8f0; text-align:center;">
                  <p style="margin:0; color:#94a3b8; font-size:12px;">
                    &copy; 2026 TD Eléctrica &middot; Tarjeta Digital<br>
                    Este correo fue enviado automáticamente, por favor no responda.
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    plain_message = (
        f'Hola {user_name},\n\n'
        f'Has solicitado un crédito por un valor de {credit_value}.\n'
        f'Tu código de aprobación es: {approval_code}\n\n'
        f'Comparte este código con tu asesor para completar la aprobación.\n\n'
        f'TD Eléctrica - Tarjeta Digital'
    )

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f'Error enviando correo de código de aprobación a {user_email}: {e}')
        return False
