from django.template.defaultfilters import register

@register.filter(name='format_thousands')

def format_thousands(value):
    if value == None:
        return None
    else:
        try:
            return "{:,}".format(value)
        except:
            return None
