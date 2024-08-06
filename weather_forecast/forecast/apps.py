from django.apps import AppConfig

class ForecastConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forecast'

    def ready(self):
        import forecast.signals

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals