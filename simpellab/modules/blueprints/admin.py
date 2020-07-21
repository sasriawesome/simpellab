from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from simpellab.core import hooks
from simpellab.admin.menus import admin_menu
from simpellab.admin.admin import ModelAdmin, ModelMenuGroup
from simpellab.modules.blueprints.models import *


@admin.register(Blueprint)
class BlueprintAdmin(PolymorphicParentModelAdmin, ModelAdmin):
    """ Parent admin Blueprint Model, set child model in settings """
    menu_icon = 'package'
    menu_order = 1
    search_fields = ['name']
    child_models = []
    list_display = ['user', 'name']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(user=request.user)

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