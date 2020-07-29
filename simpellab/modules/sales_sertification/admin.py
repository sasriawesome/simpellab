import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductChildAdmin, ProductFeeInline, SpecificationInline
from simpellab.modules.sales.admin import SalesOrderChildAdmin, OrderFeeInline, SalesOrderItemInline
from simpellab.modules.sales_sertification.models import *


@admin.register(SertificationService)
class SertificationServiceAdmin(ProductChildAdmin):
    list_display = []
    inlines = [ProductFeeInline, SpecificationInline]

    
class SertificationOrderItemInline(SalesOrderItemInline):
    model = SertificationOrderItem


@admin.register(SertificationOrder)
class SertificationAdmin(SalesOrderChildAdmin):
    inlines = [OrderFeeInline, SertificationOrderItemInline]
    

@hooks.register('sales_order_child_model')
def register_pro_order():
    return SertificationOrder


@hooks.register('product_child_model')
def register_pro_service():
    return SertificationService