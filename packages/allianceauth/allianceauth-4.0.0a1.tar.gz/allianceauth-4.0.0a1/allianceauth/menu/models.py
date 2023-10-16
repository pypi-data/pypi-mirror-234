import logging
from allianceauth.hooks import get_hooks

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class MenuItem(models.Model):
    # Auto Generated model from an auth_hook
    hook_function = models.CharField(
        max_length=500, default=None, null=True, blank=True)

    # User Made Model
    icon_classes = models.CharField(
        max_length=150, default=None, null=True, blank=True, help_text="Font Awesome classes to show as icon on menu")
    text = models.CharField(
        max_length=150, default=None, null=True, blank=True, help_text="Text to show on menu")
    url = models.CharField(max_length=2048, default=None,
                            null=True, blank=True)

    # Put it under a header?
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, help_text="Parent Header. (Optional)")

    # Put it where? lowest first
    rank = models.IntegerField(default=1000, help_text="Order of the menu. Lowest First.")

    # Hide it fully? Hiding a parent will hide all it's children
    hide = models.BooleanField(default=False, help_text="Hide this menu item. If this item is a header all items under it will be hidden too.")

    class Meta:
        indexes = [
            models.Index(fields=['rank', ]),
        ]

    def __str__(self) -> str:
        return self.text

    @property
    def classes(self):  # Helper function to make this model closer to the hook functions
        return self.icon_classes

    @staticmethod
    def hook_to_name(mh):
        return f"{mh.__class__.__module__}.{mh.__class__.__name__}"

    @staticmethod
    def sync_hook_models():
        # TODO define aa way for hooks to predefine a "parent" to create a sub menu from modules
        menu_hooks = get_hooks('menu_item_hook')
        hook_functions = []
        for hook in menu_hooks:
            mh = hook()
            cls = MenuItem.hook_to_name(mh)
            try:
                # if it exists update the text only
                # Users can adjust ranks so lets not change it if they have.
                mi = MenuItem.objects.get(hook_function=cls)
                mi.text = getattr(mh, "text", mh.__class__.__name__)
                mi.save()
            except MenuItem.DoesNotExist:
                # This is a new hook, Make the database model.
                MenuItem.objects.create(
                    hook_function=cls,
                    rank=getattr(mh, "order", 500),
                    text=getattr(mh, "text", mh.__class__.__name__)
                )
            hook_functions.append(cls)

        # Get rid of any legacy hooks from modules removed
        MenuItem.objects.filter(hook_function__isnull=False).exclude(
            hook_function__in=hook_functions).delete()

    @classmethod
    def filter_items(cls, menu_item: dict):
        """
        filter any items with no valid children from a menu
        """
        count_items = len(menu_item['items'])
        if count_items:  # if we have children confirm we can see them
            for i in menu_item['items']:
                if len(i['render']) == 0:
                    count_items -= 1
            if count_items == 0:  # no children left dont render header
                return False
            return True
        else:
            return True

    @classmethod
    def render_menu(cls, request):
        """
        Return the sorted side menu items with any items the user can't see removed.
        """
        # Override all the items to the bs5 theme
        template = "menu/menu-item-bs5.html"
        # TODO discuss permissions for user defined links

        # Turn all the hooks into functions
        menu_hooks = get_hooks('menu_item_hook')
        items = {}
        for fn in menu_hooks:
            f = fn()
            items[cls.hook_to_name(f)] = f

        menu_items = MenuItem.objects.all().order_by("rank")

        menu = {}
        for mi in menu_items:
            if mi.hide:
                # hidden item, skip it completely
                continue
            try:
                _cnt = 0
                _render = None
                if mi.hook_function:
                    # This is a module hook, so we need to render it as the developer intended
                    # TODO add a new attribute for apps that want to override it in the new theme
                    items[mi.hook_function].template = template
                    _render = items[mi.hook_function].render(request)
                    _cnt = items[mi.hook_function].count
                else:
                    # This is a user defined menu item so we render it with defaults.
                    _render = render_to_string(template,
                                                {'item': mi},
                                                request=request)

                parent = mi.id
                if mi.parent_id:  # Set it if present
                    parent = mi.parent_id

                if parent not in menu:  # this will cause the menu headers to be out of order
                    menu[parent] = {"items": [],
                                    "count": 0,
                                    "render": None,
                                    "text": "None",
                                    "rank": 9999,
                                    }
                _mi = {
                    "count": _cnt,
                    "render": _render,
                    "text": mi.text,
                    "rank": mi.rank,
                    "classes": (mi.icon_classes if mi.icon_classes != "" else "fas fa-folder"),
                    "hide": mi.hide
                }

                if parent != mi.id:
                    # this is a sub item
                    menu[parent]["items"].append(_mi)
                    if _cnt:
                        #add its count to the header count
                        menu[parent]["count"] += _cnt
                else:
                    if len(menu[parent]["items"]):
                        # this is a top folder dont update the count.
                        del(_mi["count"])
                    menu[parent].update(_mi)
            except Exception as e:
                logger.exception(e)

        # reset to list
        menu = list(menu.values())

        # sort the menu list as the parents may be out of order.
        menu.sort(key=lambda i: i['rank'])

        # ensure no empty groups
        menu = filter(cls.filter_items, menu)

        return menu
