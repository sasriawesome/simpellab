import nested_admin
from django.contrib import admin
from django.utils import translation
from django.core.exceptions import ImproperlyConfigured

from rangefilter.filter import DateRangeFilter
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from admin_numeric_filter.admin import RangeNumericFilter

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin, ReadOnlyAdminMixin, ModelMenuGroup
from simpellab.modules.sales.models import *


_ = translation.ugettext_lazy


class OrderFeeInline(nested_admin.NestedTabularInline):
    extra = 0
    min_num = 0
    model = OrderFee
    autocomplete_fields = ['fee']
    readonly_fields = ['amount', 'total_fee']


class SalesOrderChildAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderFeeInline]
    readonly_fields = ['total_order', 'discount', 'grand_total']

    def get_inlines(self, request, obj):
        """Hook for specifying custom inlines."""
        if obj and self.has_change_permission:
            return self.inlines
        else:
            return [OrderFeeInline]


class SalesOrderItemInline(nested_admin.NestedStackedInline):
    extra = 0
    min_num = 1
    autocomplete_fields = ['product']
    fields = ['product', 'name', 'quantity', 'note', 'unit_price', 'total_price']
    readonly_fields = ['unit_price', 'total_price']


class OrderAdminBase(ModelAdmin):
    menu_icon = 'bookmark'
    list_display = ['customer', 'created_at']
    search_fields = ['inner_id', 'customer__name']
    list_display = [
            'inner_id',
            'customer',
            'created_at',
            'total_order',
            'discount',
            'grand_total',
            'state'
        ]
    date_hierarchy = 'created_at'
    list_select_related = ['customer']
    autocomplete_fields = ['customer']
    list_filter = [
        ('created_at', DateRangeFilter),
        ('grand_total', RangeNumericFilter),
        'status',
    ]
    actions = ['trash_action', 'draft_action', 'validate_action']

    def state(self, obj):
        return obj.get_status_display()

    def trash_action(self, request, queryset):
        try:
            for i in queryset.all():
                i.get_real_instance().trash()
        except PermissionError as err:
            print(err)

    trash_action.short_description = _('Trash selected Sales Orders')

    def draft_action(self, request, queryset):
        try:
            for i in queryset.all():
                i.get_real_instance().draft()
        except PermissionError as err:
            print(err)

    draft_action.short_description = _('Draft selected Sales Orders')

    def validate_action(self, request, queryset):
        try:
            for i in queryset.all():
                real = i.get_real_instance()
                real.validate()
        except PermissionError as err:
            print(err)

    validate_action.short_description = _('Validate selected Sales Orders')

    def get_inspect_context(self, obj, request, extra_context=None):
        context = {
            **self.admin_site.each_context(request),
            'self': self,
            'opts': self.opts,
            'instance': obj.get_real_instance(),
            **(extra_context or {})
        }
        return context


@admin.register(SalesOrder)
class OrderAdmin(ReadOnlyAdminMixin, OrderAdminBase):
    pass


class PolymorphicOrderAdmin(PolymorphicParentModelAdmin, OrderAdminBase):
    child_models = [
        CommonOrder
    ]

    def get_child_models(self):
        """ 
            Register child model using hooks

            @hooks.register('sales_order_child_model', order=1)
            def register_child_model():
                return ChildModel
        """
        super_child_models = super().get_child_models()
        child_models = list(super_child_models).copy()
        
        # list function that return SalesOrderModel
        for func in hooks.get_hooks('sales_order_child_model'):
            value = func()
            if issubclass(value, SalesOrder):
                child_models.append(value)
            else:
                raise ImproperlyConfigured('Hook sales_order_child_model should return SalesOrder subclass')
        
        return child_models


class CommonOrderItemInline(SalesOrderItemInline):
    model = CommonOrderItem


@admin.register(CommonOrder)
class CommonOrderAdmin(SalesOrderChildAdmin):
    inlines = [OrderFeeInline, CommonOrderItemInline]


@admin.register(Invoice)
class InvoiceAdmin(ReadOnlyAdminMixin, ModelAdmin):
    menu_icon = 'bookmark'
    search_fields = ['inner_id', 'billed_to__name']
    list_display = ['inner_id', 'billed_to', 'sales_order', 'due_date', 'grand_total', 'paid', 'contract']


class SalesModelMenuGroup(ModelMenuGroup):
    adminsite = admin.site
    menu_icon = 'bookmark'
    menu_label = _('Sales')
    menu_order = 3
    items = [ 
        (SalesOrder, OrderAdmin), 
        (Invoice, InvoiceAdmin),
    ]


@hooks.register('admin_menu_item')
def register_sales_menu(request):
    group = SalesModelMenuGroup()
    return group.get_menu_item(request)
