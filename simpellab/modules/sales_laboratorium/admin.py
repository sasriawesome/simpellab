import nested_admin
from django.urls import path
from django.utils.html import format_html
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductChildAdmin, ProductFeeInline
from simpellab.modules.sales_laboratorium.models import *
from simpellab.modules.sales.admin import SalesOrderChildAdmin, OrderFeeInline, SalesOrderItemInline


@admin.register(LaboratoriumService)
class LaboratoriumServiceAdmin(ProductChildAdmin):
    list_display = ['name']
    inlines = [ProductFeeInline]


class LaboratoriumOrderItemParameterInline(nested_admin.NestedTabularInline):
    extra = 0
    min_num = 1
    model = LaboratoriumOrderItemParameter
    fields = ['parameter', 'note', 'price', 'date_effective']
    autocomplete_fields = ['parameter']
    readonly_fields = ['price', 'date_effective']


class LaboratoriumOrderItemInline(SalesOrderItemInline):
    model = LaboratoriumOrderItem
    inlines = [LaboratoriumOrderItemParameterInline]


@admin.register(LaboratoriumOrder)
class LaboratoriumOrderAdmin(SalesOrderChildAdmin):
    inlines = [OrderFeeInline, LaboratoriumOrderItemInline]


class LaboratoriumCartParameterInline(admin.TabularInline):
    extra = 0
    min_num = 1
    autocomplete_fields = ['parameter']
    model = LaboratoriumCartParameter


@admin.register(LaboratoriumCart)
class LaboratoriumCartAdmin(PolymorphicChildModelAdmin, ModelAdmin):
    inspect_enabled = False
    inlines = [LaboratoriumCartParameterInline]
    autocomplete_fields = ['product']

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class LaboratoriumBlueprintParameterInline(admin.TabularInline):
    extra = 0
    min_num = 1
    autocomplete_fields = ['parameter']
    model = LaboratoriumBlueprintParameter


@admin.register(LaboratoriumBlueprint)
class LaboratoriumBlueprintAdmin(PolymorphicChildModelAdmin, ModelAdmin):
    inspect_enabled = False
    inlines = [LaboratoriumBlueprintParameterInline]
    autocomplete_fields = ['product']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


@hooks.register('sales_order_child_model')
def register_lab_order():
    return LaboratoriumOrder


@hooks.register('product_child_model')
def register_lab_service():
    return LaboratoriumService


@hooks.register('blueprint_child_model')
def register_lab_service():
    return LaboratoriumBlueprint


@hooks.register('cart_child_model')
def register_lab_service():
    return LaboratoriumCart