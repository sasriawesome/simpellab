import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductMixin, ProductFeeInline
from simpellab.modules.sales.admin import OrderFeeInline
from simpellab.modules.sales_inspection.models import *


class InspectionServiceParameterInline(admin.TabularInline):
    extra = 0
    model = InspectionServiceParameter
    raw_id_fields = ['parameter']
    readonly_fields = ['price', 'date_effective']


@admin.register(InspectionService)
class InspectionServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    inlines = [ProductFeeInline, InspectionServiceParameterInline]


class InspectionOrderItemExtraParameterInline(nested_admin.NestedTabularInline):
    extra = 0
    model = InspectionOrderItemExtraParameter
    raw_id_fields = ['parameter']
    readonly_fields = ['price', 'date_effective']


class InspectionOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = InspectionOrderItem
    inlines = [InspectionOrderItemExtraParameterInline]
    readonly_fields = ['unit_price', 'total_price']
    raw_id_fields = ['product']


@admin.register(InspectionOrder)
class InspectionOrderAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    inlines = [OrderFeeInline, InspectionOrderItemInline]


@hooks.register('sales_order_child_model')
def register_lab_order():
    return InspectionOrder


@hooks.register('product_child_model')
def register_lit_service():
    return InspectionService