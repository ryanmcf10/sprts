from datetime import datetime

from django.db import models

from nba.utils.fetch import fetch_player_gamelog


class NBAPlayerGameLog(models.Model):
    player = models.ForeignKey('NBAPlayer',
                               related_name='gamelogs',
                               related_query_name='gamelog',
                               on_delete=models.PROTECT)

    game = models.ForeignKey('NBAGame',
                             related_name='player_gamelogs',
                             related_query_name='player_gamelog',
                             on_delete=models.PROTECT)

    minutes_played = models.PositiveSmallIntegerField(default=0)
    points = models.PositiveSmallIntegerField(default=0)

    field_goals_made = models.PositiveSmallIntegerField(default=0)
    field_goals_attempted = models.PositiveSmallIntegerField(default=0)

    three_pointers_made = models.PositiveSmallIntegerField(default=0)
    three_pointers_attempted = models.PositiveSmallIntegerField(default=0)

    free_throws_made = models.PositiveSmallIntegerField(default=0)
    free_throws_attempted = models.PositiveSmallIntegerField(default=0)

    offensive_rebounds = models.PositiveSmallIntegerField(default=0)
    defensive_rebounds = models.PositiveSmallIntegerField(default=0)

    assists = models.PositiveSmallIntegerField(default=0)
    steals = models.PositiveSmallIntegerField(default=0)
    blocks = models.PositiveSmallIntegerField(default=0)
    turnovers = models.PositiveSmallIntegerField(default=0)
    personal_fouls = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'NBA Player GameLog'
        verbose_name_plural = 'NBA Player GameLogs'
        unique_together = ['player', 'game']

        ordering = ['game__date']

    def __str__(self):
        return f"[{datetime.strftime(self.game.date, '%m/%d/%Y')}] {self.player}"

    def save(self, *args, **kwargs):
        # fetch gamelog data from NBA API on the initial save only
        if self.id is None:
            try:
                self.fetch_gamelog()
            except Exception:
                raise Exception("Unable to find a gamelog for this player/game combination.")

        super(NBAPlayerGameLog, self).save(*args, **kwargs)

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

    def get_player_team(self):
        return self.player.get_team_on_date(self.game.date)

    def fetch_gamelog(self):
        gamelog = fetch_player_gamelog(self.game, self.player)

        self.points = gamelog['PTS']
        self.minutes_played = gamelog['MIN']
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
