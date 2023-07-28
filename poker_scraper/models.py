from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    hendon_mob_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    img_url = models.URLField()
    # Add any other fields as necessary

class TournamentResult(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament_name = models.CharField(max_length=200)
    description = models.TextField()
    position = models.IntegerField()
    prize = models.DecimalField(max_digits=10, decimal_places=2)
    gpi_points = models.DecimalField(max_digits=6, decimal_places=2)
    poy_points = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(Player, blank=True)
