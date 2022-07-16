from urllib.parse import urlencode
from django import template

register = template.Library()

@register.simple_tag
def format_card_number(BIN, number):
    string = str(BIN + number)
    return ' '.join(string[i:i + 4] for i in range(0, len(string), 4))