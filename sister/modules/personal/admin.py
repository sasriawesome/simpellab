from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sister.admin.sites import tenant_admin
from sister.admin.admin import ModelAdmin

from .models import *


class ContactInline(admin.StackedInline):
    model = PersonContact


class AddressInline(admin.StackedInline):
    extra = 1
    model = PersonAddress


class PersonAdmin(ModelAdmin):
    list_display = ['full_name', 'gender', 'date_of_birth']
    list_select_related = ['user']
    inlines = [ContactInline, AddressInline]


class GuruAdmin(ModelAdmin):
    list_display = ['nip', 'full_name']
    list_select_related = ['person']

    def full_name(self, obj):
        return obj.person.full_name


class WaliAdmin(ModelAdmin):
    list_display = ['full_name']
    list_select_related = ['person']

    def full_name(self, obj):
        return obj.person.full_name


class SiswaAdmin(ModelAdmin):
    list_display = ['nis', 'full_name', 'nisn']
    list_select_related = ['person']

    def full_name(self, obj):
        return obj.person.full_name


tenant_admin.register(Person, PersonAdmin)
tenant_admin.register(Guru, GuruAdmin)
tenant_admin.register(Wali, WaliAdmin)
tenant_admin.register(Siswa, SiswaAdmin)