import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductChildAdmin, ProductFeeInline, SpecificationInline
from simpellab.modules.sales.admin import SalesOrderChildAdmin, OrderFeeInline, SalesOrderItemInline
from simpellab.modules.sales_consultancy.models import *


@admin.register(ConsultancyService)
class ConsultancyServiceAdmin(ProductChildAdmin):
    inlines = [ProductFeeInline, SpecificationInline]


class ConsultancyOrderItemInline(SalesOrderItemInline):
    model = ConsultancyOrderItem


@admin.register(ConsultancyOrder)
class ConsultancyOrderAdmin(SalesOrderChildAdmin):
    inlines = [OrderFeeInline, ConsultancyOrderItemInline]
    

@hooks.register('sales_order_child_model')
def register_ksl_order():
    return ConsultancyOrder


@hooks.register('product_child_model')
def register_ksl_order():
    return ConsultancyService