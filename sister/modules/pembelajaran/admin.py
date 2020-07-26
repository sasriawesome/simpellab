from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from sister.core import hooks
from sister.admin.sites import tenant_admin
from sister.admin.admin import ModelAdmin, ModelMenuGroup
from sister.modules.penilaian.models import BobotPenilaian

from .models import *


class MataPelajaranKelasInline(admin.TabularInline):
    extra = 1
    model = MataPelajaranKelas


class BobotPenilaianInline(admin.TabularInline):
    model = BobotPenilaian


class MataPelajaranKelasAdmin(ModelAdmin):
    inlines = [BobotPenilaianInline]
    list_display = ['kelas', 'mata_pelajaran', 'guru']



class ItemJadwalPelajaranInline(admin.TabularInline):
    extra = 1
    model = ItemJadwalPelajaran


class ItemJadwalEkstraKurikulerInline(admin.TabularInline):
    extra = 1
    model = ItemJadwalEkstraKurikuler


class JadwalKelasAdmin(ModelAdmin):
    inlines = [
        ItemJadwalPelajaranInline,
        ItemJadwalEkstraKurikulerInline
        ]


class ItemPiketKelasInline(admin.TabularInline):
    extra = 1
    model = ItemPiketKelas


class PiketKelasAdmin(ModelAdmin):
    inlines = [ItemPiketKelasInline]


class SiswaKelasInline(admin.TabularInline):
    extra = 1
    model = SiswaKelas


class KelasAdmin(ModelAdmin):
    inlines = [MataPelajaranKelasInline, SiswaKelasInline]


class RentangNilaiAdmin(ModelAdmin):
    list_display = ['kelas', 'nilai_minimum', 'nilai_maximum', 'predikat', 'aksi']


class SiswaKelasAdmin(ModelAdmin):
    pass


class ItemPresensiSiswa(admin.TabularInline):
    extra = 1
    model = ItemPresensiSiswa


class PresensiSiswaAdmin(ModelAdmin):
    list_filter = ['kelas']
    inlines = [ItemPresensiSiswa]


    def get_inlines(self, request, obj):
        if obj:
            return self.inlines
        return []


tenant_admin.register(MataPelajaranKelas, MataPelajaranKelasAdmin)
tenant_admin.register(JadwalKelas, JadwalKelasAdmin)
tenant_admin.register(PiketKelas, PiketKelasAdmin)
tenant_admin.register(Kelas, KelasAdmin)
tenant_admin.register(RentangNilai, RentangNilaiAdmin)
tenant_admin.register(SiswaKelas, SiswaKelasAdmin)
tenant_admin.register(PresensiSiswa, PresensiSiswaAdmin)


# class PersonalModelMenuGroup(ModelMenuGroup):
#     adminsite = admin.site
#     menu_label = _('Personals')
#     menu_icon = 'account'
#     items = [
#         (Person, PersonAdmin),
#         (Siswa, SiswaAdmin),
#         (Wali, WaliAdmin),
#         (Guru, GuruAdmin),
#         (Kelas, PersonAdmin),
#     ]


# class KelasModelMenuGroup(ModelMenuGroup):
#     adminsite = admin.site
#     menu_label = _('Classrooms')
#     menu_icon = 'teach'
#     items = [
#         (JadwalPelajaran, JadwalPelajaranAdmin),
#         (RentangNilai, RentangNilaiAdmin),
#         (PresensiSiswa , PresensiSiswaAdmin),
#         (PenilaianMataPelajaran , PenilaianMataPelajaranAdmin),
#         (PenilaianEkstraKurikuler , PenilaianEkstraKurikulerAdmin),
#     ]


# class KurikulumModelMenuGroup(ModelMenuGroup):
#     adminsite = admin.site
#     menu_label = _('Curriculum')
#     menu_icon = 'book'
#     items = [
#         (Tema, TemaAdmin),
#         (Sekolah, SekolahAdmin),
#         (TahunAjaran, TahunAjaranAdmin),
#         (Kurikulum, KurikulumAdmin),
#         (MataPelajaran, MataPelajaranAdmin),
#         (KompetensiInti, KompetensiIntiAdmin),
#         (KompetensiDasar, KompetensiDasarAdmin),
#     ]


# @hooks.register('admin_menu_item')
# def register_kurikulum_menu(request):
#     group = KurikulumModelMenuGroup()
#     return group.get_menu_item(request)


# @hooks.register('admin_menu_item')
# def register_personal_menu(request):
#     group = PersonalModelMenuGroup()
#     return group.get_menu_item(request)


# @hooks.register('admin_menu_item')
# def register_kelas_menu(request):
#     group = KelasModelMenuGroup()
#     return group.get_menu_item(request)