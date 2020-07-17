import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.admin.admin import ModelAdmin
from simpellab.modules.sales.admin import OrderFeeInline
from simpellab.modules.sales_sertification.models import *


class SertificationOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = SertificationOrderItem
    readonly_fields = ['unit_price', 'total_price']
    raw_id_fields = ['product']


@admin.register(SertificationOrder)
class SertificationAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    inlines = [OrderFeeInline, SertificationOrderItemInline]