from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from sister.core import hooks
from sister.auth.models import Person
from sister.auth.admin import PersonAdmin
from sister.admin.admin import ModelAdmin, ModelMenuGroup

from . import models


@admin.register(models.TahunAjaran)
class TahunAjaranAdmin(ModelAdmin):
    pass


@admin.register(models.Sekolah)
class SekolahAdmin(ModelAdmin):
    pass


class MataPelajaranKurikulumInline(admin.TabularInline):
    extra = 1
    model = models.MataPelajaranKurikulum


@admin.register(models.Kurikulum)
class KurikulumAdmin(ModelAdmin):
    inlines = [MataPelajaranKurikulumInline]


@admin.register(models.MataPelajaran)
class MataPelajaranAdmin(ModelAdmin):
    pass


@admin.register(models.MataPelajaranKurikulum)
class MataPelajaranKurikulumAdmin(ModelAdmin):
    pass


@admin.register(models.Tema)
class TemaAdmin(ModelAdmin):
    pass


@admin.register(models.KompetensiInti)
class KompetensiIntiAdmin(ModelAdmin):
    pass


@admin.register(models.KompetensiDasar)
class KompetensiDasarAdmin(ModelAdmin):
    pass


@admin.register(models.EkstraKurikuler)
class EkstraKurikuler(ModelAdmin):
    pass


@admin.register(models.Guru)
class GuruAdmin(ModelAdmin):
    list_display = ['nip', 'full_name']
    list_select_related = ['person']

    def full_name(self, obj):
        return obj.person.full_name


@admin.register(models.Wali)
class WaliAdmin(ModelAdmin):
    list_display = ['full_name']
    list_select_related = ['person']

    def full_name(self, obj):
        return obj.person.full_name


@admin.register(models.Siswa)
class SiswaAdmin(ModelAdmin):
    list_display = ['nis', 'full_name', 'nisn']
    list_select_related = ['person']

    def full_name(self, obj):
        return obj.person.full_name


class MataPelajaranKelasInline(admin.TabularInline):
    extra = 1
    model = models.MataPelajaranKelas


class BobotPenilaianInline(admin.TabularInline):
    model = models.BobotPenilaian


@admin.register(models.MataPelajaranKelas)
class MataPelajaranKelasAdmin(ModelAdmin):
    inlines = [BobotPenilaianInline]
    list_display = ['kelas', 'mata_pelajaran', 'guru']
    

class ItemJadwalPelajaranInline(admin.TabularInline):
    extra = 1
    model = models.ItemJadwalPelajaran


@admin.register(models.JadwalPelajaran)
class JadwalPelajaranAdmin(ModelAdmin):
    inlines = [ItemJadwalPelajaranInline]


class ItemPiketKelasInline(admin.TabularInline):
    extra = 1
    model = models.ItemPiketKelas


@admin.register(models.PiketKelas)
class PiketKelasAdmin(ModelAdmin):
    inlines = [ItemPiketKelasInline]

class SiswaKelasInline(admin.TabularInline):
    extra = 1
    model = models.SiswaKelas


@admin.register(models.Kelas)
class KelasAdmin(ModelAdmin):
    inlines = [MataPelajaranKelasInline, SiswaKelasInline]


@admin.register(models.RentangNilai)
class RentangNilaiAdmin(ModelAdmin):
    list_display = ['kelas', 'nilai_minimum', 'nilai_maximum', 'predikat', 'aksi']


@admin.register(models.SiswaKelas)
class SiswaKelasAdmin(ModelAdmin):
    pass


class ItemPenilaianMataPelajaranInline(admin.TabularInline):
    extra = 1
    model = models.ItemPenilaianMataPelajaran


@admin.register(models.PenilaianMataPelajaran)
class PenilaianMataPelajaranAdmin(ModelAdmin):
    list_display = [
        'siswa_kelas', 
        'mata_pelajaran_kelas',
        'semester',
        'nilai_tugas',
        'nilai_ph',
        'nilai_pts',
        'nilai_pas',
        'nilai_total',
        'predikat'
        ]
    inlines = [ItemPenilaianMataPelajaranInline]


@admin.register(models.PenilaianEkstraKurikuler)
class PenilaianEkstraKurikulerAdmin(ModelAdmin):
    list_display = [
        'siswa_kelas', 
        'ekskul',
        'semester',
        'nilai',
        'predikat']


@admin.register(models.NilaiSiswa)
class NilaiSiswaAdmin(ModelAdmin):
    pass


class ItemPresensiSiswa(admin.TabularInline):
    extra = 1
    model = models.ItemPresensiSiswa


@admin.register(models.PresensiSiswa)
class PresensiSiswaAdmin(ModelAdmin):
    list_filter = ['kelas']
    inlines = [ItemPresensiSiswa]


    def get_inlines(self, request, obj):
        if obj:
            return self.inlines
        return []


class PersonalModelMenuGroup(ModelMenuGroup):
    adminsite = admin.site
    menu_label = _('Personals')
    menu_icon = 'account'
    items = [
        (models.Person, PersonAdmin),
        (models.Siswa, SiswaAdmin),
        (models.Wali, WaliAdmin),
        (models.Guru, GuruAdmin),
        (models.Kelas, PersonAdmin),
    ]


class KelasModelMenuGroup(ModelMenuGroup):
    adminsite = admin.site
    menu_label = _('Classrooms')
    menu_icon = 'teach'
    items = [
        (models.JadwalPelajaran, JadwalPelajaranAdmin),
        (models.RentangNilai, RentangNilaiAdmin),
        (models.PresensiSiswa , PresensiSiswaAdmin),
        (models.PenilaianMataPelajaran , PenilaianMataPelajaranAdmin),
        (models.PenilaianEkstraKurikuler , PenilaianEkstraKurikulerAdmin),
    ]


class KurikulumModelMenuGroup(ModelMenuGroup):
    adminsite = admin.site
    menu_label = _('Curriculum')
    menu_icon = 'book'
    items = [
        (models.Tema, TemaAdmin),
        (models.Sekolah, SekolahAdmin),
        (models.TahunAjaran, TahunAjaranAdmin),
        (models.Kurikulum, KurikulumAdmin),
        (models.MataPelajaran, MataPelajaranAdmin),
        (models.KompetensiInti, KompetensiIntiAdmin),
        (models.KompetensiDasar, KompetensiDasarAdmin),
    ]


@hooks.register('admin_menu_item')
def register_kurikulum_menu(request):
    group = KurikulumModelMenuGroup()
    return group.get_menu_item(request)


@hooks.register('admin_menu_item')
def register_personal_menu(request):
    group = PersonalModelMenuGroup()
    return group.get_menu_item(request)


@hooks.register('admin_menu_item')
def register_kelas_menu(request):
    group = KelasModelMenuGroup()
    return group.get_menu_item(request)