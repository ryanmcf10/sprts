from datetime import date

from django.db import models
from django.db.models import Q
from django.apps import apps

from shared.models import BaseTeam


class NBATeam(BaseTeam):
    """A team in the NBA"""
    state = models.TextField(blank=True)
    year_founded = models.TextField(blank=True)

    nba_api_id = models.CharField(max_length=12, unique=True, editable=False)

    def get_current_player_memberships(self):
        return self.player_memberships.filter(end_date=None)

    def get_roster_on_date(self, date):
        """
        Return an NBAPlayer QuerySet of the players on this team on 'date'.
        :param date:
        :return:
        """
        NBAPlayer = apps.get_model('nba', 'NBAPlayer')

        return NBAPlayer.objects.filter(
            id__in=self.player_memberships.filter(
                Q(end_date__isnull=True) | Q(end_date__gte=date),
                start_date__lte=date
            ).values_list('player__id', flat=True)
        )

    def get_current_roster(self):
        """
        Return an NBAPlayer QuerySet of the players on this team today.
        :return:
        """
        return self.get_roster_on_date(date.today())
