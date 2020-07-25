from django.contrib import admin
from django.utils.html import format_html

from sister.admin.admin import ModelAdmin
from sister.core import hooks

from .models import ShortUrl


@admin.register(ShortUrl)
class ShortUrlAdmin(ModelAdmin):
    menu_icon = 'link'
    list_display = ['name', 'hashed_url', 'clicked', 'view_url']   

    def view_url(self, obj):
        return format_html("<a href='%s' target='_blank'>View</a>" % obj.get_absolute_url() )


@hooks.register('admin_menu_item')
def register_shorturls_menu(request):
    modeladmin = ShortUrlAdmin(ShortUrl, admin.site)
    return modeladmin.get_menu_item(request)