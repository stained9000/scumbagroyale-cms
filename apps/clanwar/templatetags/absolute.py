from django.template.defaultfilters import register

@register.filter(name='absolute')

def absolute(value):
    return abs(value)
