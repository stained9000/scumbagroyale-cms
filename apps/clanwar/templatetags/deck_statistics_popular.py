from django.template.defaultfilters import register
from apps.clanwar.models import Teams

@register.filter(name='deck_statistics_popular')

def deck_statistics_popular(id):
    battles = Teams.objects.all().filter(deck__id=id)
    winners_count = battles.filter(battle__winner__gt=0).count()
    losers_count = battles.filter(battle__winner__lt=0).count()
    draws_count = battles.filter(battle__winner=0).count()

    return {'wins': winners_count, 'losses': losers_count, 'draws': draws_count}
