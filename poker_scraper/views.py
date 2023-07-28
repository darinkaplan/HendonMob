from .models import Player, TournamentResult, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import PlayerForm, TournamentResultForm


def search(request):
    query = request.GET.get('q', '')
    players = Player.objects.filter(name__icontains=query)
    return render(request, 'poker_scraper/search.html', {'players': players})

def display(request, pk):
    player = Player.objects.get(pk=pk)
    tournament_results = TournamentResult.objects.filter(player=player)
    return render(request, 'poker_scraper/display.html', {'player': player, 'tournament_results': tournament_results})

def compare(request):
    # Depends on your requirements
    pass

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirect to login page after registering
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('poker_scraper:search')
    else:
        form = PlayerForm()
    return render(request, 'poker_scraper/add_player.html', {'form': form})

def add_tournament_result(request):
    if request.method == 'POST':
        form = TournamentResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('poker_scraper:search')
    else:
        form = TournamentResultForm()
    return render(request, 'poker_scraper/add_tournament_result.html', {'form': form})