from django.contrib import admin
from sister.core import hooks

def get_custom_admin_urls():
    custom_url_hooks = hooks.get_hooks('admin_custom_view')
    custom_urls = [ path() for path in custom_url_hooks]
    return custom_urls

patterns = list(admin.site.get_urls()) + get_custom_admin_urls(), 'admin', admin.site.name