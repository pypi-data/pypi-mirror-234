from django import template

from allianceauth.hooks import get_hooks
from allianceauth.menu.models import MenuItem

from ..providers import MenuProvider

register = template.Library()


def process_menu_items(hooks, request):
    _menu_items = list()
    items = [fn() for fn in hooks]
    items.sort(key=lambda i: i.order)
    for item in items:
        _menu_items.append(item.render(request))
    return _menu_items


@register.inclusion_tag('public/menublock.html', takes_context=True)
def menu_items(context):
    request = context['request']

    return {
        'menu_items': process_menu_items(get_hooks('menu_item_hook'), request),
    }


@register.inclusion_tag('menu/menu-block.html', takes_context=True)
def sorted_menu_items(context):
    request = context['request']
    manu_items = MenuItem.render_menu(request)
    return {
        'menu_items':manu_items
    }
