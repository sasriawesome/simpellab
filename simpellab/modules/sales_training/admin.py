import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductMixin, ProductFeeInline, SpecificationInline
from simpellab.modules.sales.admin import OrderFeeInline
from simpellab.modules.sales_training.models import *


class TrainingTopicInline(admin.TabularInline):
    extra = 0
    model = TrainingTopic


@admin.register(TrainingService)
class TrainingServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    inlines = [ProductFeeInline, SpecificationInline, TrainingTopicInline]
    

class TrainingOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = TrainingOrderItem
    readonly_fields = ['unit_price', 'total_price']
    raw_id_fields = ['product']


@admin.register(TrainingOrder)
class TrainingAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    inlines = [OrderFeeInline, TrainingOrderItemInline]


@hooks.register('sales_order_child_model')
def register_lat_order():
    return TrainingOrder


@hooks.register('product_child_model')
def register_lat_service():
    return TrainingService