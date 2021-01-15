import time

from django.apps import apps
from django.db import models


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

    def get_home_team_gamelog(self):
        return self.team_gamelogs.get(team=self.home_team)

    def get_away_team_gamelog(self):
        return self.team_gamelogs.get(team=self.away_team)

    def get_home_team_roster(self):
        return self.home_team.get_roster_on_date(self.date)

    def get_away_team_roster(self):
        return self.away_team.get_roster_on_date(self.date)

    def get_winning_team(self):
        return self.team_gamelogs.select_related('team').get(result='W').team

    def get_losing_team(self):
        return self.team_gamelogs.select_related('team').get(result='L').team

    def get_winning_team_gamelog(self):
        return self.team_gamelogs.get(result='W')

    def get_losing_team_gamelog(self):
        return self.team_gamelogs.get(result='L')

    def create_gamelogs(self):
        try:
            self.create_team_gamelogs()
        except Exception as e:
            raise e

        self.create_player_gamelogs()

    def create_team_gamelogs(self):
        NBATeamGameLog = apps.get_model('nba', 'NBATeamGameLog')

        NBATeamGameLog.objects.create(
            game=self,
            team=self.away_team
        )

        NBATeamGameLog.objects.create(
            game=self,
            team=self.home_team
        )

    def create_player_gamelogs(self):
        NBAPlayerGameLog = apps.get_model('nba', 'NBAPlayerGameLog')

        for player in self.get_home_team_roster():
            try:
                NBAPlayerGameLog.objects.create(
                    game=self,
                    player=player
                )
            except Exception:
                continue

            time.sleep(1)

        for player in self.get_away_team_roster():

            try:
                NBAPlayerGameLog.objects.create(
                    game=self,
                    player=player
                )
            except Exception:
                continue

            time.sleep(1)
