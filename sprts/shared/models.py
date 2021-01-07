from django.db import models


class BasePlayer(models.Model):
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class BaseTeam(models.Model):
    city = models.TextField(blank=True)
    nickname = models.TextField(blank=True)
    abbreviation = models.TextField(blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.city} {self.nickname}".strip()
