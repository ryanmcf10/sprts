from django.db import models

from shared.models import BaseTeam


class NBATeam(BaseTeam):
    """A team in the NBA"""
    state = models.TextField(blank=True)
    year_founded = models.TextField(blank=True)

    nba_api_id = models.CharField(max_length=12, unique=True, editable=False)