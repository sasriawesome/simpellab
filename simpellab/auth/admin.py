from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from simpellab.admin.admin import ModelAdmin
from simpellab.auth.models import PersonContact, PersonAddress, Person


@admin.register(get_user_model())
class UserAdmin(UserAdminBase):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'short_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'full_name', 'is_staff')
    search_fields = ('username', 'full_name', 'short_name', 'email')


class ContactInline(admin.StackedInline):
    model = PersonContact


class AddressInline(admin.StackedInline):
    extra = 1
    model = PersonAddress


@admin.register(Person)
class PersonAdmin(ModelAdmin):
    list_display = ['user', 'title', 'date_of_birth']
    list_select_related = ['user']
    inlines = [ContactInline, AddressInline]



