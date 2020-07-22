import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductChildAdmin, ProductFeeInline
from simpellab.modules.sales.admin import SalesOrderChildAdmin, OrderFeeInline, SalesOrderItemInline
from simpellab.modules.sales_inspection.models import *


@admin.register(InspectionService)
class InspectionServiceAdmin(ProductChildAdmin):
    inlines = [ProductFeeInline]


class InspectionOrderItemParameterInline(nested_admin.NestedTabularInline):
    extra = 0
    min_num = 1
    autocomplete_fields = ['parameter']
    model = InspectionOrderItemParameter
    fields = ['parameter', 'note', 'price', 'date_effective']
    readonly_fields = ['price', 'date_effective']


class InspectionOrderItemInline(SalesOrderItemInline):
    model = InspectionOrderItem
    inlines = [InspectionOrderItemParameterInline]


@admin.register(InspectionOrder)
class InspectionOrderAdmin(SalesOrderChildAdmin):
    inlines = [OrderFeeInline, InspectionOrderItemInline]
    

class InspectionCartParameterInline(admin.TabularInline):
    extra = 0
    min_num = 1
    autocomplete_fields = ['parameter']
    model = InspectionCartParameter


@admin.register(InspectionCart)
class InspectionCartAdmin(PolymorphicChildModelAdmin, ModelAdmin):
    inspect_enabled = False
    inlines = [InspectionCartParameterInline]
    autocomplete_fields = ['product']

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class InspectionBlueprintParameterInline(admin.TabularInline):
    extra = 0
    min_num = 1
    autocomplete_fields = ['parameter']
    model = InspectionBlueprintParameter


@admin.register(InspectionBlueprint)
class InspectionBlueprintAdmin(PolymorphicChildModelAdmin, ModelAdmin):
    inspect_enabled = False
    inlines = [InspectionBlueprintParameterInline]
    autocomplete_fields = ['product']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


@hooks.register('sales_order_child_model')
def register_lit_order():
    return InspectionOrder


@hooks.register('product_child_model')
def register_lit_service():
    return InspectionService


@hooks.register('blueprint_child_model')
def register_lit_blueprint():
    return InspectionBlueprint


@hooks.register('cart_child_model')
def register_lit_cart():
    return InspectionCart