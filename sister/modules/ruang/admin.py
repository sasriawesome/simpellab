from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from sister.core import hooks
from sister.admin.sites import tenant_admin
from sister.admin.admin import ModelAdmin, ModelMenuGroup
from sister.modules.ruang.models import Ruang


class RuangAdmin(ModelAdmin):
    list_display = ['kode', 'nama', 'kapasitas']

tenant_admin.register(Ruang, RuangAdmin)