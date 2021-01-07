from django.db import models
from django.apps import apps

from shared.models import BaseTeam


class NBATeam(BaseTeam):
    """A team in the NBA"""
    state = models.TextField(blank=True)
    year_founded = models.TextField(blank=True)

    nba_api_id = models.CharField(max_length=12, unique=True, editable=False)

    def get_current_player_memberships(self):
        return self.player_memberships.filter(end_date=None)

    def get_current_players(self):
        NBAPlayer = apps.get_model('nba', 'NBAPlayer')

        return NBAPlayer.objects.filter(
            team_membership__in=self.get_current_player_memberships()
        )