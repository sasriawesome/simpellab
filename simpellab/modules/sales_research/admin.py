import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductChildAdmin, ProductFeeInline, SpecificationInline
from simpellab.modules.sales.admin import SalesOrderChildAdmin, OrderFeeInline, SalesOrderItemInline
from simpellab.modules.sales_research.models import *


@admin.register(ResearchService)
class ResearchServiceAdmin(ProductChildAdmin):
    inlines = [ProductFeeInline, SpecificationInline]


class ResearchOrderItemInline(SalesOrderItemInline):
    model = ResearchOrderItem


@admin.register(ResearchOrder)
class ResearchAdmin(SalesOrderChildAdmin):
    inlines = [OrderFeeInline, ResearchOrderItemInline]
    

@hooks.register('sales_order_child_model')
def register_research_order():
    return ResearchOrder


@hooks.register('product_child_model')
def register_research_product():
    return ResearchService