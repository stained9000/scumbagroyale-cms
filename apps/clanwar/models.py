from django.core.urlresolvers import reverse
from django.db import models
import requests
import json
from datetime import datetime
from time import strftime
import pytz


class ClanStandings(models.Model):
    clan_img = models.URLField(default="https://royaleapi.com/static/img/badge/no_clan.png")
    battles_played =  models.IntegerField()
    crowns = models.IntegerField()
    name = models.CharField(max_length=100)
    participants = models.IntegerField()
    clan_tag = models.CharField(max_length=100)
    war_trophies = models.IntegerField()
    war_trophies_change = models.IntegerField()
    war_trophies_start = models.IntegerField()
    wins = models.IntegerField()
    war_id = models.CharField(max_length=100)

    class Meta:
        unique_together = (('war_id', 'clan_tag'),)

class WarParticipation(models.Model):
    war_id = models.CharField(max_length=200)
    time_id = models.DateTimeField(default=datetime.now)
    season = models.CharField(max_length=200)
    player_tag = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    cards_earned = models.CharField(max_length=200)
    battles_played = models.CharField(max_length=200)
    wins = models.CharField(max_length=200)
    clan_tag = models.CharField(max_length=200)

    class Meta:
        unique_together = (("war_id", "player_tag"),)

    def refresh(self, request):
        url = 'http://api.royaleapi.com/clans/' + request.GET['clan_tag'].upper()    + '/warlog'

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()


        try:
            if 'error' in data.keys():
                return False

        except:



            war_dict = dict()

            for war in data:
                war_id = list()

                for clan in war['standings']:
                    war_id.append(clan['tag'])

                war_id.sort()
                war_id = "".join(war_id)

                war_dict[war_id] = {"date": war['createdDate'], "participants": war['participants'], "season": war['seasonNumber'], "standings": war['standings']}

            for war in war_dict.keys():

                for clan in war_dict[war]['standings']:
                    obj, created = ClanStandings.objects.get_or_create(
                    war_id = war,
                    clan_img = clan['badge']['image'],
                    battles_played = clan['battlesPlayed'],
                    crowns = clan['crowns'],
                    name = clan['name'],
                    participants = clan['participants'],
                    clan_tag = clan ['tag'],
                    war_trophies = clan['warTrophies'],
                    war_trophies_change = clan['warTrophiesChange'],
                    war_trophies_start = clan['warTrophies'] - clan['warTrophiesChange'],
                    wins = clan['wins']
                    )

                for participant in war_dict[war]['participants']:
                    obj, created = WarParticipation.objects.get_or_create(
                    war_id = war,
                    time_id = datetime.utcfromtimestamp(war_dict [war]['date']).replace(tzinfo=pytz.utc),
                    season = war_dict[war]['season'],
                    player_tag = participant['tag'],
                    name = participant['name'],
                    cards_earned = participant['cardsEarned'],
                    battles_played = participant['battlesPlayed'],
                    wins = participant['wins'],
                    clan_tag = request.GET['clan_tag'].upper()
                    )



            return True



    def __str__(self):
        return self.war_id

