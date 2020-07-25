from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from sister.core import hooks
from sister.admin.admin import ModelAdmin, ModelMenuGroup
from sister.modules.ruang.models import Ruang


@admin.register(Ruang)
class RuangAdmin(ModelAdmin):
    list_display = ['kode', 'nama', 'kapasitas']