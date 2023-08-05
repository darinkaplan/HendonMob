from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'poker_scraper'
urlpatterns = [
    path('', views.search, name='search'),
    path('hm_search/', views.hendon_mob_search, name='hm_search'),
    path('player/<int:pk>/', views.display, name='display'),
    path('compare/', views.compare, name='compare'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add_player/', views.add_player, name='add_player'),
    path('add_hm_player/', views.hendon_mob_add_player, name='add_hm_player'),
    path('delete_hm_player/', views.hendon_mob_delete_player, name='delete_hm_player'),
    path('add_tournament_result/', views.add_tournament_result, name='add_tournament_result'),
    path('select_friends/', views.select_friends, name='select_friends'),
    path('view_friends/', views.view_friends, name='view_friends'),
]
