# Generated by Django 4.2.3 on 2023-07-28 00:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hendon_mob_id', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('img_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friends', models.ManyToManyField(blank=True, to='poker_scraper.player')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament_name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('position', models.IntegerField()),
                ('prize', models.DecimalField(decimal_places=2, max_digits=10)),
                ('gpi_points', models.DecimalField(decimal_places=2, max_digits=6)),
                ('poy_points', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poker_scraper.player')),
            ],
        ),
    ]
