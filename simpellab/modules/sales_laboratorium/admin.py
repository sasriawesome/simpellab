import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductMixin, ProductFeeInline
from simpellab.modules.sales_laboratorium.models import *
from simpellab.modules.sales.admin import OrderFeeInline


@admin.register(LaboratoriumService)
class LaboratoriumServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    list_display = ['name']
    inlines = [ProductFeeInline]


class LaboratoriumOrderItemParameterInline(nested_admin.NestedTabularInline):
    extra = 0
    min_num = 1
    model = LaboratoriumOrderItemParameter
    fields = ['parameter', 'note', 'price', 'date_effective']
    autocomplete_fields = ['parameter']
    readonly_fields = ['price', 'date_effective']


class LaboratoriumOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = LaboratoriumOrderItem
    inlines = [LaboratoriumOrderItemParameterInline]
    readonly_fields = ['unit_price', 'total_price']
    autocomplete_fields = ['product']


@admin.register(LaboratoriumOrder)
class LaboratoriumOrderAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    inlines = [OrderFeeInline, LaboratoriumOrderItemInline]
    autocomplete_fields = ['customer']
    readonly_fields = ['total_order', 'discount', 'grand_total']


class LaboratoriumBlueprintParameterInline(admin.TabularInline):
    extra = 0
    min_num = 1
    autocomplete_fields = ['parameter']
    model = LaboratoriumBlueprintParameter


@admin.register(LaboratoriumBlueprint)
class LaboratoriumBlueprintAdmin(PolymorphicChildModelAdmin, ModelAdmin):
    inlines = [LaboratoriumBlueprintParameterInline]
    autocomplete_fields = ['product']


@hooks.register('sales_order_child_model')
def register_lab_order():
    return LaboratoriumOrder


@hooks.register('product_child_model')
def register_lab_service():
    return LaboratoriumService


@hooks.register('blueprint_child_model')
def register_lab_service():
    return LaboratoriumBlueprint