import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.admin.admin import ModelAdmin
from simpellab.modules.sales.admin import OrderFeeInline
from simpellab.modules.sales_training.models import *


class TrainingOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = TrainingOrderItem
    readonly_fields = ['unit_price', 'total_price']
    raw_id_fields = ['product']


@admin.register(TrainingOrder)
class TrainingAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    inlines = [OrderFeeInline, TrainingOrderItemInline]