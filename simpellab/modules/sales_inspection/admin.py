import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.admin.admin import ModelAdmin
from simpellab.modules.sales.admin import OrderFeeInline
from simpellab.modules.sales_inspection.models import *


class InspectionOrderItemExtraParameterInline(nested_admin.NestedTabularInline):
    extra = 0
    model = InspectionOrderItemExtraParameter
    raw_id_fields = ['parameter']
    readonly_fields = ['price', 'date_effective']


class InspectionOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = InspectionOrderItem
    inlines = [InspectionOrderItemExtraParameterInline]
    readonly_fields = ['unit_price', 'total_price']
    raw_id_fields = ['product']


@admin.register(InspectionOrder)
class InspectionOrderAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    inlines = [OrderFeeInline, InspectionOrderItemInline]