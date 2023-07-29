from django.apps import AppConfig


class PokerScraperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'poker_scraper'

    def ready(self):
        import poker_scraper.signals
