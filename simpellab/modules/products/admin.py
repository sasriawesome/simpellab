from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from simpellab.admin.admin import ModelAdmin
from .models import (
    Product, Asset, Inventory,
    Fee, Tag, Category, UnitOfMeasure, Specification,
    ProductFee
)
from .filters import ProductChildFilter


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    show_in_index = True
    search_fields = ['name']


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    raw_id_fields = ['unit_of_measure']


class ProductChildAdmin(PolymorphicChildModelAdmin, ModelAdmin):
    base_model = Product


@admin.register(Product)
class ProductAdmin(PolymorphicParentModelAdmin, ModelAdmin):
    """ Parent admin Product Model, set child model in settings """
    search_fields = ['name']
    child_models = [
        Asset,
        Inventory
    ]
    list_filter = [ProductChildFilter]
    list_display = ['inner_id', 'name', 'price', 'fee', 'total_price']


class SpecificationInline(admin.StackedInline):
    extra = 0
    model = Specification


class ProductFeeInline(admin.TabularInline):
    extra = 0
    model = ProductFee
    raw_id_fields = ['fee']
    readonly_fields = ['price', 'date_effective']


class ProductMixin(admin.ModelAdmin):
    ordering = ['-created_at']
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



# @admin.register(ANYService)
# class ANYServiceAdmin(ProductMixin, ProductChildAdmin):
#     pass
#
#
# @admin.register(KALService)
# class KALServiceAdmin(ProductMixin, ProductChildAdmin):
#     pass
#
#
# @admin.register(KSLService)
# class KSLServiceAdmin(ProductMixin, ProductChildAdmin):
#     pass
#
#
# @admin.register(LIBService)
# class LIBServiceAdmin(ProductMixin, ProductChildAdmin):
#     pass
#
#
# @admin.register(PROService)
# class PROServiceAdmin(ProductMixin, ProductChildAdmin):
#     pass


# @admin.register(LATService)
# class LATServiceAdmin(ProductMixin, ProductChildAdmin):
#     pass
#
#

#
#
# @admin.register(LABService)
# class LABServiceAdmin(ProductChildAdmin):
#     readonly_fields = ['price', 'fee', 'total_price']
#     inlines = [ProductFeeInline]
#
#
# class LITParameterInline(admin.TabularInline):
#     extra = 0
#     model = LITParameter
#     raw_id_fields = ['parameter']
#     readonly_fields = ['price', 'date_effective']
#
#
# @admin.register(LITService)
# class LITServiceAdmin(ProductChildAdmin):
#     readonly_fields = ['price', 'fee', 'total_price']
#     inlines = [ProductFeeInline]
