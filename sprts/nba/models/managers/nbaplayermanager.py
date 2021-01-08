from django.db import models
from django.db.models import Q

class NBAPlayerQuerySet(models.QuerySet):

    def guards(self):
        return self.filter(
            Q(position_1='G') |
            Q(position_2='G')
        )

    def forwards(self):
        return self.filter(
            Q(position_1='F') |
            Q(position_2='F')
        )

    def centers(self):
        return self.filter(
            Q(position_1='C') |
            Q(position_2='C')
        )

NBAPlayerManager = NBAPlayerQuerySet.as_manager()
