import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductMixin, ProductFeeInline, SpecificationInline
from simpellab.modules.sales.admin import OrderFeeInline
from simpellab.modules.sales_consultancy.models import *


@admin.register(ConsultancyService)
class ConsultancyServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    inlines = [ProductFeeInline, SpecificationInline]


class ConsultancyOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = ConsultancyOrderItem
    readonly_fields = ['unit_price', 'total_price']
    raw_id_fields = ['product']


@admin.register(ConsultancyOrder)
class ConsultancyAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    inlines = [OrderFeeInline, ConsultancyOrderItemInline]
    readonly_fields = ['total_order', 'discount', 'grand_total']
    

@hooks.register('sales_order_child_model')
def register_ksl_order():
    return ConsultancyOrder


@hooks.register('product_child_model')
def register_ksl_order():
    return ConsultancyService