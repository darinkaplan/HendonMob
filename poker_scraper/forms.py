from django import forms
from .models import Player, TournamentResult

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'  # or list the fields you want to include in your form

class TournamentResultForm(forms.ModelForm):
    class Meta:
        model = TournamentResult
        fields = '__all__'  # or list the fields you want to include in your form
