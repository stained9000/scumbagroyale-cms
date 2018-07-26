from django.db.models import Count
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
import requests
import json
from .models import WarParticipation, Player, ClanStandings, Cards, Badges, Locations, Arenas, Decks, Clans, Players, Games, Stats, Battles, Teams, Opponents, CurrentSeason, PreviousSeasons


# Create your views here.

def homepage(request):
    return render(request, 'clanwar/homepage.html')

def war_paticipation_query(request):
    return render(request, 'clanwar/war_participation_query.html')

def war_participation(request):
    cw = current_war(request.GET['clan_tag'])

    war = WarParticipation()
    result = war.refresh(request)

    if result == True:
        clan_std = ClanStandings.objects.filter(war_id__contains=request.GET['clan_tag'].upper()).filter(clan_tag=request.GET['clan_tag'].upper())
        oponent_std = ClanStandings.objects.filter(war_id__contains=request.GET['clan_tag'].upper()).exclude(clan_tag=request.GET['clan_tag'].upper())
        id = WarParticipation.objects.filter(war_id__contains=request.GET['clan_tag'].upper()).order_by('-time_id').values('war_id', 'time_id', "season").distinct()
        participation = WarParticipation.objects.filter(war_id__contains=request.GET['clan_tag'].upper()).filter(clan_tag=request.GET['clan_tag'].upper()).order_by('war_id')
        return render(request, 'clanwar/war_participation.html', {'participation': participation, 'id': id, "clan_std": clan_std, "oponent_std": oponent_std, "cw": cw})

    else:
        participation = "Invalid Input. Please provide a valid Clan Tag."
        return render(request, 'clanwar/war_participation.html', {'participation': participation})

def player_participation(request):
    play = Player()
    result = play.update(request)

    participation = WarParticipation.objects.filter(player_tag=request.GET['player_tag'].upper()).order_by('-time_id')
    player_info = Player.objects.filter(player_tag=request.GET['player_tag'].upper())
    return render(request, 'clanwar/player_participation.html', {'participation': participation, 'player_info': player_info})

def back_war_participation(request):

    return redirect(request, 'clanwar/war_participation.html')

