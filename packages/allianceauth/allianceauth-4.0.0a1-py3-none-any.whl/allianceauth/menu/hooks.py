from django.template.loader import render_to_string


from typing import List, Optional


class MenuItemHook:
    """
    Auth Hook for generating Side Menu Items
    """
    def __init__(self, text: str, classes: List[str], url_name: str, order: Optional[int] = None, navactive: List = list([])):
        """
        :param text: The text shown as menu item, e.g. usually the name of the app.
        :type text: str
        :param classes: The classes that should be applied to the menu item icon
        :type classes: List[str]
        :param url_name: The name of the Django URL to use
        :type url_name: str
        :param order: An integer which specifies the order of the menu item, lowest to highest. Community apps are free to use any order above `1000`. Numbers below are served for Auth.
        :type order: Optional[int], optional
        :param navactive: A list of views or namespaces the link should be highlighted on. See [django-navhelper](https://github.com/geelweb/django-navhelper#navactive) for usage. Defaults to the supplied `url_name`.
        :type navactive: List, optional
        """

        self.text = text
        self.classes = classes
        self.url_name = url_name
        self.template = 'public/menuitem.html'
        self.order = order if order is not None else 9999

        # count is an integer shown next to the menu item as badge when count != None
        # apps need to set the count in their child class, e.g. in render() method
        self.count = None

        navactive = navactive or []
        navactive.append(url_name)
        self.navactive = navactive

    def render(self, request):
        return render_to_string(self.template,
                                {'item': self},
                                request=request)
