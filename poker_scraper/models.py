from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    hendon_mob_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    img_url = models.URLField(null=True, blank=True)
    birthplace = models.CharField(max_length=100, null=True, blank=True)


class TournamentResult(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    position = models.IntegerField(null=True)
    prize = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    gpi_points = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    poy_points = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    date = models.DateField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(Player, blank=True)
