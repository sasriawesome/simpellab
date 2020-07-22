from django.contrib import admin
from django.db import transaction
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import reverse, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.menus import admin_menu
from simpellab.admin.admin import ModelAdmin, ModelMenuGroup
from simpellab.modules.carts.models import Cart
from simpellab.modules.blueprints.models import *


@admin.register(Blueprint)
class BlueprintAdmin(PolymorphicParentModelAdmin, ModelAdmin):
    """ Parent admin Blueprint Model, set child model in settings """
    menu_icon = 'package'
    menu_label = _('My Blueprints')
    menu_order = 1
    search_fields = ['name']
    child_models = []
    list_display = ['name', 'product']
    inspect_enabled = False
    
    def product(self, obj):
        return obj.get_real_instance().product

    def get_queryset(self, request):
        return super().get_queryset(request).filter(user=request.user)

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
        blueprint = get_object_or_404(self.model, pk=object_id)
        try:
            cart_item = blueprint.add_to_cart(request)
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
        return format_html(template % (url, _('add_to_cart').title()))
    
    add_to_cart_link.short_description=''


    def get_child_models(self):
        """ 
            Register child model using hooks

            @hooks.register('blueprint_child_model', order=1)
            def register_child_model():
                return BlueprintChildModel
            
        """
        super_child_models = super().get_child_models()
        child_models = list(super_child_models).copy()
        
        # list function that return Product subclass
        func_list = hooks.get_hooks('blueprint_child_model')
        for func in func_list:
            value = func()
            if issubclass(value, Blueprint):
                child_models.append(value)
            else:
                raise ImproperlyConfigured('Hook blueprint_child_model should return Product subclass')
        return child_models


@hooks.register('admin_menu_item')
def register_blueprint_menu(request):
    modeladmin = BlueprintAdmin(Blueprint, admin.site)
    return modeladmin.get_menu_item(request)