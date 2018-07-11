from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^clanwar/participation$', views.war_participation, name='war_participation'),
    url(r'^clanwar/participation_query$', views.war_paticipation_query, name='war_participation_query'),
    url(r'^clanwar/player_participation$', views.player_participation, name='player_participation'),
    url(r'^ladder/top_clans$', views.top_clans, name='top_clans'),
    url(r'^ladder/top_players$', views.top_players, name='top_players'),
    url(r'^popular_decks$', views.popular_decks, name='popular_decks'),
    url(r'^player_profile$', views.player_profile, name='player_profile'),
    url(r'^update_constants_cards$', views.update_constants_cards, name='update_constants_cards'),
    url(r'^update_constants_badges$', views.update_constants_badges, name='update_constants_badges'),
    url(r'^update_constants_locations$', views.update_constants_locations, name='update_constants_locations'),
    url(r'^update_constants_arenas$', views.update_constants_arenas, name='update_constants_arenas'),
]
