from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin
from simpellab.admin.admin import ModelAdmin

from simpellab.modules.payments.models import *


@admin.register(PaymentMethod)
class PaymentMethodAdmin(PolymorphicParentModelAdmin, ModelAdmin):
    list_display = ['name', 'rate_method', 'transfer_fee']
    child_models = [
        ManualTransferMethod
    ]


@admin.register(ManualTransferMethod)
class ManualTransferMethod(PolymorphicChildModelAdmin, ModelAdmin):
    pass



@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    pass