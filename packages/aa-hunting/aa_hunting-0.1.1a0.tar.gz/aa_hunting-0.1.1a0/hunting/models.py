import datetime

from eveuniverse.models import (
    EveConstellation, EveRegion, EveSolarSystem, EveStation, EveType,
)

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo
from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ("basic_access", "Can access the Hunting App"),
            ("target_view", "Can modify a Hunting target"),
            ("target_add", "Can add a Hunting target"),
            ("target_edit", "Can modify a Hunting target"),
            ("locator_view", "Can view LocateCharMsg's"),
            ("locator_addtoken", "Can add a Token for locator agents"),
            ("locator_request", "Can request a locate"),
            ("locator_action", "Can perform a locate, and mark it as actioned"),
        )


class Agent(models.Model):
    # https://sde.zzeve.com/agtAgents.json
    character = models.OneToOneField(
        EveCharacter, verbose_name=_("Eve Character"), on_delete=models.CASCADE)
    DIVISION_CHOICES = [
        (18, _("R&D")),
        (22, _("Distribution")),
        (23, _("Mining")),
        (24, _("Security")),
        (25, _("Business")),
        (26, _("Exploration")),
        (27, _("Industry")),
        (28, _("Military")),
        (29, _("Advanced Military")),
        (37, _("Paragon"))]
    division = models.IntegerField(
        _("Division"),
        choices=DIVISION_CHOICES,
        default=28)
    corporation = models.ForeignKey(
        EveCorporationInfo, verbose_name=_("Corporation"), on_delete=models.CASCADE)
    station = models.ForeignKey(
        EveStation, verbose_name=_("Station"), on_delete=models.CASCADE)
    LEVEL_CHOICES = [
        (1, _("Level 1")),
        (2, _("Level 2")),
        (3, _("Level 3")),
        (4, _("Level 4")),
        (5, _("Level 5"))]
    level = models.IntegerField(
        _("Level 1<>5"),
        choices=LEVEL_CHOICES
    )
    TYPE_CHOICES = [
        (1, _("NonAgent")),
        (2, _("BasicAgent")),
        (3, _("TutorialAgent")),
        (4, _("ResearchAgent")),
        (5, _("CONCORDAgent")),
        (6, _("GenericStorylineMissionAgent")),
        (7, _("StorylineMissionAgent")),
        (8, _("EventMissionAgent")),
        (9, _("FactionalWarfareAgent")),
        (10, _("EpicArcAgent")),
        (11, _("AuraAgent")),
        (12, _("CareerAgent")),
    ]
    type = models.IntegerField(
        _("Type"),
        choices=TYPE_CHOICES,
        help_text="")
    is_locator = models.BooleanField(_("Locator Agent"))

    @property
    def cooldown(self) -> int:
        """
        Agent Cooldown in Minutes
        """
        if self.level == 1:
            return 5
        elif self.level == 2:
            return 5
        elif self.level == 3:
            return 15
        elif self.level == 4:
            return 30
        elif self.level == 5:
            return 60
        else:
            return 0

    def __str__(self):
        return f'{self.station.name}'

    class Meta:
        """
        Meta definitions
        """
        default_permissions = ()
        verbose_name = _("Locator Agent")


class LocateCharAgent(models.Model):
    # Meta model, not active used by LocateCharMsg <> LocateChar / Character
    # Defines a relationship between a character and their valid agents

    agent = models.ForeignKey(
        Agent, verbose_name=_("Locator Agent"), on_delete=models.CASCADE)
    character = models.ForeignKey(
        EveCharacter, verbose_name=_("Character"), on_delete=models.CASCADE)

    @property
    def available(self) -> bool:
        cooldown = timezone.now() + datetime.timedelta(minutes=self.agent.cooldown)
        last_run = LocateCharMsg.objects.filter(
            character=self.character,
            agent=self.agent).latest('timestamp')
        return cooldown > last_run.timestamp

    class Meta:
        verbose_name = _("Character - Locator Agent")
        constraints = [
            models.UniqueConstraint(fields=['agent', 'character'], name="LocateCharAgent"),
        ]

    def __str__(self):
        return f"{self.agent.character.character_name}{self.character.character_name}"

    def get_or_create_submodels(self, agent_id, character_id):
        # not sure this function actually does what i want
        try:
            self.agent = EveCharacter.objects.get(character_id=character_id)
        except EveCharacter.DoesNotExist:
            self.character = EveCharacter.objects.create_character(character_id=character_id)

        try:
            self.character = EveCharacter.objects.get(character_id=agent_id)
        except EveCharacter.DoesNotExist:
            self.character = EveCharacter.objects.create_character(character_id=agent_id)

        return self.save()


