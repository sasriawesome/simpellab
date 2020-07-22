import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductChildAdmin, ProductFeeInline, SpecificationInline
from simpellab.modules.sales.admin import OrderFeeInline
from simpellab.modules.sales_research.models import *


@admin.register(ResearchService)
class ResearchServiceAdmin(ProductChildAdmin):
    inlines = [ProductFeeInline, SpecificationInline]


class ResearchOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = ResearchOrderItem
    readonly_fields = ['unit_price', 'total_price']
    raw_id_fields = ['product']


@admin.register(ResearchOrder)
class ResearchAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderFeeInline, ResearchOrderItemInline]
    readonly_fields = ['total_order', 'discount', 'grand_total']
    

@hooks.register('sales_order_child_model')
def register_research_order():
    return ResearchOrder


@hooks.register('product_child_model')
def register_research_product():
    return ResearchService