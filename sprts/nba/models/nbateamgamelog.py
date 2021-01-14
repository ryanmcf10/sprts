from datetime import datetime

from django.db import models

from nba.utils.fetch import fetch_team_gamelog


class NBATeamGameLog(models.Model):
    team = models.ForeignKey(
        'NBATeam',
        related_name='gamelogs',
        related_query_name='gamelog',
        on_delete=models.PROTECT
    )

    game = models.ForeignKey(
        'NBAGame',
        related_name='team_gamelogs',
        related_query_name='team_gamelog',
        on_delete=models.PROTECT
    )

    WIN = 'W'
    LOSS = 'L'

    RESULT_CHOICES = (
        (WIN, 'Win'),
        (LOSS, 'Loss')
    )

    result = models.CharField(max_length=1, choices=RESULT_CHOICES)

    points = models.PositiveSmallIntegerField()

    field_goals_made = models.PositiveSmallIntegerField()
    field_goals_attempted = models.PositiveSmallIntegerField()

    three_pointers_made = models.PositiveSmallIntegerField()
    three_pointers_attempted = models.PositiveSmallIntegerField()

    free_throws_made = models.PositiveSmallIntegerField()
    free_throws_attempted = models.PositiveSmallIntegerField()

    offensive_rebounds = models.PositiveSmallIntegerField()
    defensive_rebounds = models.PositiveSmallIntegerField()

    assists = models.PositiveSmallIntegerField()
    steals = models.PositiveSmallIntegerField()
    blocks = models.PositiveSmallIntegerField()
    turnovers = models.PositiveSmallIntegerField()
    team_fouls = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'NBA Team GameLog'
        verbose_name_plural = 'NBA Team GameLogs'
        unique_together = ['game', 'team']

        ordering = ['game__date']

    def __str__(self):
        return f"[{datetime.strftime(self.game.date, '%m/%d/%Y')}] {self.team}"

    def save(self, *args, **kwargs):
        # fetch gamelog data from NBA API on the initial save only
        if self.id is None:
            self.fetch_gamelog()

        super(NBATeamGameLog, self).save(*args, **kwargs)

    @property
    def field_goal_percentage(self):
        return round(self.field_goals_made / self.field_goals_attempted, 3)

    @property
    def three_point_percentage(self):
        return round(self.three_pointers_made / self.three_pointers_attempted, 3)

    @property
    def free_throw_percentage(self):
        return round(self.free_throws_made / self.free_throws_attempted, 3)

    @property
    def rebounds(self):
        return self.offensive_rebounds + self.defensive_rebounds

    def fetch_gamelog(self):
        gamelog = fetch_team_gamelog(self.game, self.team)

        self.result = gamelog['WL']
        self.points = gamelog['PTS']
        self.field_goals_made = gamelog['FGM']
        self.field_goals_attempted = gamelog['FGA']
        self.three_pointers_made = gamelog['FG3M']
        self.three_pointers_attempted = gamelog['FG3A']
        self.free_throws_made = gamelog['FTM']
        self.free_throws_attempted = gamelog['FTA']
        self.offensive_rebounds = gamelog['OREB']
        self.defensive_rebounds = gamelog['DREB']
        self.assists = gamelog['AST']
        self.steals = gamelog['STL']
        self.blocks = gamelog['BLK']
        self.turnovers = gamelog['TOV']
        self.team_fouls = gamelog['PF']

    def get_opposing_team(self):
        if self.game.home_team == self.team:
            return self.game.away_team
        else:
            return self.game.home_team

    def get_opposing_team_gamelog(self):
        if self.game.home_team == self.team:
            return self.game.away_team_gamelog
        else:
            return self.game.home_team_gamelog
