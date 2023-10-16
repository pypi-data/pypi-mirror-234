from django.template.loader import render_to_string

from allianceauth.hooks import get_hooks

from .models import MenuItem


class MenuProvider():
    def __init__(self) -> None:
        pass
