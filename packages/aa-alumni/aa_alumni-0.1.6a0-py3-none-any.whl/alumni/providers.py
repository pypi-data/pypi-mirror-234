from typing import Dict

from allianceauth import __version__ as aa__version__
from allianceauth.services.hooks import get_extension_logger
from esi.clients import EsiClientProvider

from . import __version__ as a__version__

logger = get_extension_logger(__name__)

APP_INFO_TEXT = f"allianceauth v{aa__version__} & aa-alumni v{a__version__}"

"""
Swagger spec operations:
get_corporations_corporation_id_alliancehistory
get_characters_character_id_corporationhistory
"""

esi = EsiClientProvider(app_info_text=APP_INFO_TEXT)


def get_corporations_corporation_id_alliancehistory(corporation_id: int) -> Dict:
    result = esi.client.Corporation.get_corporations_corporation_id_alliancehistory(
        corporation_id=corporation_id
    ).results()
    return result


def get_characters_character_id_corporationhistory(character_id: int) -> Dict:
    result = esi.client.Character.get_characters_character_id_corporationhistory(
        character_id=character_id
    ).results()
    return result
