from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicParentModelAdmin
    )
from simpellab.admin.admin import ModelAdmin

from simpellab.modules.payments.models import *


@admin.register(PaymentMethod)
class PaymentMethodAdmin(PolymorphicParentModelAdmin, ModelAdmin):
    list_display = ['name', 'rate_method', 'transfer_fee']
    child_models = [
        CashPaymentMethod,
        ManualTransferMethod,
    ]


@admin.register(ManualTransferMethod)
class ManualTransferMethodAdmin(PolymorphicChildModelAdmin, ModelAdmin):
    pass


@admin.register(CashPaymentMethod)
class CashPaymentMethodAdmin(PolymorphicChildModelAdmin, ModelAdmin):
    pass


@admin.register(Receipt)
class ReceiptAdmin(ModelAdmin):
    search_fields = ['inner_id', 'partner__name']
    list_display = ['inner_id', 'partner', 'item', 'amount', 'status']
    actions = ['confirm_payment']

    def confirm_payment(self, request, queryset):
        try:
            for item in queryset:
                item.confirm()
                print('successfully confirming %s' % item)
        except Exception as err:
            print(err)

    
    confirm_payment.short_description = _('Confirm selected payment')