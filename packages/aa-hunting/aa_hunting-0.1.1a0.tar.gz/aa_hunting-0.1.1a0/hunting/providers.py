from allianceauth import __version__ as aa__version__
from allianceauth.services.hooks import get_extension_logger
from esi.clients import EsiClientProvider
from esi.models import Token

from . import __version__ as h__version__

logger = get_extension_logger(__name__)

APP_INFO_TEXT = f"allianceauth v{aa__version__} & aa-hunting v{h__version__}"

"""
Swagger spec operations:
get_characters_character_id_notifications
"""

esi = EsiClientProvider(app_info_text=APP_INFO_TEXT)


def get_characters_character_id_notifications(character_id: int, token: Token):
    operation = esi.client.Character.get_characters_character_id_notifications(
        character_id=character_id, token=token.valid_access_token())
    operation.request_config.also_return_response = True
    notifications, response = operation.results()
    return notifications, response
