from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
import poker_scraper.views

urlpatterns = [
    path('', poker_scraper.views.empty, name='empty'),
    path('poker_scraper/', include('poker_scraper.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
