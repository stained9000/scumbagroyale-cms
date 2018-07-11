from django.template.defaultfilters import register

@register.filter(name='format_thousands')

def format_thousands(value):
    return "{:,}".format(value)
