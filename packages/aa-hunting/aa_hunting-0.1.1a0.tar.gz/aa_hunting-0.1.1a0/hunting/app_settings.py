from django.apps import apps
from django.conf import settings

HUNTING_TASK_PRIORITY = getattr(settings, 'HUNTING_TASK_PRIORITY', "7")

HUNTING_ENABLE_CORPTOOLS_IMPORT = getattr(settings, 'HUNTING_ENABLE_CORPTOOLS_IMPORT', True)


def discordbot_active():
    return apps.is_installed('aadiscordbot')


def corptools_active():
    return apps.is_installed('corptools')


def killtracker_active():
    return apps.is_installed('killtracker')
