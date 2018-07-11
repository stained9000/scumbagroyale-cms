from django.contrib import admin
from .models import WarParticipation, Cards, Badges, Locations, Arenas, Decks, Clans, Players, Games, Stats, Battles, Teams, Opponents, CurrentSeason, PreviousSeasons

# Register your models here.

admin.site.register(WarParticipation)
admin.site.register(Cards)
admin.site.register(Badges)
admin.site.register(Locations)
admin.site.register(Arenas)
admin.site.register(Decks)
admin.site.register(Clans)
admin.site.register(Players)
admin.site.register(Games)
admin.site.register(Stats)
admin.site.register(Battles)
admin.site.register(Teams)
admin.site.register(Opponents)
admin.site.register(CurrentSeason)
admin.site.register(PreviousSeasons)
