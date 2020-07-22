import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductChildAdmin, ProductFeeInline, SpecificationInline
from simpellab.modules.sales.admin import SalesOrderChildAdmin, OrderFeeInline, SalesOrderItemInline
from simpellab.modules.sales_misc.models import *


@admin.register(MiscService)
class MiscServiceAdmin(ProductChildAdmin):
    inlines = [ProductFeeInline, SpecificationInline]


class MiscOrderItemInline(SalesOrderItemInline):
    model = MiscOrderItem


@admin.register(MiscOrder)
class MiscAdmin(SalesOrderChildAdmin):
    inlines = [OrderFeeInline, MiscOrderItemInline]


@hooks.register('sales_order_child_model')
def register_lny_order():
    return MiscOrder


@hooks.register('product_child_model')
def register_lny_service():
    return MiscService