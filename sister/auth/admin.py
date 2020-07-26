from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from sister.admin.admin import ModelAdmin
from sister.auth.models import PersonContact, PersonAddress, Person

from tenant_users.permissions.models import UserTenantPermissions


@admin.register(get_user_model())
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(UserTenantPermissions)
class UserTenantPermissionsAdmin(admin.ModelAdmin):
    pass


# @admin.register(get_user_model())
# class UserAdmin(UserAdminBase):
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         (_('Permissions'), {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('username', 'email', 'is_staff')
#     search_fields = ('username', 'email')


class ContactInline(admin.StackedInline):
    model = PersonContact


class AddressInline(admin.StackedInline):
    extra = 1
    model = PersonAddress


@admin.register(Person)
class PersonAdmin(ModelAdmin):
    list_display = ['full_name', 'gender', 'date_of_birth']
    list_select_related = ['user']
    inlines = [ContactInline, AddressInline]
