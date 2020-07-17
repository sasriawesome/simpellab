import nested_admin
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from simpellab.admin.admin import ModelAdmin
from simpellab.modules.sales_laboratorium.models import *
from simpellab.modules.sales.admin import OrderFeeInline

class LaboratoriumOrderItemExtraParameterInline(nested_admin.NestedTabularInline):
    extra = 0
    model = LaboratoriumOrderItemExtraParameter
    raw_id_fields = ['parameter']
    readonly_fields = ['price', 'date_effective']


class LaboratoriumOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    model = LaboratoriumOrderItem
    inlines = [LaboratoriumOrderItemExtraParameterInline]
    readonly_fields = ['unit_price', 'total_price']
    raw_id_fields = ['product']


@admin.register(LaboratoriumOrder)
class LaboratoriumOrderAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    inlines = [OrderFeeInline, LaboratoriumOrderItemInline]