import nested_admin
from django.contrib import admin
from django.utils import translation
from django.core.exceptions import ImproperlyConfigured

from rangefilter.filter import DateRangeFilter
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from admin_numeric_filter.admin import RangeNumericFilter

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin, ModelMenuGroup
from simpellab.modules.partners.models import Partner
from simpellab.modules.partners.admin import PartnerAdmin
from simpellab.modules.sales.forms import OrderProductFormset
from simpellab.modules.sales.models import *


_ = translation.ugettext_lazy


class OrderFeeInline(nested_admin.NestedTabularInline):
    extra = 0
    min_num = 0
    model = OrderFee
    autocomplete_fields = ['fee']
    readonly_fields = ['amount', 'total_fee']


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
                i.get_real_instance().validate()
        except PermissionError as err:
            print(err)

    validate_action.short_description = _('Validate selected Sales Orders')


@admin.register(SalesOrder)
class PolymorphicOrderAdmin(PolymorphicParentModelAdmin, OrderAdminBase):
    child_models = [
        CommonOrder
    ]
    
    def get_inspect_context(self, obj, request, extra_context=None):
        context = {
            **self.admin_site.each_context(request),
            'self': self,
            'opts': self.opts,
            'instance': obj.get_real_instance(),
            **(extra_context or {})
        }
        return context

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


class CommonOrderItemInline(nested_admin.NestedTabularInline):
    extra = 0
    min_num = 1
    model = CommonOrderItem
    autocomplete_fields = ['product']
    fields = ['product', 'name', 'quantity', 'note', 'unit_price', 'total_price']
    readonly_fields = ['unit_price', 'total_price']


@admin.register(CommonOrder)
class CommonOrderAdmin(PolymorphicChildModelAdmin, nested_admin.NestedModelAdmin, ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderFeeInline, CommonOrderItemInline]
    readonly_fields = ['total_order', 'discount', 'grand_total']


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    menu_icon = 'bookmark'
    search_fields = ['inner_id', 'billed_to__name']
    list_display = ['inner_id', 'billed_to', 'sales_order', 'due_date', 'grand_total', 'paid']

    def has_change_permission(self, request, obj=None):
        return True


class SalesModelMenuGroup(ModelMenuGroup):
    adminsite = admin.site
    menu_icon = 'cart'
    menu_label = _('Partner and Sales')
    menu_order = 3
    items = [ 
        (SalesOrder, PolymorphicOrderAdmin), 
        (Invoice, InvoiceAdmin), 
        (Partner, PartnerAdmin), 
    ]


@hooks.register('admin_menu_item')
def register_sales_menu(request):
    group = SalesModelMenuGroup()
    return group.get_menu_item(request)
