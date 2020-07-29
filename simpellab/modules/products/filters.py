from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType


class ProductChildFilter(admin.SimpleListFilter):
    title = _('Product by Type')
    parameter_name = 'ctype'

    def lookups(self, request, model_admin):
        models = model_admin.get_child_models()
        child_ctypes = ContentType.objects.get_for_models(*models)
        lookup = [(str(val.id), str(val.name)) for val in child_ctypes.values()]
        return lookup

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        return queryset.filter(polymorphic_ctype=self.value())
