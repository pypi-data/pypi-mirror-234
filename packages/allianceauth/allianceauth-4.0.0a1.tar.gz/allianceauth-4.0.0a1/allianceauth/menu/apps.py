import logging

from django.apps import AppConfig
from django.db.utils import ProgrammingError, OperationalError

logger = logging.getLogger(__name__)


class MenuConfig(AppConfig):
    name = "allianceauth.menu"
    label = "menu"

    def ready(self):
        try:
            logger.debug("Syncing MenuItem Hooks")
            from allianceauth.menu.providers import MenuItem
            MenuItem.sync_hook_models()
        except (ProgrammingError, OperationalError):
            logger.warning("Migrations not completed for MenuItems")
