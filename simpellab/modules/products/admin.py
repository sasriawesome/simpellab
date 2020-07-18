from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.menus import admin_menu
from simpellab.admin.admin import ModelAdmin, ModelMenuGroup
from simpellab.modules.products.models import *
from .filters import ProductChildFilter


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    menu_icon = 'tag'


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    menu_icon = 'tag'


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(ModelAdmin):
    search_fields = ['name']
    menu_icon = 'tag'


@admin.register(Parameter)
class ParameterAdmin(ModelAdmin):
    raw_id_fields = ['unit_of_measure']
    menu_icon = 'filter'

@admin.register(Fee)
class FeeAdmin(ModelAdmin):
    raw_id_fields = ['unit_of_measure']
    menu_icon = 'tag'

class ProductChildAdmin(PolymorphicChildModelAdmin, ModelAdmin):
    base_model = Product


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


class ProductMixin(ModelAdmin):
    ordering = ['-created_at']
    list_display = ['name']
    search_fields = ['inner_id', 'name']
    date_hierarchy = 'created_at'
    raw_id_fields = ['category', 'unit_of_measure']
    readonly_fields = ['fee', 'total_price']
    inlines = [SpecificationInline, ProductFeeInline]


@admin.register(Asset)
class AssetAdmin(ProductMixin, ProductChildAdmin, ModelAdmin):
    pass


@admin.register(Inventory)
class InventoryAdmin(ProductMixin, ProductChildAdmin, ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(ProductMixin, ProductChildAdmin, ModelAdmin):
    pass


class ProductModelMenuGroup(ModelMenuGroup):
    adminsite = admin.site
    menu_icon = 'package'
    menu_label = _('Product and Services')
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
    return group.get_menu_item()