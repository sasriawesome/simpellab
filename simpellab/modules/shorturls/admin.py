from django.contrib import admin
from django.utils.html import format_html
from .models import ShortUrl

@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ['name', 'hashed_url', 'clicked', 'view_url']   

    def view_url(self, obj):
        return format_html("<a href='%s' target='_blank'>View</a>" % obj.get_absolute_url() )