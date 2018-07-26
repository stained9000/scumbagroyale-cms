from django.template.defaultfilters import register

@register.filter(name='games_percent')

def games_percent(value, total_games):
    if type(total_games) == type({}):
        return value/total_games['card_count']
    else:
        return value/total_games
