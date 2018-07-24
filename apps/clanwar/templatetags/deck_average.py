from django.template.defaultfilters import register

@register.filter(name='deck_average')

def deck_average(deck):
    total_elixir = 0
    for card in deck:
        total_elixir += card.elixir

    return {'avg': total_elixir/8, '4-avg': total_elixir/4}
