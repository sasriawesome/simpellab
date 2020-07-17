import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.admin.admin import ModelAdmin
from simpellab.modules.sales.admin import OrderFeeInline
from simpellab.modules.sales_consultancy.models import *


class ConsultancyOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = ConsultancyOrderItem
    readonly_fields = ['unit_price', 'total_price']
    raw_id_fields = ['product']


@admin.register(ConsultancyOrder)
class ConsultancyAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    inlines = [OrderFeeInline, ConsultancyOrderItemInline]