import json
from datetime import datetime

from django.db import models

from nba_api.stats.endpoints import LeagueGameFinder


class NBAGame(models.Model):
    date = models.DateField(null=True)

    home_team = models.ForeignKey('NBATeam',
                                  related_name='home_games',
                                  related_query_name='home_game',
                                  on_delete=models.PROTECT)

    away_team = models.ForeignKey('NBATeam',
                                  related_name='away_games',
                                  related_query_name='away_game',
                                  on_delete=models.PROTECT)

    nba_api_id = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = 'NBA Game'
        verbose_name_plural = 'NBA Games'

    def __str__(self):
        return f"[{self.date}] {self.away_team} @ {self.home_team}"

    def fetch_nba_api_id(self):
        # date needs to be in the form MM/DD/YYYY
        if not (self.date and self.away_team and self.home_team):
            raise Exception("Cannot fetch NBA API ID without knowing the date and teams for this game.")

        data = json.loads(LeagueGameFinder(
            player_or_team_abbreviation = 'T',
            team_id_nullable = self.home_team.nba_api_id,
            vs_team_id_nullable = self.away_team.nba_api_id,
            date_from_nullable = datetime.strftime(self.date, '%m/%d/%Y'),
            date_to_nullable=datetime.strftime(self.date, '%m/%d/%Y')
        ).get_json())