class Player(models.Model):
    player_tag = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    trophies = models.IntegerField()
    arena_number = models.CharField(max_length=200)
    arena_name = models.CharField(max_length=200)
    clan_name = models.CharField(max_length=200)
    clan_tag = models.CharField(max_length=200)
    clan_img = models.URLField(default="https://royaleapi.com/static/img/badge/no_clan.png")
    role = models.CharField(max_length=200)
    donations = models.IntegerField(default=0)
    donations_delta = models.IntegerField(default=0)
    donatios_received = models.IntegerField(default=0)
    cards_found = models.IntegerField(default=0)
    challenge_cards = models.IntegerField(default=0)
    challenge_max_wins = models.IntegerField(default=0)
    clan_cards_collected = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    max_trophies = models.IntegerField(default=0)
    current_best_trophies = models.IntegerField(default=0)
    best_season_trophies = models.IntegerField(default=0)
    previous_season_trophies = models.IntegerField(default=0)
    three_crown_wins = models.IntegerField(default=0)
    total_donations = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    draws_percent = models.FloatField(default=0)
    losses = models.IntegerField(default=0)
    losses_percent = models.FloatField(default=0)
    total_games = models.IntegerField(default=0)
    war_day_wins = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    wins_percent = models.FloatField(default=0)

    class Meta:
        unique_together = (("player_tag"),)

    def update(self, request):
        url = 'http://api.royaleapi.com/player/' + str(request.GET['player_tag']).upper()

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

        class returnFalse(dict):
            def __missing__(self, key):
                return {}

        class returnZero(dict):
            def __missing__(self, key):
                return 0

        class returnNone(dict):
            def __missing__(self, key):
                return None


        if type(data['clan']) == type(None) and "leagueStatistics" in data.keys():
            obj, created = Player.objects.update_or_create(
            player_tag = data['tag'],
            defaults={
            "name": data['name'],
            "trophies": data['trophies'],
            "arena_number": data['arena']['arena'],
            "arena_name": data['arena']['name'],
            "clan_img": "https://royaleapi.com/static/img/badge/no_clan.png",
            "cards_found": data['stats']['cardsFound'],
            "challenge_cards": data['stats']['challengeCardsWon'],
            "challenge_max_wins": data['stats']['challengeMaxWins'],
            "level": data['stats']['level'],
            "max_trophies": data['stats']['maxTrophies'],
            "current_best_trophies": data['leagueStatistics']['currentSeason']['bestTrophies'],
            "best_season_trophies": data['leagueStatistics']['bestSeason']['trophies'],
            "previous_season_trophies": data['leagueStatistics']['previousSeason']['trophies'],
            "three_crown_wins": data['stats']['threeCrownWins'],
            "draws": data['games']['draws'],
            "draws_percent": data['games']['drawsPercent'],
            "losses": data['games']['losses'],
            "losses_percent": data['games']['lossesPercent'],
            "total_games": data['games']['total'],
            "wins": data['games']['wins'],
            "wins_percent": data['games']['winsPercent']
            }
            )

        elif type(data['clan']) == type(None) and "leagueStatistics" not in data.keys():
            obj, created = Player.objects.update_or_create(
            player_tag = data['tag'],
            defaults={
            "name": data['name'],
            "trophies": data['trophies'],
            "arena_number": data['arena']['arena'],
            "arena_name": data['arena']['name'],
            "clan_img": "https://royaleapi.com/static/img/badge/no_clan.png",
            "cards_found": data['stats']['cardsFound'],
            "challenge_cards": data['stats']['challengeCardsWon'],
            "challenge_max_wins": data['stats']['challengeMaxWins'],
            "level": data['stats']['level'],
            "max_trophies": data['stats']['maxTrophies'],
            "three_crown_wins": data['stats']['threeCrownWins'],
            "draws": data['games']['draws'],
            "draws_percent": data['games']['drawsPercent'],
            "losses": data['games']['losses'],
            "losses_percent": data['games']['lossesPercent'],
            "total_games": data['games']['total'],
            "wins": data['games']['wins'],
            "wins_percent": data['games']['winsPercent']
            }
            )


        elif "leagueStatistics" in data.keys():
            obj, created = Player.objects.update_or_create(
                player_tag = data['tag'],
                defaults={
                "name": data['name'],
                "trophies": data['trophies'],
                "arena_number": data['arena']['arena'],
                "arena_name": data['arena']['name'],
                "clan_name": data['clan']['name'],
                "clan_tag": data['clan']['tag'],
                "clan_img": data['clan']['badge']['image'],
                "role": data['clan']['role'],
                "donations": data['clan']['donations'],
                "donations_delta": data['clan']['donationsDelta'],
                "donatios_received": data['clan']['donationsReceived'],
                "cards_found": data['stats']['cardsFound'],
                "challenge_cards": data['stats']['challengeCardsWon'],
                "challenge_max_wins": data['stats']['challengeMaxWins'],
                "clan_cards_collected": data['stats']['clanCardsCollected'],
                "level": data['stats']['level'],
                "max_trophies": data['stats']['maxTrophies'],
                "current_best_trophies": returnZero(data['leagueStatistics']['currentSeason'])['bestTrophies'],
                "best_season_trophies": returnZero(returnFalse(data['leagueStatistics'])['bestSeason'])['trophies'],
                "previous_season_trophies": returnZero(returnFalse(data['leagueStatistics'])['previousSeason'])['trophies'],
                "three_crown_wins": data['stats']['threeCrownWins'],
                "total_donations": data['stats']['totalDonations'],
                "draws": data['games']['draws'],
                "draws_percent": data['games']['drawsPercent'],
                "losses": data['games']['losses'],
                "losses_percent": data['games']['lossesPercent'],
                "total_games": data['games']['total'],
                "war_day_wins": data['games']['warDayWins'],
                "wins": data['games']['wins'],
                "wins_percent": data['games']['winsPercent']
                }
                )
        elif "leagueStatistics" not in data.keys():
            obj, created = Player.objects.update_or_create(
                player_tag = data['tag'],
                defaults={
                "name": data['name'],
                "trophies": data['trophies'],
                "arena_number": data['arena']['arena'],
                "arena_name": data['arena']['name'],
                "clan_name": data['clan']['name'],
                "clan_tag": data['clan']['tag'],
                "clan_img": data['clan']['badge']['image'],
                "role": data['clan']['role'],
                "donations": data['clan']['donations'],
                "donations_delta": data['clan']['donationsDelta'],
                "donatios_received": data['clan']['donationsReceived'],
                "cards_found": data['stats']['cardsFound'],
                "challenge_cards": data['stats']['challengeCardsWon'],
                "challenge_max_wins": data['stats']['challengeMaxWins'],
                "clan_cards_collected": data['stats']['clanCardsCollected'],
                "level": data['stats']['level'],
                "max_trophies": data['stats']['maxTrophies'],
                "three_crown_wins": data['stats']['threeCrownWins'],
                "total_donations": data['stats']['totalDonations'],
                "draws": data['games']['draws'],
                "draws_percent": data['games']['drawsPercent'],
                "losses": data['games']['losses'],
                "losses_percent": data['games']['lossesPercent'],
                "total_games": data['games']['total'],
                "war_day_wins": data['games']['warDayWins'],
                "wins": data['games']['wins'],
                "wins_percent": data['games']['winsPercent']
                }
                )




    def __str__(self):
        return self.player_tag

