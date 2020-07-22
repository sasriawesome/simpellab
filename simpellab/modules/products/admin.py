from django.urls import path
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.utils.html import format_html
from django.shortcuts import reverse, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.menus import admin_menu
from simpellab.admin.admin import ModelAdmin, ModelMenuGroup
from simpellab.modules.products.models import *
from simpellab.modules.carts.models import CommonCart

from .filters import ProductChildFilter


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    inspect_enabled = False
    search_fields = ['name']
    menu_icon = 'tag'


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    inspect_enabled = False
    search_fields = ['name']
    menu_icon = 'tag'


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(ModelAdmin):
    inspect_enabled = False
    search_fields = ['name']
    menu_icon = 'tag'


@admin.register(Parameter)
class ParameterAdmin(ModelAdmin):
    inspect_enabled = False
    search_fields = ['name']
    list_display = ['name', 'ptype', 'price']
    autocomplete_fields = ['unit_of_measure']
    menu_icon = 'filter'

@admin.register(Fee)
class FeeAdmin(ModelAdmin):
    inspect_enabled = False
    search_fields = ['name']
    list_display = ['name', 'description', 'price']
    autocomplete_fields = ['unit_of_measure']
    menu_icon = 'tag'


@admin.register(Product)
class ProductAdmin(PolymorphicParentModelAdmin, ModelAdmin):
    """ Parent admin Product Model, set child model in settings """
    menu_icon = 'package'
    search_fields = ['name']
    child_models = [
        Asset,
        Inventory
    ]
    list_filter = [ProductChildFilter]
    list_display = ['inner_id', 'name', 'price', 'fee', 'total_price']

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = super().get_urls()
        custom_urls = []
        custom_urls.append(
            path('<path:object_id>/add_to_cart/',
                    self.admin_site.admin_view(self.add_to_cart_view),
                    name='%s_%s_add_to_cart' % info
                    )
        )
        return custom_urls + urls
    
    def add_to_cart_view(self, request, object_id, *args, **kwargs):
        product = get_object_or_404(self.model, pk=object_id)
        try:
            cart_item = product.add_to_cart(request)
            return redirect(reverse('admin:simpellab_carts_cart_change', args=(cart_item.id,)))
        except Exception as err:
            print(err)
            return redirect(reverse('admin:simpellab_carts_cart_changelist'))

    def get_list_display(self, request):
        list_display = super().get_list_display(request).copy()
        if self.has_view_or_change_permission(request):
            list_display.append('add_to_cart_link')
        return list_display
        
    def add_to_cart_link(self, obj):
        template = "<a class='addlink' href='%s' title='%s'></a>"
        url = reverse(self.get_url_name('add_to_cart'), args=(obj.id,))
        return format_html(template % (url, _('add to cart').title()))
    
    add_to_cart_link.short_description=''

    def get_child_models(self):
        """ 
            Register child model using hooks

            @hooks.register('product_child_model', order=1)
            def register_child_model():
                return ProductChildModel
            
        """
        super_child_models = super().get_child_models()
        child_models = list(super_child_models).copy()
        
        # list function that return Product subclass
        func_list = hooks.get_hooks('product_child_model')
        for func in func_list:
            value = func()
            if issubclass(value, Product):
                child_models.append(value)
            else:
                raise ImproperlyConfigured('Hook product_child_model should return Product subclass')
        return child_models


class SpecificationInline(admin.StackedInline):
    extra = 0
    model = Specification


class ProductFeeInline(admin.TabularInline):
    extra = 0
    model = ProductFee
    raw_id_fields = ['fee']
    readonly_fields = ['price', 'date_effective']

    
class ProductAdmin(ModelAdmin):
    menu_icon = 'package'
    ordering = ['-created_at']
    list_display = ['name']
    search_fields = ['inner_id', 'name']
    date_hierarchy = 'created_at'
    raw_id_fields = ['category', 'unit_of_measure']
    readonly_fields = ['fee', 'total_price']
    inlines = [SpecificationInline, ProductFeeInline]


class ProductChildAdmin(PolymorphicChildModelAdmin, ProductAdmin):
    base_model = Product

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
                'admin:simpellab_products_product_changelist',
                current_app=self.admin_site.name,
            )
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': opts}, post_url
            )
        else:
            post_url = reverse('admin:index', current_app=self.admin_site.name)
        return redirect(post_url)

@admin.register(Asset)
class AssetAdmin(ProductChildAdmin):
    pass


@admin.register(Inventory)
class InventoryAdmin(ProductChildAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(ProductChildAdmin):
    pass


class ProductModelMenuGroup(ModelMenuGroup):
    adminsite = admin.site
    menu_icon = 'package'
    menu_label = _('Products')
    menu_order = 2
    items = [ 
        (Product, ProductAdmin), 
        (Parameter, ParameterAdmin), 
        (Category, CategoryAdmin), 
        (UnitOfMeasure, UnitOfMeasureAdmin), 
        (Tag, TagAdmin), 
        (Fee, FeeAdmin), 
    ]


@hooks.register('admin_menu_item')
def register_product_menu(request):
    group = ProductModelMenuGroup()
    return group.get_menu_item(request)