from datetime import datetime

from django.db import models

class NBAPlayerGameLog(models.Model):
    player = models.ForeignKey('NBAPlayer',
                               related_name='gamelogs',
                               related_query_name='gamelog',
                               on_delete=models.PROTECT)

    game = models.ForeignKey('NBAGame',
                             related_name='player_gamelogs',
                             related_query_name='player_gamelog',
                             on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'NBA Player GameLog'
        verbose_name_plural = 'NBA Player GameLogs'
        unique_together = ['player', 'game']

        ordering = ['game__date']

    def __str__(self):
        return f"[{datetime.strftime(self.game.date, '%m/%d/%Y')}] {self.player}"