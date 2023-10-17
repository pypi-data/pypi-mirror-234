from django.apps import AppConfig

from . import __version__


class TopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "top"
    label = "top"
    verbose_name = f'AA Top v{__version__}'
