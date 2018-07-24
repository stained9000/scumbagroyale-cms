from django.template.defaultfilters import register

@register.filter(name='games_percent')

def games_percent(value, total_games):
    return value/total_games
