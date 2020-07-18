import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductMixin, ProductFeeInline, SpecificationInline
from simpellab.modules.sales.admin import OrderFeeInline
from simpellab.modules.sales_misc.models import *


@admin.register(MiscService)
class MiscServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    inlines = [ProductFeeInline, SpecificationInline]


class MiscOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = MiscOrderItem
    readonly_fields = ['unit_price', 'total_price']
    raw_id_fields = ['product']


@admin.register(MiscOrder)
class MiscAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    inlines = [OrderFeeInline, MiscOrderItemInline]


@hooks.register('sales_order_child_model')
def register_lny_order():
    return MiscOrder


@hooks.register('product_child_model')
def register_lny_service():
    return MiscService