from django.contrib import admin

from . import models


@admin.register(models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['text', 'hide', 'parent', 'url', 'icon_classes', 'rank']
    ordering = ('rank',)
