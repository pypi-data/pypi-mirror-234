import datetime

import requests
import yaml
from celery import shared_task
from eveuniverse.models import (
    EveConstellation, EveRegion, EveSolarSystem, EveStation,
)

from django.utils import timezone

from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo
from allianceauth.services.hooks import get_extension_logger
from esi.models import Token

from .app_settings import HUNTING_ENABLE_CORPTOOLS_IMPORT, corptools_active
from .models import Agent, LocateChar, LocateCharMsg
from .providers import get_characters_character_id_notifications

logger = get_extension_logger(__name__)

SQUIZZ_AGT_AGENTS = "https://sde.zzeve.com/agtAgents.json"

"""
agentLocation:
    3: 10000001
    4: 20000007
    5: 30000044
    15: 60012163
characterID: 90406623
messageIndex: 0 <- 0=Sleezebag, 1=Scumsucker
targetLocation:
    3: 10000002
    4: 20000020
    5: 30000142
    15: 60003760
"""


def parse_notification_text(text: str) -> dict:
    return yaml.load(text, Loader=yaml.UnsafeLoader)


@shared_task()
def pull_notifications():
    for character in LocateChar.objects.all():
        if character.cache_expiry < timezone.now() or character.cache_expiry is None:
            pull_character_notifications(
                character_id=character.character.character_id)


def pull_character_notifications(character_id: int):
    logger.debug(f"pull_character_notifications for: {character_id}")

    locate_char = LocateChar.objects.get(character__character_id=character_id)

    req_scopes = ['esi-characters.read_notifications.v1']
    token = Token.get_token(character_id, req_scopes)

    if not token:
        return "No Tokens"

    _bulkcreate = []

    notifications, response = get_characters_character_id_notifications(
        character_id, token)

    for notification in notifications:
        if notification["type"] == "LocateCharMsg":
            notification_text = parse_notification_text(notification["text"])
            solar_system, fetched = EveSolarSystem.objects.get_or_create_esi(
                id=notification_text["targetLocation"][5])
            constellation, fetched = EveConstellation.objects.get_or_create_esi(
                id=notification_text["targetLocation"][4])
            region, fetched = EveRegion.objects.get_or_create_esi(
                id=notification_text["targetLocation"][3])
            try:
                character = EveCharacter.objects.get(
                    character_id=notification_text['characterID'])
            except EveCharacter.DoesNotExist:
                character = EveCharacter.objects.create_character(
                    character_id=notification_text['characterID'])
            locatecharmsg = LocateCharMsg(
                locate_character=locate_char,
                id=notification["notification_id"],
                sender_id=notification["sender_id"],
                timestamp=notification["timestamp"],
                solar_system=solar_system,
                constellation=constellation,
                region=region,
                character=character,
            )
            try:
                locatecharmsg.station = EveStation.objects.get_or_create_esi(id=notification_text["targetLocation"][15])[0]
            except KeyError:
                pass
            _bulkcreate.append(locatecharmsg)

    LocateCharMsg.objects.bulk_create(
        _bulkcreate, ignore_conflicts=True, batch_size=500)

    locate_char.cache_expiry = datetime.datetime.strptime(
        str(response.headers['Expires']), '%a, %d %b %Y %H:%M:%S %Z')
    locate_char.save()


@shared_task()
def import_agents_squizz():
    agents_json = requests.get(SQUIZZ_AGT_AGENTS).json()
    _bulkcreate = []
    # {"agentID":3008416,"divisionID":22,"corporationID":1000002,"locationID":60000004,"level":1,"quality":null,"agentTypeID":2,"isLocator":0}
    for agent in agents_json:
        if agent["isLocator"] == 1:
            try:
                agent_character = EveCharacter.objects.get(
                    character_id=agent["agentID"])
            except EveCharacter.DoesNotExist:
                agent_character = EveCharacter.objects.create_character(
                    character_id=agent["agentID"]
                )

            try:
                agent_corporation = EveCorporationInfo.objects.get(
                    corporation_id=agent["corporationID"])
            except EveCorporationInfo.DoesNotExist:
                agent_corporation = EveCorporationInfo.objects.create_corporation(
                    corp_id=agent["corporationID"])

            _bulkcreate.append(
                Agent(
                    character=agent_character,
                    division=agent["divisionID"],
                    corporation=agent_corporation,
                    station=EveStation.objects.get_or_create_esi(id=agent["locationID"])[0],
                    level=agent["level"],
                    type=agent["agentTypeID"],
                    is_locator=agent["isLocator"],
                )
            )
        else:
            # lets skip non locators
            pass

    Agent.objects.bulk_create(
        _bulkcreate, ignore_conflicts=True, batch_size=500)


@shared_task()
def import_notifications_apps():
    if corptools_active() and HUNTING_ENABLE_CORPTOOLS_IMPORT:
        _bulkcreate = []
        from corptools.models import Notification
        for notification in Notification.objects.filter(notification_type="LocateCharMsg"):

            notification_text = parse_notification_text(notification.notification_text.notification_text)
            try:
                character = EveCharacter.objects.get(
                    character_id=notification_text['characterID'])
            except EveCharacter.DoesNotExist:
                character = EveCharacter.objects.create_character(
                    character_id=notification_text['characterID'])[0]

            locatecharmsg = LocateCharMsg(
                locate_character=LocateChar.objects.get_or_create(character=notification.character.character)[0],
                id=notification.notification_id,
                sender_id=notification.sender_id,
                timestamp=notification.timestamp,
                solar_system=EveSolarSystem.objects.get_or_create_esi(id=notification_text["targetLocation"][5])[0],
                constellation=EveConstellation.objects.get_or_create_esi(id=notification_text["targetLocation"][4])[0],
                region=EveRegion.objects.get_or_create_esi(id=notification_text["targetLocation"][3])[0],
                character=character,
            )
            try:
                locatecharmsg.station = EveStation.objects.get_or_create_esi(id=notification_text["targetLocation"][15])[0]
            except KeyError:
                # no station in the LocateCharMsg
                pass
            _bulkcreate.append(locatecharmsg)
            LocateCharMsg.objects.bulk_create(_bulkcreate, ignore_conflicts=True, batch_size=500)
