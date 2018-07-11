from django.template.defaultfilters import register

@register.filter(name='format_percent')

def format_percent(value):
    return "{0:.2f}".format(value * 100)
