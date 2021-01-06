from django.db import models


class NBAGame(models.Model):
    date = models.DateField(blank=True)
    home_team = models.ForeignKey('NBATeam', on_delete=models.PROTECT, related_name='home_games')
    away_team = models.ForeignKey('NBATeam', on_delete=models.PROTECT, related_name='away_games')
