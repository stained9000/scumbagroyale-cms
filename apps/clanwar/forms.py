from django import forms
from .models import WarParticipation, Cards, Badges, Locations, Arenas, Decks, Clans, Players, Games, Stats, Battles, Teams, Opponents, CurrentSeason, PreviousSeasons

class TagForm(forms.ModelForm):

    class Meta:
        model = WarParticipation
        fields = ('player_tag',)

class CardsForm(forms.ModelForm):

    class Meta:
        model = Cards
        fields = '__all__'

class BadgesForm(forms.ModelForm):

    class Meta:
        model = Badges
        fields = '__all__'

class LocationsForm(forms.ModelForm):

    class Meta:
        model = Locations
        fields = '__all__'

class ArenasForm(forms.ModelForm):

    class Meta:
        model = Arenas
        fields = '__all__'

class DecksForm(forms.ModelForm):

    class Meta:
        model = Decks
        fields = '__all__'

class ClansForm(forms.ModelForm):

    class Meta:
        model = Clans
        fields = '__all__'

class PlayersForm(forms.ModelForm):

    class Meta:
        model = Players
        fields = '__all__'

class GamesForm(forms.ModelForm):

    class Meta:
        model = Games
        fields = '__all__'

class StatsForm(forms.ModelForm):

    class Meta:
        model = Stats
        fields = '__all__'

class BattlesForm(forms.ModelForm):

    class Meta:
        model = Battles
        fields = '__all__'

class TeamsForm(forms.ModelForm):

    class Meta:
        model = Teams
        fields = '__all__'

class OpponentsForm(forms.ModelForm):

    class Meta:
        model = Opponents
        fields = '__all__'

class CurrentSeasonForm(forms.ModelForm):

    class Meta:
        model = CurrentSeason
        fields = '__all__'

class PreviousSeasonsForm(forms.ModelForm):

    class Meta:
        model = PreviousSeasons
        fields = '__all__'
