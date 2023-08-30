from datetime import datetime
from django import template

register = template.Library()


@register.simple_tag
def check_due_date(due_date) -> bool:
    if due_date:
        return datetime.today() > datetime.strptime(due_date, '%Y-%m-%d')
    
    return False