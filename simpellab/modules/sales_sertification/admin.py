import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductMixin, ProductFeeInline, SpecificationInline
from simpellab.modules.sales.admin import OrderFeeInline
from simpellab.modules.sales_sertification.models import *


@admin.register(SertificationService)
class SertificationServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    list_display = []
    inlines = [ProductFeeInline, SpecificationInline]

    
class SertificationOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = SertificationOrderItem
    readonly_fields = ['unit_price', 'total_price']
    raw_id_fields = ['product']


@admin.register(SertificationOrder)
class SertificationAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderFeeInline, SertificationOrderItemInline]
    readonly_fields = ['total_order', 'discount', 'grand_total']
    

@hooks.register('sales_order_child_model')
def register_pro_order():
    return SertificationOrder


@hooks.register('product_child_model')
def register_pro_service():
    return SertificationService