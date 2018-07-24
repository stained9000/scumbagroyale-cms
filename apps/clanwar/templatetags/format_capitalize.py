from django.template.defaultfilters import register

@register.filter(name='format_capitalize')

def format_capitalize(value):
    return value.capitalize()
