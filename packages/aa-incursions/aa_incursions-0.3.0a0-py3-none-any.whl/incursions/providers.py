from allianceauth import __version__ as aa__version__
from allianceauth.services.hooks import get_extension_logger
from esi.clients import EsiClientProvider

from . import __version__ as i__version__

logger = get_extension_logger(__name__)

APP_INFO_TEXT = f"allianceauth v{aa__version__} & aa-incursions v{i__version__}"

"""
Swagger spec operations:
get_incursions
"""

esi = EsiClientProvider(app_info_text=APP_INFO_TEXT)


def get_incursions_incursions():
    operation = esi.client.Incursions.get_incursions()
    operation.request_config.also_return_response = True
    incursions, response = operation.results()
    return incursions, response
