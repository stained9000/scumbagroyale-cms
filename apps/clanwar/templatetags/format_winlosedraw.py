from django.template.defaultfilters import register

@register.filter(name='format_winlosedraw')

def format_winlosedraw(value):
    if value == 0:
        return {'result': 'Draw', 'color1':"#ddd", 'color2': "#a9a8a8"}
    elif value < 0:
        return {'result': 'Lost', 'color1':"#d01f30", 'color2': "#902622"}
    else:
        return {'result': 'Won', 'color1':"#001ff9", 'color2': "#1c3b8c"}
