import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductMixin, ProductFeeInline, SpecificationInline
from simpellab.modules.sales.admin import OrderFeeInline
from simpellab.modules.sales_calibration.models import *


@admin.register(CalibrationService)
class CalibrationServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    inlines = [ProductFeeInline, SpecificationInline]
    

class CalibrationOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = CalibrationOrderItem
    readonly_fields = ['unit_price', 'total_price']
    raw_id_fields = ['product']


@admin.register(CalibrationOrder)
class CalibrationOrderAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderFeeInline, CalibrationOrderItemInline]
    readonly_fields = ['total_order', 'discount', 'grand_total']
    

@hooks.register('sales_order_child_model')
def register_kal_order():
    return CalibrationOrder


@hooks.register('product_child_model')
def register_kal_service():
    return CalibrationService