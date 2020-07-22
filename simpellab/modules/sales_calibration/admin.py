import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductChildAdmin, ProductFeeInline, SpecificationInline
from simpellab.modules.sales.admin import SalesOrderChildAdmin, OrderFeeInline, SalesOrderItemInline
from simpellab.modules.sales_calibration.models import *


@admin.register(CalibrationService)
class CalibrationServiceAdmin(ProductChildAdmin):
    inlines = [ProductFeeInline, SpecificationInline]
    

class CalibrationOrderItemInline(SalesOrderItemInline):
    model = CalibrationOrderItem


@admin.register(CalibrationOrder)
class CalibrationOrderAdmin(SalesOrderChildAdmin):
    inlines = [OrderFeeInline, CalibrationOrderItemInline]
    

@hooks.register('sales_order_child_model')
def register_kal_order():
    return CalibrationOrder


@hooks.register('product_child_model')
def register_kal_service():
    return CalibrationService