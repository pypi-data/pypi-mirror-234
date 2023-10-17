from django.apps import AppConfig

from . import __version__


class HuntingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "hunting"
    label = "hunting"
    verbose_name = f'AA Hunting v{__version__}'
