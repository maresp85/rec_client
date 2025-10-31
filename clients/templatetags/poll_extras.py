from datetime import datetime, date
from django import template

register = template.Library()

@register.filter
def format_due_date(value):
    """
    Formatea value a 'DD/MM/YYYY'. Soporta:
    - datetime object
    - date object
    - ISO strings: 'YYYY-MM-DD', 'YYYY-MM-DDTHH:MM:SSZ', 'YYYY-MM-DDTHH:MM:SS-06:00'
    - Si no puede formatear devuelve el original como string.
    """
    if not value:
        return ''
    # Si es datetime o date
    if isinstance(value, datetime):
        return value.date().strftime("%d/%m/%Y")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")

    s = str(value)
    # Tomar la parte YYYY-MM-DD si viene ISO
    clean = s.split("T")[0]
    try:
        dt = datetime.strptime(clean, "%Y-%m-%d").date()
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return s  # fallback: devolver como vino


@register.simple_tag
def check_due_date(due_date):
    """
    Devuelve True si hoy > due_date (solo por fecha). Acepta datetime/date/string ISO.
    """
    if not due_date:
        return False

    # Convertir a date
    if isinstance(due_date, datetime):
        due = due_date.date()
    elif isinstance(due_date, date):
        due = due_date
    else:
        clean = str(due_date).split("T")[0]
        try:
            due = datetime.strptime(clean, "%Y-%m-%d").date()
        except Exception:
            return False

    return date.today() > due
