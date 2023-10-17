from django.contrib import admin

from allianceauth.services.hooks import get_extension_logger

from .models import (
    Agent, LocateChar, LocateCharMsg, Note, Target, TargetAlt, TargetGroup,
)

logger = get_extension_logger(__name__)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(LocateChar)
class LocateCharAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(LocateCharMsg)
class LocateCharMsgAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(TargetAlt)
class TargetAltAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(TargetGroup)
class TargetGroupAdmin(admin.ModelAdmin):
    list_display = ('id', )
