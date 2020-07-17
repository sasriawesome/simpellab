from django.contrib import admin
from django.utils import translation

from simpellab.admin.admin import ModelAdmin
from simpellab.modules.partners.models import (
    Partner,
    PartnerContact,
    PartnerAddress,
    ContactPerson
)

_ = translation.gettext_lazy


class ContactPersonInline(admin.TabularInline):
    extra = 0
    model = ContactPerson
    can_delete = True


class PartnerInline(admin.TabularInline):
    extra = 0
    model = Partner
    can_delete = True


class PartnerContactInline(admin.StackedInline):
    max_num = 1
    extra = 1
    model = PartnerContact


class PartnerAddressInline(admin.StackedInline):
    extra = 1
    max_num = 2
    model = PartnerAddress


@admin.register(Partner)
class PartnerAdmin(ModelAdmin):
    show_in_index = True
    search_fields = ['owner__company__name']
    list_display = ['inner_id', 'name', 'is_customer', 'is_supplier', 'is_active', 'created_at']
    inlines = [PartnerContactInline, PartnerAddressInline, ContactPersonInline]