class LocateChar(models.Model):
    character = models.OneToOneField(
        EveCharacter, verbose_name=_("Character"),
        on_delete=models.CASCADE)
    locate_char_agent = models.ManyToManyField(
        LocateCharAgent, verbose_name=_("Valid Locator Agents"),
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cache_expiry = models.DateTimeField(
        default=datetime.datetime.min)

    def __str__(self):
        return f'{self.character.character_name}'

    class Meta:
        """
        Meta definitions
        """
        default_permissions = ()
        verbose_name = _("Character")
        indexes = (
            models.Index(fields=['character']),
        )


class LocateCharMsg(models.Model):
    # id is the notification id from ESI
    locate_character = models.ForeignKey(
        LocateChar, verbose_name=_("Locator Character"), on_delete=models.CASCADE)
    sender_id = models.IntegerField(
        _("Sender Agent ID"))
    timestamp = models.DateTimeField(
        _("Timestamp"), auto_now=False, auto_now_add=False)
    character = models.ForeignKey(
        EveCharacter, verbose_name=_("Character"), on_delete=models.CASCADE)
    solar_system = models.ForeignKey(
        EveSolarSystem, verbose_name=_("Solar Systen"), on_delete=models.CASCADE)
    constellation = models.ForeignKey(
        EveConstellation, verbose_name=_("Constellation"), on_delete=models.CASCADE)
    region = models.ForeignKey(
        EveRegion, verbose_name=_("Region"), on_delete=models.CASCADE)
    station = models.ForeignKey(
        EveStation, verbose_name=_("Station"), on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        """
        Meta definitions
        """
        default_permissions = ()
        verbose_name = _("LocateCharMsg Notification")
        indexes = (
            models.Index(fields=['locate_character']),
            models.Index(fields=['character']),
            models.Index(fields=['sender_id']),
        )

    def __str__(self):
        return f'{self.character.character_name} {self.solar_system.name} {self.timestamp}'


class TargetAlt(models.Model):
    character = models.ForeignKey(
        EveCharacter, verbose_name=_("Character"), on_delete=models.CASCADE)
    hard_cyno = models.BooleanField(_("Hard Cyno"))
    beacon_cyno = models.BooleanField(_("Anchored Cyno Beacon"))
    scout = models.BooleanField(_("Scout"))
    pilot = models.BooleanField(_("Can Pilot the Target Ship"))

    def _lastcharmsg(self):
        return LocateCharMsg.objects.filter(
            character=self.character).latest('timestamp')

    @property
    def locatecharmsg_set(self):
        return LocateCharMsg.objects.filter(
            character=self.character).order_by('timestamp')

    @property
    def last_locatecharmsg(self):
        return self._lastcharmsg()

    @property
    def last_locatecharmsg_oneday(self) -> bool:
        time_ref = timezone.now() - datetime.timedelta(days=1)

        if (self._lastcharmsg().timestamp < time_ref):
            return True
        else:
            return False

    @property
    def last_locatecharmsg_onehour(self) -> bool:
        time_ref = timezone.now() - datetime.timedelta(hours=1)

        if (self._lastcharmsg().timestamp < time_ref):
            return True
        else:
            return False

    @property
    def related_alts(self):
        return self.target_set.all()

    class Meta:
        """
        Meta definitions
        """
        default_permissions = ()
        verbose_name = _("Target Alt")
        indexes = (
            models.Index(fields=['character']),
        )

    def __str__(self):
        return f'{self.character.character_name}'


class Target(models.Model):
    character = models.ForeignKey(
        EveCharacter, verbose_name=_("Character"), on_delete=models.CASCADE)
    ship = models.ForeignKey(
        EveType, verbose_name=_("Ship"), on_delete=models.CASCADE)
    alts = models.ManyToManyField(
        TargetAlt, verbose_name=_("Alts"), blank=True)
    last_ship_location = models.ForeignKey(
        EveSolarSystem, verbose_name=_("Last Known Ship Location"), on_delete=models.CASCADE)

    def _lastcharmsg(self):
        return LocateCharMsg.objects.filter(
            character=self.character).latest('timestamp')

    @property
    def locatecharmsg_set(self):
        return LocateCharMsg.objects.filter(
            character=self.character).order_by('timestamp')

    @property
    def last_locatecharmsg(self):
        return self._lastcharmsg()

    @property
    def last_locatecharmsg_oneday(self) -> bool:
        time_ref = timezone.now() - datetime.timedelta(days=1)

        if (self._lastcharmsg().timestamp < time_ref):
            return True
        else:
            return False

    @property
    def last_locatecharmsg_onehour(self) -> bool:
        time_ref = timezone.now() - datetime.timedelta(hours=1)

        if (self._lastcharmsg().timestamp < time_ref):
            return True
        else:
            return False

    class Meta:
        """
        Meta definitions
        """
        default_permissions = ()

    def __str__(self):
        return f'{self.character.character_name} {self.ship.name}'


class TargetGroup(models.Model):
    models.ManyToManyField(
        Target, verbose_name=_("Target"))

    class Meta:
        """
        Meta definitions
        """
        default_permissions = ()


class Note(models.Model):
    target = models.ForeignKey(
        Target, verbose_name=_("Hunting Target"), on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, verbose_name=_("Author"), on_delete=models.CASCADE)
    text = models.TextField(_("Note Text"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta definitions
        """
        default_permissions = ()
