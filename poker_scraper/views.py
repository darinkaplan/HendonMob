from .models import Player, TournamentResult, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PlayerForm, TournamentResultForm
from .scraper import tournament_results, player_search


def search(request):
    query = request.GET.get('q', '')
    players = Player.objects.filter(name__icontains=query)
    return render(request, 'poker_scraper/search.html', {'players': players})

def hendon_mob_search(request):
    query = request.GET.get('q', '')
    hendon_mob_players = player_search(query) if query != '' else None

    #determine if each player in db for button usage
    if hendon_mob_players is not None:
        for x in hendon_mob_players:
            x['in_db'] = Player.objects.filter(hendon_mob_id=x['id']).exists()

    return render(request, 'poker_scraper/hm_search.html', {'players': hendon_mob_players})

def hendon_mob_add_player(request):
    query = request.GET.get('q', '')
    id = request.GET.get('id', '')
    hendon_mob_players = player_search(query) if query != '' else None
    player_found = [x for x in hendon_mob_players if x['id']==id]
    player = player_found[0] if len(player_found)>0 else None
    if player is not None:
        # check to see if player is already in db
        p = Player.objects.filter(hendon_mob_id=id)
        if len(p)==0: # Not in local db
            new_player = Player(
                hendon_mob_id=id,
                name=player['name'],
                img_url=player['image'],
                birthplace=player['birthplace'],
            )
            new_player.save()

    #determine if each player in db for button usage
    for x in hendon_mob_players:
        x['in_db'] = Player.objects.filter(hendon_mob_id=x['id']).exists()

    return render(request, 'poker_scraper/hm_search.html', {'players': hendon_mob_players})

def hendon_mob_delete_player(request):
    query = request.GET.get('q', '')
    id = request.GET.get('id', '')
    p = Player.objects.filter(hendon_mob_id=id).delete()

    #determine if each player in db for button usage
    hendon_mob_players = player_search(query) if query != '' else []
    for x in hendon_mob_players:
        x['in_db'] = Player.objects.filter(hendon_mob_id=x['id']).exists()

    return render(request, 'poker_scraper/hm_search.html', {'players': hendon_mob_players})


def display(request, pk):
    player = Player.objects.get(pk=pk)
    items = tournament_results(player.hendon_mob_id)
    results = []

    for item in items:
        result = TournamentResult(
            player=player,
            tournament_name=item['event_name'],
            position=item['place'],
            prize=item['currency'],
            gpi_points=item['points'],
            date=item['date']
        )
        results.append(result)

    return render(request, 'poker_scraper/display.html', {'player': player, 'tournament_results': results})

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


def select_friends(request):
    profile = UserProfile.objects.get(user=request.user)
    current_friends = profile.friends.all()

    if request.method == 'POST':
        selected_friends_ids = request.POST.getlist('friend')

        for player in Player.objects.all():
            if str(player.id) in selected_friends_ids:
                profile.friends.add(player)
            elif player in current_friends:
                profile.friends.remove(player)

        return redirect('poker_scraper:view_friends')
    else:
        players = Player.objects.all()
        player_friends = [{'player': player, 'is_friend': player in current_friends} for player in players]
        return render(request, 'poker_scraper/select_friends.html', {'players': player_friends})



@login_required
def view_friends(request):
    profile = UserProfile.objects.get(user=request.user)
    friends = profile.friends.all()
    return render(request, 'poker_scraper/view_friends.html', {'friends': friends})
