import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductChildAdmin, ProductFeeInline, SpecificationInline
from simpellab.modules.sales.admin import SalesOrderChildAdmin, OrderFeeInline, SalesOrderItemInline
from simpellab.modules.sales_training.models import *


class TrainingTopicInline(admin.TabularInline):
    extra = 0
    model = TrainingTopic


@admin.register(TrainingService)
class TrainingServiceAdmin(ProductChildAdmin):
    inlines = [ProductFeeInline, SpecificationInline, TrainingTopicInline]
    

class TrainingOrderItemInline(SalesOrderItemInline):
    model = TrainingOrderItem


@admin.register(TrainingOrder)
class TrainingAdmin(SalesOrderChildAdmin):
    inlines = [OrderFeeInline, TrainingOrderItemInline]
    

@hooks.register('sales_order_child_model')
def register_lat_order():
    return TrainingOrder


@hooks.register('product_child_model')
def register_lat_service():
    return TrainingService