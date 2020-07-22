from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.admin import ModelAdmin
from simpellab.modules.sales.admin import PolymorphicOrderAdmin
from simpellab.modules.carts.models import Cart, CommonCart


@admin.register(Cart)
class CartAdmin(PolymorphicParentModelAdmin, ModelAdmin):
    menu_order = 1
    menu_label = 'My Cart'
    menu_icon = 'cart'
    inspect_enabled=False
    list_display = ['product', 'quantity']
    list_select_related = []
    child_models = [
        CommonCart
    ]

    def product(self, obj):
        return obj.get_real_instance().product

    def quantity(self, obj):
        return obj.get_real_instance().quantity

    def get_queryset(self, request):
        return super().get_queryset(request).filter(user=request.user)

    def has_add_permission(self, request, obj=None):
        return False

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = super().get_urls()
        custom_urls = []
        custom_urls.append(
            path('create_order/',
                self.admin_site.admin_view(self.create_order_view),
                name='%s_%s_create_order' % info
                )
        )
        return custom_urls + urls
    
    def create_order_view(self, request, *args, **kwargs):
        return OrderCreateView.as_view(*args, **kwargs)(request)

    def get_child_models(self):
        """ 
            Register child model using hooks

            @hooks.register('cart_child_model', order=1)
            def register_child_model():
                return CartChildModel
            
        """
        super_child_models = super().get_child_models()
        child_models = list(super_child_models).copy()
        
        # list function that return Cart subclass
        func_list = hooks.get_hooks('cart_child_model')
        for func in func_list:
            value = func()
            if issubclass(value, Cart):
                child_models.append(value)
            else:
                raise ImproperlyConfigured('Hook cart_child_model should return Cart subclass')
        return child_models


@admin.register(CommonCart)
class CommonCartAdmin(PolymorphicChildModelAdmin):
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


@hooks.register('admin_menu_item')
def register_cart_menu(request):
    modeladmin = CartAdmin(Cart, admin.site)
    return modeladmin.get_menu_item(request)