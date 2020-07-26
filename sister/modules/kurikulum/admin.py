from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from sister.core import hooks
from sister.admin.sites import tenant_admin
from sister.admin.admin import ModelAdmin, ModelMenuGroup

from .models import *


class SekolahAdmin(ModelAdmin):
    pass

class TahunAjaranAdmin(ModelAdmin):
    pass

class EkstraKurikulerAdmin(ModelAdmin):
    pass


class MataPelajaranKurikulumInline(admin.TabularInline):
    extra = 1
    model = MataPelajaranKurikulum


class KurikulumAdmin(ModelAdmin):
    inlines = [MataPelajaranKurikulumInline]


class MataPelajaranAdmin(ModelAdmin):
    pass


class KompetensiIntiAdmin(ModelAdmin):
    pass


class KompetensiDasarAdmin(ModelAdmin):
    pass


class TemaAdmin(ModelAdmin):
    pass


tenant_admin.register(Sekolah, SekolahAdmin)
tenant_admin.register(TahunAjaran, TahunAjaranAdmin)
tenant_admin.register(EkstraKurikuler, EkstraKurikulerAdmin)
tenant_admin.register(Kurikulum, KurikulumAdmin)
tenant_admin.register(MataPelajaran, MataPelajaranAdmin)
tenant_admin.register(KompetensiInti, KompetensiIntiAdmin)
tenant_admin.register(KompetensiDasar, KompetensiDasarAdmin)
tenant_admin.register(Tema, TemaAdmin)