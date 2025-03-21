from django.apps import AppConfig

class MyWeatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myweat'

    def ready(self):
        import myweat.signals  # Upewnij się, że sygnały są załadowane