#Falta funcion para crear decks
class Decks(models.Model):
    id = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.id


#----------CONSTANTES-------------------------------------------

#Test Funcion para agregar cartas a decks.
class Cards(models.Model):
    id = models.IntegerField(primary_key=True)
    key = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    elixir = models.IntegerField(default=0)
    type = models.CharField(max_length=30)
    rarity = models.CharField(max_length=30)
    arena = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    decks = models.ManyToManyField(Decks, blank=True)
    icon = models.URLField(null=True)

    def __str__(self):
        return self.name

    def update(self):
        url = "https://api.royaleapi.com/constants"

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

        for card in data['cards']:
            obj, created = Cards.objects.get_or_create(
            id = card['id'],
            key = card['key'],
            name = card['name'],
            elixir = card['elixir'],
            type = card['type'],
            rarity = card['rarity'],
            arena = card['arena'],
            description = card['description']
            )

        return "Cards updated successfully"

    def add_to_deck(self, deck_id, card_id):
        d = Decks.objects.filter(id=deckid)
        c = Cards.objects.filter(id=card_id)

        c.decks.add(d)

class Badges(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    image = models.URLField(default="https://royaleapi.com/static/img/badge/no_clan.png")

    def __str__(self):
        return self.name

    def update(self):
        url = "https://api.royaleapi.com/constants"

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

        for badge in data['alliance_badges']:
            obj, created = Badges.objects.get_or_create(
            id = badge['id'],
            category = badge['category'],
            name = badge['name'],
            image = "https://royaleapi.github.io/cr-api-assets/badges/" + badge['name'] + ".png",
            )

        return "Badges updated successfully"

class Locations(models.Model):
    id = models.IntegerField(primary_key=True)
    key = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    isCountry = models.BooleanField()

    def __str__(self):
        return self.name

    def update(self):
        url = "https://api.royaleapi.com/constants"

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

        for location in data['regions']:
            obj, created = Locations.objects.get_or_create(
            id = location['id'],
            key = location['key'],
            name = location['name'],
            isCountry = location['isCountry'],
            )

        return "Locations updated successfully"

class Arenas(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    name = models.CharField(max_length=30)
    arena = models.IntegerField(default=0)
    tv_arena = models.CharField(max_length=30)
    is_in_use = models.BooleanField()
    training_camp = models.BooleanField()
    trophy_limit = models.IntegerField(default=0)
    max_trophy_limit = models.IntegerField(default=0)
    demote_trophy_limit = models.IntegerField(default=0)
    chest_reward_multiplier = models.IntegerField(default=0)
    shop_chest_reward_multiplier = models.IntegerField(default=0)
    request_size = models.IntegerField(default=0)
    max_donation_count_common = models.IntegerField(default=0)
    max_donation_count_rare = models.IntegerField(default=0)
    max_donation_count_epic = models.IntegerField(default=0)
    matchmaking_min_trophy_delta = models.IntegerField(default=0)
    matchmaking_max_trophy_delta = models.IntegerField(default=0)
    matchmaking_max_seconds = models.IntegerField(default=0)
    daily_donation_capacity_limit = models.IntegerField(default=0)
    battle_reward_gold = models.IntegerField(default=0)
    season_reward_chest = models.CharField(max_length=30, blank=True, null=True)
    quest_cycle = models.CharField(max_length=30)
    force_quest_chest_cycle = models.CharField(max_length=30, blank=True, null=True)
    key = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    subtitle = models.CharField(max_length=30)
    arena_id = models.IntegerField(default=0)
    league_id = models.CharField(max_length=30)
    icon = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def update(self):
        url = "https://api.royaleapi.com/constants"

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

        for arena_current in data['arenas']:
            obj, created = Arenas.objects.update_or_create(
            id = arena_current['id'],
            defaults={
            'name' : arena_current['name'],
            'arena' : arena_current['arena'],
            'tv_arena' : arena_current['tv_arena'],
            'is_in_use' : arena_current['is_in_use'],
            'training_camp' : arena_current['training_camp'],
            'trophy_limit' : arena_current['trophy_limit'],
            'demote_trophy_limit' : arena_current['demote_trophy_limit'],
            'chest_reward_multiplier' : arena_current['chest_reward_multiplier'],
            'shop_chest_reward_multiplier' : arena_current['shop_chest_reward_multiplier'],
            'request_size' : arena_current['request_size'],
            'max_donation_count_common' : arena_current['max_donation_count_common'],
            'max_donation_count_rare' : arena_current['max_donation_count_rare'],
            'max_donation_count_epic' : arena_current['max_donation_count_epic'],
            'matchmaking_min_trophy_delta' : arena_current['matchmaking_min_trophy_delta'],
            'matchmaking_max_trophy_delta' : arena_current['matchmaking_min_trophy_delta'],
            'matchmaking_max_seconds' : arena_current['matchmaking_max_seconds'],
            'daily_donation_capacity_limit' : arena_current['daily_donation_capacity_limit'],
            'battle_reward_gold' : arena_current['battle_reward_gold'],
            'season_reward_chest' : arena_current['season_reward_chest'],
            'quest_cycle' : arena_current['quest_cycle'],
            'force_quest_chest_cycle' : arena_current['force_quest_chest_cycle'],
            'key' : arena_current['key'],
            'title' : arena_current['title'],
            'subtitle' : arena_current['subtitle'],
            'arena_id' : arena_current['arena_id'],
            'league_id' : str(arena_current['league_id']),
            'icon': "https://royaleapi.com/static/img/arenas/" + arena_current['key'] + ".png",
            }
            )

        return "Arenas updated successfully"

#------------FIN DE CONSTANTES---------------------------------



#update
class Clans(models.Model):
    tag = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=30)
    score = models.IntegerField(default=0)
    memberCount = models.IntegerField(default=0)
    requiredScore = models.IntegerField(default=0)
    donations = models.IntegerField(default=0)
    badge = models.ForeignKey(Badges, on_delete=models.DO_NOTHING)
    location = models.ForeignKey(Locations, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    def update(self, clan_tag):
        url = "https://api.royaleapi.com/clan/" + clan_tag

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

        clan, created = Clans.objects.update_or_create(
        tag = data['tag'],
        defaults={
        'name' : data['name'],
        'description' : data['description'],
        'type' : data['type'],
        'score' : data['score'],
        'memberCount' : data['memberCount'],
        'requiredScore' : data['requiredScore'],
        'donations' : data['donations'],
        'badge' : Badges.objects.get(id=data['badge']['id']),
        'location' : Locations.objects.get(key=data['location']['code'])
        }
        )

#update
class Players(models.Model):
    tag = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=30)
    trophies = models.IntegerField(default=0)
    rank = models.IntegerField(default=0, null=True)
    arena = models.ForeignKey(Arenas, on_delete=models.CASCADE, blank=True, null=True)
    clan = models.ForeignKey(Clans, on_delete=models.CASCADE, blank=True, null=True)
    role = models.CharField(max_length=30)
    donations = models.IntegerField(default=0)
    donationsReceived = models.IntegerField(default=0)
    donationsDelta = models.IntegerField(default=0)
    deckLink = models.URLField()
    currentDeck = models.ForeignKey(Decks)

    def __str__(self):
        return self.name

    #Necesita ser optimizado. Incluir update de Stats, Games y leagueStatistics
    def update(self, player_tag):
        url = "https://api.royaleapi.com/player/" + player_tag
        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
        }
        response = requests.request("GET", url, headers=headers)
        data = response.json()

        #Crear variable para pasar a Stats.update()
        stats_data = data['stats']

        #Crear variable para pasar a CurrentSeason.update()
        current_season_data = data['leagueStatistics']['currentSeason']

        try:
            #Crear variable para pasar a PreviousSeason.update()
            previous_season_data = data['leagueStatistics']['previousSeason']
        except:
            previous_season_data = None
        #Crear variable para pasar a Games.update()
        games_data = data['games']

        #Verificar si deck existe o crear
        cards_list = list()

        for card in data['currentDeck']:
            cards_list.append(card['id'])

        cards_list = "-".join(str(id) for id in sorted(cards_list))

        deck, created = Decks.objects.get_or_create(
        id = cards_list,
        )

        if created:
            for card in data['currentDeck']:
                Cards.objects.filter(id=card['id'])[0].decks.add(deck)
                Cards.objects.filter(id=card['id'])[0].save()

        if not data['clan'] == None:
            #Update o create Clan
            clan = Clans()
            clan.update(data['clan']['tag'])

        if data['clan'] == None:
            player, created = Players.objects.update_or_create(
            tag = player_tag,
            defaults={
            'name' : data['name'],
            'trophies' : data['trophies'],
            'deckLink' : data['deckLink'],
            'arena' : Arenas.objects.get(arena=data['arena']['arenaID']),
            'currentDeck' : deck,
            }
            )

        else:
            player, created = Players.objects.update_or_create(
            tag = player_tag,
            defaults={
            'name' : data['name'],
            'trophies' : data['trophies'],
            'rank' : data['rank'],
            'role' : data['clan']['role'],
            'donations' : data['clan']['donations'],
            'donationsReceived' : data['clan']['donationsReceived'],
            'donationsDelta' : data['clan']['donationsDelta'],
            'deckLink' : data['deckLink'],
            'arena' : Arenas.objects.get(arena=data['arena']['arenaID']),
            'clan' : Clans.objects.get(tag=data['clan']['tag']),
            'currentDeck' : deck,
            }
            )

        return stats_data, current_season_data, previous_season_data, games_data


#update
class Games(models.Model):
    player = models.OneToOneField(Players, primary_key=True, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    tournamentGames = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    warDayWins = models.IntegerField(default=0)
    winsPercent = models.FloatField(default=0)
    losses = models.IntegerField(default=0)
    lossesPercent = models.FloatField(default=0)
    draws = models.IntegerField(default=0)
    drawsPercent = models.FloatField(default=0)

    def __str__(self):
        return self.player.name

    def update(self, player_tag, games_data):
        game, created = Games.objects.update_or_create(
        player = Players.objects.get(tag=player_tag),
        defaults={
        'total' : games_data['total'],
        'tournamentGames' : games_data['tournamentGames'],
        'wins' : games_data['wins'],
        'warDayWins' : games_data['warDayWins'],
        'winsPercent' : games_data['winsPercent'],
        'losses' : games_data['losses'],
        'lossesPercent' : games_data['lossesPercent'],
        'draws' : games_data['draws'],
        'drawsPercent' : games_data['drawsPercent'],
        }
        )

#update
class Stats(models.Model):
    player = models.OneToOneField(Players, primary_key=True, on_delete=models.CASCADE)
    clanCardsCollected = models.IntegerField(default=0)
    tournamentCardsWon = models.IntegerField(default=0)
    maxTrophies = models.IntegerField(default=0)
    threeCrownWins = models.IntegerField(default=0)
    cardsFound = models.IntegerField(default=0)
    favoriteCard = models.ForeignKey(Cards, on_delete=models.CASCADE)
    totalDonations = models.IntegerField(default=0)
    challengeMaxWins = models.IntegerField(default=0)
    challengeCardsWon = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.player.tag + " - " + self.player.name

    def update(self, player_tag, stats_data):
        stats, created = Stats.objects.update_or_create(
        player = Players.objects.get(tag=player_tag),
        defaults={
        'clanCardsCollected' : stats_data['clanCardsCollected'],
        'tournamentCardsWon' : stats_data['tournamentCardsWon'],
        'maxTrophies' : stats_data['maxTrophies'],
        'threeCrownWins' : stats_data['threeCrownWins'],
        'cardsFound' : stats_data['cardsFound'],
        'totalDonations' : stats_data['totalDonations'],
        'challengeMaxWins' : stats_data['challengeMaxWins'],
        'challengeCardsWon' : stats_data['challengeCardsWon'],
        'favoriteCard': Cards.objects.get(id=stats_data['favoriteCard']['id']),
        'level' : stats_data['level'],
        }
        )

#update
class Battles(models.Model):
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    utcTime = models.DateTimeField(default=datetime.now)
    type = models.CharField(max_length=30)
    challengeType = models.CharField(max_length=30, null=True, blank=True)
    mode_name = models.CharField(max_length=30)
    mode_deck = models.CharField(max_length=30, blank=True, null=True)
    mode_cardLevels = models.CharField(max_length=30, null=True, blank=True)
    mode_overtimeSeconds = models.IntegerField(default=0, null=True)
    mode_players = models.CharField(max_length=30, null=True, blank=True)
    mode_sameDeck = models.NullBooleanField(default=False)
    winCountBefore = models.IntegerField(default=0, null=True)
    deckType = models.CharField(max_length=30)
    teamSize = models.IntegerField(default=0)
    winner = models.IntegerField(default=0)
    teamCrowns = models.IntegerField(default=0)
    opponentCrowns = models.IntegerField(default=0)

    class Meta:
        unique_together=(('player', 'utcTime'),)

    def __str__(self):
        return self.player.name + self.utcTime

    def update(self, player_tag):
        url = "https://api.royaleapi.com/player/" + player_tag + "/battles"

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

        for battle in data:
            if 'cardLevels' in battle['mode'].keys():
                battle_obj, created = Battles.objects.update_or_create(
                player = Players.objects.get(tag=player_tag),
                utcTime = datetime.utcfromtimestamp(battle['utcTime']).replace(tzinfo=pytz.utc),
                defaults={
                'type' : battle['type'],
                'challengeType' : battle['challengeType'],
                'mode_name' : battle['mode']['name'],
                'mode_deck' : battle['mode']['deck'],
                'mode_cardLevels' : battle['mode']['cardLevels'],
                'mode_overtimeSeconds' : battle['mode']['overtimeSeconds'],
                'mode_players' : battle['mode']['players'],
                'mode_sameDeck' : battle['mode']['sameDeck'],
                'winCountBefore' : battle['winCountBefore'],
                'deckType' : battle['deckType'],
                'teamSize' : battle['teamSize'],
                'winner' : battle['winner'],
                'teamCrowns' : battle['teamCrowns'],
                'opponentCrowns' : battle['opponentCrowns'],
                }
                )
            else:
                battle_obj, created = Battles.objects.update_or_create(
                player = Players.objects.get(tag=player_tag),
                utcTime = datetime.utcfromtimestamp(battle['utcTime']).replace(tzinfo=pytz.utc),
                defaults={
                'type' : battle['type'],
                'challengeType' : battle['challengeType'],
                'mode_name' : battle['mode']['name'],
                'winCountBefore' : battle['winCountBefore'],
                'deckType' : battle['deckType'],
                'teamSize' : battle['teamSize'],
                'winner' : battle['winner'],
                'teamCrowns' : battle['teamCrowns'],
                'opponentCrowns' : battle['opponentCrowns'],
                }
                )
            team = Teams()
            team.update(battle_obj, battle['team'])

            opponent = Opponents()
            opponent.update(battle_obj, battle['opponent'])

#update
class Teams(models.Model):
    battle = models.ForeignKey(Battles, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=200)
    player_tag = models.CharField(max_length=200)
    startTrophies = models.IntegerField(default=0, null=True, blank=True)
    crownsEarned = models.IntegerField(default=0)
    clan_name = models.CharField(max_length=200, blank=True, null=True)
    clan_tag = models.CharField(max_length=200, blank=True, null=True)
    deck = models.ForeignKey(Decks)

    class Meta:
        unique_together=(('battle', 'player_tag'),)

    def __str__(self):
        return self.player_name

    def update(self, battle_obj, team_list):

        for team_player in team_list:

            #Verificar si deck existe o crear
            cards_list = list()

            for card in team_player['deck']:
                cards_list.append(card['id'])

            cards_list = "-".join(str(id) for id in sorted(cards_list))

            player_deck, created = Decks.objects.get_or_create(
            id = cards_list,
            )

            if created:
                for card in team_player['deck']:
                    Cards.objects.get(id=card['id']).decks.add(player_deck)
                    Cards.objects.get(id=card['id']).save()

            try:
                x = team_player['startTrophies']
            except:
                team_player['startTrophies'] = None

            if team_player['clan'] == None:
                team, created = Teams.objects.update_or_create(
                battle = battle_obj,
                deck = player_deck,
                defaults={
                'player_name' : team_player['name'],
                'player_tag' : team_player['tag'],
                'startTrophies' : team_player['startTrophies'],
                'crownsEarned' : team_player['crownsEarned'],
                }
                )
            else:
                team, created = Teams.objects.update_or_create(
                battle = battle_obj,
                deck = player_deck,
                defaults={
                'player_name' : team_player['name'],
                'player_tag' : team_player['tag'],
                'startTrophies' : team_player['startTrophies'],
                'clan_name' : team_player['clan']['name'],
                'clan_tag' : team_player['clan']['tag'],
                'crownsEarned' : team_player['crownsEarned'],
                }
                )

#update
class Opponents(models.Model):
    battle = models.ForeignKey(Battles, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=200)
    player_tag = models.CharField(max_length=200)
    startTrophies = models.IntegerField(default=0, null=True, blank=True)
    crownsEarned = models.IntegerField(default=0)
    clan_name = models.CharField(max_length=200, blank=True, null=True)
    clan_tag = models.CharField(max_length=200, blank=True, null=True)
    deck = models.ForeignKey(Decks)

    class Meta:
        unique_together=(('battle', 'player_tag'),)

    def __str__(self):
        return self.player_name

    def update(self, battle_obj, team_list):
        for opponent_player in team_list:
            #Verificar si deck existe o crear
            cards_list = list()

            for card in opponent_player['deck']:
                cards_list.append(card['id'])

            cards_list = "-".join(str(id) for id in sorted(cards_list))

            player_deck, created = Decks.objects.get_or_create(
            id = cards_list,
            )

            if created:
                for card in opponent_player['deck']:
                    Cards.objects.get(id=card['id']).decks.add(player_deck)
                    Cards.objects.get(id=card['id']).save()

            try:
                x = opponent_player['startTrophies']
            except:
                opponent_player['startTrophies'] = None

            if opponent_player['clan'] == None:
                opponent, created = Opponents.objects.update_or_create(
                battle = battle_obj,
                deck = player_deck,
                defaults={
                'player_name' : opponent_player['name'],
                'player_tag' : opponent_player['tag'],
                'startTrophies' : opponent_player['startTrophies'],
                'crownsEarned' : opponent_player['crownsEarned'],
                }
                )

            else:

                opponent, created = Opponents.objects.update_or_create(
                battle = battle_obj,
                deck = player_deck,
                defaults={
                'player_name' : opponent_player['name'],
                'player_tag' : opponent_player['tag'],
                'startTrophies' : opponent_player['startTrophies'],
                'clan_name' : opponent_player['clan']['name'],
                'clan_tag' : opponent_player['clan']['tag'],
                'crownsEarned' : opponent_player['crownsEarned'],
                }
                )

#update
class CurrentSeason(models.Model):
    player = models.OneToOneField(Players, primary_key=True, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0, null=True, blank=True)
    trophies = models.IntegerField(default=0)
    bestTrophies = models.IntegerField(default=0)

    def __str__(self):
        return 'CurrentSeason'

    def update(self, player_tag, current_season_data):
        if 'rank' in current_season_data.keys():
            season, created = CurrentSeason.objects.update_or_create(
            player = Players.objects.get(tag=player_tag),
            defaults={
            'rank' : current_season_data['rank'],
            'trophies' : current_season_data['trophies'],
            'bestTrophies' : current_season_data['bestTrophies'],
            }
            )
        else:
            season, created = CurrentSeason.objects.update_or_create(
            player = Players.objects.get(tag=player_tag),
            defaults={
            'trophies' : current_season_data['trophies'],
            'bestTrophies' : current_season_data['bestTrophies'],
            }
            )

#update
class PreviousSeasons(models.Model):
    season = models.CharField(max_length=30)
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0, null=True, blank=True)
    trophies = models.IntegerField(default=0)
    bestTrophies = models.IntegerField(default=0, blank=True, null=True)
    arena = models.ForeignKey(Arenas, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together=(('season', 'player'),)

    def __str__(self):
        return self.player.tag + ": " + self.season

    def update(self, player_tag, previous_season_data):
        if previous_season_data == None:
            return None
        elif 'rank' in previous_season_data.keys():
            season, created = PreviousSeasons.objects.update_or_create(
            season = previous_season_data['id'],
            player = Players.objects.get(tag=player_tag),
            defaults={
            'rank' : previous_season_data['rank'],
            'trophies' : previous_season_data['trophies'],
            'bestTrophies' : previous_season_data['bestTrophies'],
            'arena'  : Arenas.objects.get(trophy_limit__lte=previous_season_data['trophies'], max_trophy_limit__gt=previous_season_data['trophies']),
            }
            )
        else:
            season, created = PreviousSeasons.objects.update_or_create(
            season = previous_season_data['id'],
            player = Players.objects.get(tag=player_tag),
            defaults={
            'rank' : None,
            'trophies' : previous_season_data['trophies'],
            'bestTrophies' : previous_season_data['bestTrophies'],
            'arena'  : Arenas.objects.get(trophy_limit__lte=previous_season_data['trophies'], max_trophy_limit__gt=previous_season_data['trophies']),
            }
            )

        return season