def current_war(tag):
    url = 'http://api.royaleapi.com/clans/' + tag + '/war'

    headers = {
    'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()

    return data

def top_clans(request):
    try:
        url = 'http://api.royaleapi.com/top/clans/' + request.GET['country'][:2].lower()
        country_code = request.GET['country'][:2].upper()
        country_name = "in " + request.GET['country'][2:]


    except:
        url = 'http://api.royaleapi.com/top/clans/'
        country_code = "_INT"
        country_name = "Global"

    headers = {
    'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()

    return render(request, 'clanwar/top_clans.html', {'data': data, 'country_code': country_code, 'country_name': country_name,})

def top_players(request):
    try:
        url = 'https://api.royaleapi.com/top/players/' + request.GET['country'][:2].lower()
        country_code = request.GET['country'][:2].upper()
        country_name = "in " + request.GET['country'][2:]


    except:
        url = 'https://api.royaleapi.com/top/players/'
        country_code = "_INT"
        country_name = "Global"

    headers = {
    'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    """
    for player in data:
        p = Players()
        p.update(player['tag'])
    """

    most_common = Decks.objects.values('cards__id').annotate(id_count = Count('cards__id')).order_by('-id_count')[0]['cards__id']
    card_obj = Cards.objects.filter(id=most_common)


    return render(request, 'clanwar/top_players.html', {'data': data, 'country_code': country_code, 'country_name': country_name, 'card_obj': card_obj,})

def popular_decks(request):
    url = 'https://api.royaleapi.com/popular/decks'

    headers = {
    'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()

    decks = Teams.objects.all().values('deck__id').annotate(id_count = Count('deck__id')).order_by('-id_count')
    decks_list = list()
    total_games = 0
    for deck in decks:
        decks_list.append({'deck_obj': Decks.objects.get(id=deck['deck__id']), 'count': deck['id_count']})
        total_games += deck['id_count']
    deck_count = len(decks_list[0:10])

    return render(request, 'clanwar/popular_decks.html', {'data': data, 'decks_list': decks_list[0:10], 'total_games': total_games, 'deck_count': deck_count})

def update_constants_cards(request):
    cards = Cards()
    cards_update = cards.update()
    return render(request, 'clanwar/update_constants_cards.html', {'cards_update': cards_update,})


def update_constants_badges(request):
    badges = Badges()
    badges_update = badges.update()
    return render(request, 'clanwar/update_constants_badges.html', {'badges_update': badges_update,})


def update_constants_locations(request):
    locations = Locations()
    locations_update = locations.update()
    return render(request, 'clanwar/update_constants_locations.html', {'locations_update': locations_update,})


def update_constants_arenas(request):
    arenas = Arenas()
    arenas_update = arenas.update()
    return render(request, 'clanwar/update_constants_arenas.html', {'arenas_update': arenas_update,})

def player_profile(request):
    player_tag = request.GET['player_tag']
    player = Players()
    stats_data, current_season_data, previous_season_data , games_data = player.update(player_tag)
    stats = Stats()
    stats.update(player_tag, stats_data)
    currentSeason = CurrentSeason()
    currentSeason.update(player_tag, current_season_data)
    previousSeason = PreviousSeasons()
    previousSeason = previousSeason.update(player_tag, previous_season_data)
    games = Games()
    games.update(player_tag, games_data)


    player = Players.objects.filter(tag=player_tag)[0]
    return render(request, 'clanwar/player_profile.html', {'player': player, 'previousSeason': previousSeason})

def player_battles(request):
    player_tag = request.GET['player_tag']
    player = Players()
    stats_data, current_season_data, previous_season_data , games_data = player.update(player_tag)
    battles = Battles()
    battles.update(player_tag)


    player = Players.objects.filter(tag=player_tag)[0]
    battles = Battles.objects.filter(player=player)
    return render(request, 'clanwar/player_battles.html', {'player': player, 'battles': battles})

def player_decks(request):
    player_tag = request.GET['player_tag']
    player = Players()
    stats_data, current_season_data, previous_season_data , games_data = player.update(player_tag)
    battles = Battles()
    battles.update(player_tag)


    player = Players.objects.filter(tag=player_tag)[0]
    battles = Battles.objects.filter(player=player)
    decks = Teams.objects.filter(player_tag=player_tag).values('deck__id').annotate(id_count = Count('deck__id')).order_by('-id_count')
    decks_list = list()
    total_games = 0
    for deck in decks:
        decks_list.append({'deck_obj': Decks.objects.get(id=deck['deck__id']), 'count': deck['id_count']})
        total_games += deck['id_count']

    barbarian_count = Teams.objects.filter(player_tag=player_tag).filter(deck__id__contains='26000008').count()

    return render(request, 'clanwar/player_decks.html', {'player': player, 'battles': battles, 'decks_list': decks_list, 'total_games': total_games, 'barbarian_count': barbarian_count})

def player_analytics(request):
    player_tag = request.GET['player_tag']
    player = Players()
    stats_data, current_season_data, previous_season_data , games_data = player.update(player_tag)
    battles = Battles()
    battles.update(player_tag)


    player = Players.objects.filter(tag=player_tag)[0]
    battles = Battles.objects.filter(player=player)

    total_games = battles.count()

    count_list = list()

    for card in Cards.objects.all():
        card_count = Teams.objects.filter(player_tag=player_tag).filter(deck__id__contains=str(card.id)).count()
        card_obj = card
        wins_count = Teams.objects.filter(player_tag=player_tag).filter(deck__id__contains=str(card.id), battle__winner__gt=0).count()

        count_list.append({'card_obj': [card_obj,], 'card_count': card_count, 'wins_count': wins_count})

    return render(request, 'clanwar/player_analytics.html', {'player': player, 'battles': battles, 'total_games': total_games, 'count_list': count_list})

def clan_profile(request):
    clan_tag = request.GET['clan_tag']
    clan = Clans()
    clan, members = clan.update(clan_tag)

    return render(request, 'clanwar/clan_profile.html', {'clan': clan, 'members': members})
