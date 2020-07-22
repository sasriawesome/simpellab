# from django.contrib import admin
# from django.utils.translation import gettext_lazy as _

# from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
# from admin_numeric_filter.admin import (
#     SingleNumericFilter,
#     RangeNumericFilter,
#     SliderNumericFilter
# )

# from simpellab.admin.menus import admin_menu
# from simpellab.admin.sites import admin_site
# from simpellab.admin.admin import (
#     ModelAdmin, 
#     ModelAdminPDFPrintMixin,
#     ModelMenuGroup
# )
# from .models import Work, Note, JasaLaboratorium, JasaPelatihan

# # Custom Django Admin Filter Examples
# class CustomSliderNumericFilter(SliderNumericFilter):
#     MAX_DECIMALS = 2
#     STEP = 2

# class WorkAdmin(ModelAdminPDFPrintMixin, ModelAdmin):
#     inspect_enabled = True
#     menu_icon = 'briefcase-variant'
#     menu_label = 'Pelanggan'
#     list_per_page = 10
#     list_display = ['title', 'created_at', 'score','is_done']
#     search_fields = ['title']
#     list_filter = [
#         ('created_at', DateRangeFilter),
#         ('score', SingleNumericFilter), # Single field search, __gte lookup
#         ('score', RangeNumericFilter), # Range search, __gte and __lte lookup
#         ('score', SliderNumericFilter), # Same as range above but with slider
#         'is_done',
#     ]


# class NoteAdmin(ModelAdmin):
#     menu_label = 'Permintaan Jasa'
#     menu_icon = 'clipboard-outline'
#     inspect_enabled = True
#     list_per_page = 10
#     list_display = ['title']
#     search_fields = ['title']
#     list_filter = [
#         ('created_at', DateRangeFilter)
#     ]


# class PelatihanAdmin(ModelAdmin):
#     list_display = ['name']

# class LaboratoriumAdmin(ModelAdmin):
#     list_display = ['name']
#     list_select_related = ['produk_ptr', 'jasa_ptr']


# admin.site.register(JasaPelatihan, PelatihanAdmin)
# admin.site.register(JasaLaboratorium, LaboratoriumAdmin)

# admin.site.register(Note, NoteAdmin)
# admin.site.register(Work, WorkAdmin)

# class TodoModelMenuGroup(ModelMenuGroup):
#     adminsite = admin.site
#     menu_icon = 'book'
#     menu_label = 'Pelayanan Jasa Teknis'
#     menu_order = 5
#     items = [ (Note, NoteAdmin), (Work, WorkAdmin) ]

# @admin_menu.register
# def todo_admin_group(request):
#     group = TodoModelMenuGroup()
#     return group.get_menu_item()

from django.contrib import admin
import nested_admin

from .models import Order, OrderItem, OrderItemFee

class OrderItemFeeInline(nested_admin.NestedTabularInline):
    model = OrderItemFee
    extra = 0
    # sortable_field_name = "position"

class OrderItemInline(nested_admin.NestedStackedInline):
    model = OrderItem
    extra = 0
    # sortable_field_name = "position"
    inlines = [OrderItemFeeInline]

class OrderAdmin(nested_admin.NestedModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)