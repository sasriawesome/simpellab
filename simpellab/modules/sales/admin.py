import nested_admin
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.utils import translation
from django.shortcuts import reverse, redirect
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

    def response_delete(self, request, obj_display, obj_id):
        """
        Determine the HttpResponse for the delete_view stage.
        """
        opts = self.model._meta

        if '_popup' in request.POST:
            popup_response_data = json.dumps({
                'action': 'delete',
                'value': str(obj_id),
            })
            return TemplateResponse(request, self.popup_response_template or [
                'admin/%s/%s/popup_response.html' % (opts.app_label, opts.model_name),
                'admin/%s/popup_response.html' % opts.app_label,
                'admin/popup_response.html',
            ], {
                'popup_response_data': popup_response_data,
            })

        self.message_user(
            request,
            _('The %(name)s “%(obj)s” was deleted successfully.') % {
                'name': opts.verbose_name,
                'obj': obj_display,
            },
            messages.SUCCESS,
        )

        if self.has_change_permission(request, None):
            post_url = reverse(
                'admin:simpellab_sales_salesorder_changelist',
                current_app=self.admin_site.name,
            )
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': opts}, post_url
            )
        else:
            post_url = reverse('admin:index', current_app=self.admin_site.name)
        return redirect(post_url)

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


class OrderAdmin(ReadOnlyAdminMixin, OrderAdminBase):
    pass


@admin.register(SalesOrder)
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
    list_display = [
        'inner_id', 
        'billed_to',
        'sales_order',
        'due_date',
        'grand_total',
        'paid',
        'contract'
        ]


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
