import nested_admin
from django.contrib import admin
from django.utils import translation

from rangefilter.filter import DateRangeFilter
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from admin_numeric_filter.admin import RangeNumericFilter

from simpellab.admin.admin import ModelAdmin
from simpellab.modules.sales.forms import OrderProductFormset
from simpellab.modules.sales.models import (
    # SalesQuotationTemplate,
    # SalesQuotation, QuotationExtraFee, QuotationProduct,
    SalesOrder, OrderFee,
)

# Todo: Register this model with hooks
from simpellab.modules.sales_laboratorium.models import LaboratoriumOrder
from simpellab.modules.sales_inspection.models import InspectionOrder
from simpellab.modules.sales_calibration.models import CalibrationOrder
from simpellab.modules.sales_consultancy.models import ConsultancyOrder
from simpellab.modules.sales_research.models import ResearchOrder
from simpellab.modules.sales_training.models import TrainingOrder
from simpellab.modules.sales_sertification.models import SertificationOrder


_ = translation.ugettext_lazy


class OrderFeeInline(nested_admin.NestedTabularInline):
    extra = 0
    min_num = 1
    model = OrderFee
    raw_id_fields = ['fee']
    readonly_fields = ['amount', 'total_fee']


@admin.register(SalesOrder)
class OrderAdmin(PolymorphicParentModelAdmin, ModelAdmin):
    list_display = [
        'customer', 'created_at'
    ]
    child_models = [
        LaboratoriumOrder,
        InspectionOrder,
        SertificationOrder,
        CalibrationOrder,
        ConsultancyOrder,
        TrainingOrder,
        ResearchOrder
    ]
    search_fields = ['inner_id', 'customer']
    list_display = [
            'inner_id',
            'customer',
            'created_at',
            'total_order',
            'discount',
            'grand_total',
            'status'
        ]
    date_hierarchy = 'created_at'
    list_select_related = ['customer']
    raw_id_fields = ['customer']
    list_filter = [
        ('created_at', DateRangeFilter),
        ('grand_total', RangeNumericFilter),
        'status',
    ]
    # actions = ['trash_action', 'draft_action', 'validate_action']

    # def state(self, obj):
    #     return obj.get_status_display()

    # def trash_action(self, request, queryset):
    #     try:
    #         for i in queryset.all():
    #             i.trash()
    #     except PermissionError as err:
    #         print(err)

    # trash_action.short_description = _('Trash selected Sales Orders')

    # def draft_action(self, request, queryset):
    #     try:
    #         for i in queryset.all():
    #             i.draft()
    #     except PermissionError as err:
    #         print(err)

    # draft_action.short_description = _('Draft selected Sales Orders')

    # def validate_action(self, request, queryset):
    #     try:
    #         for i in queryset.all():
    #             i.validate()
    #     except PermissionError as err:
    #         print(err)

    # validate_action.short_description = _('Validate selected Sales Orders')
