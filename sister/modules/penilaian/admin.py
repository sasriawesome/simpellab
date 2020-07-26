from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from sister.core import hooks
from sister.admin.sites import tenant_admin
from sister.admin.admin import ModelAdmin, ModelMenuGroup

from .models import *


class ItemPenilaianTugasInline(admin.TabularInline):
    extra=0
    model = ItemPenilaianTugas


class ItemPenilaianHarianInline(admin.TabularInline):
    extra=0
    model = ItemPenilaianHarian


class ItemPenilaianTengahSemesterInline(admin.TabularInline):
    extra=0
    model = ItemPenilaianTengahSemester


class ItemPenilaianAkhirSemesterInline(admin.TabularInline):
    extra=0
    model = ItemPenilaianAkhirSemester


class PenilaianPembelajaranAdmin(ModelAdmin):
    fields = ['siswa', 'mata_pelajaran', 'semester', 'nilai']
    readonly_fields = ['nilai']
    list_display = [
        'siswa', 
        'mata_pelajaran',
        'semester',
        # 'nilai_tugas',
        # 'nilai_ph',
        # 'nilai_pts',
        # 'nilai_pas',
        'nilai',
        # 'predikat'
        ]
    inlines = [
        ItemPenilaianTugasInline,
        ItemPenilaianHarianInline,
        ItemPenilaianTengahSemesterInline,
        ItemPenilaianAkhirSemesterInline
        ]


class PenilaianEkstraKurikulerAdmin(ModelAdmin):
    fields = ['siswa', 'ekskul', 'semester', 'nilai']
    list_display = [
        'siswa', 
        'ekskul',
        'semester',
        'nilai',
        # 'predikat'
        ]



tenant_admin.register(PenilaianPembelajaran, PenilaianPembelajaranAdmin)
tenant_admin.register(PenilaianEkstraKurikuler, PenilaianEkstraKurikulerAdmin)