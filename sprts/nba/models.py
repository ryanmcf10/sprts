from django.db import models

from shared.models import BasePlayer, BaseTeam


class NBAPlayer(BasePlayer):
    """A player in the NBA"""
    nba_api_id = models.CharField(max_length=12, unique=True, editable=False)
    is_active = models.BooleanField(default=True)


class NBATeam(BaseTeam):
    """A team in the NBA"""
    state = models.TextField(blank=True)
    year_founded = models.TextField(blank=True)

    nba_api_id = models.CharField(max_length=12, unique=True, editable=False)


class NBAGame(models.Model):
    date = models.DateField(blank=True)
    home_team = models.ForeignKey('NBATeam', on_delete=models.PROTECT, related_name='home_games')
    away_team = models.ForeignKey('NBATeam', on_delete=models.PROTECT, related_name='away_games')


"""
class NBATeamMembership(models.Model):
    player = models.ForeignKey('NBAPlayer', on_delete=models.CASCADE, related_name='team_memberships', related_query_name='team_membership')
    team = models.ForeignKey('NBATeam', on_delete=models.PROTECT, related_name='player_memberships', related_query_name='player_membership')

    start_date = models.DateField(default='2020-12-22')
    end_date = models.DateField(blank=True, null=True)

    def clean(self):
        # TODO: implement logic to prevent overlapping dates
"""