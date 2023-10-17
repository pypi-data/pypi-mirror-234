from django.apps import AppConfig

from . import __version__


class IncursionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "incursions"
    verbose_name = f'AA Incursions v{__version__}'

    def ready(self):
        import incursions.signals  # noqa:F401
