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

    def get_winning_team(self):
        return self.team_gamelogs.select_related('team').get(result='W').team

    def get_losing_team(self):
        return self.team_gamelogs.select_related('team').get(result='L').team

    def get_winning_team_gamelog(self):
        return self.team_gamelogs.get(result='W')

    def get_losing_team_gamelog(self):
        return self.team_gamelogs.get(result='L')

    def create_team_gamelogs(self):
        NBATeamGameLog = apps.get_model('nba', 'NBATeamGameLog')

        gamelogs = NBATeamGameLog.objects.filter(game=self)

        if gamelogs.count() == 2:
            raise Exception("NBATeamGameLogs have already been created for this Game.")
        elif gamelogs.count() == 1:
            gamelogs.first().delete()  # Something went wrong and only 1 GameLog was created. Delete it and try again.

        NBATeamGameLog.objects.create(
            game=self,
            team=self.away_team
        )

        NBATeamGameLog.objects.create(
            game=self,
            team=self.home_team
        )
