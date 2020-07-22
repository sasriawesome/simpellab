from django.contrib import admin
from simpellab.admin.admin import ModelAdmin

from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicParentModelAdmin)
from simpellab.modules.contracts.models import *


@admin.register(Contract)
class ContractAdmin(PolymorphicParentModelAdmin):
    list_display = [
        'inner_id',
        'title',
        'issued_at',
        'active_at',
        'expired_at',
        'valid_days',
        'is_valid'
    ]
    child_models = [
        CustomerContract
    ]

@admin.register(CustomerContract)
class CustomerContractAdmin(PolymorphicChildModelAdmin):
    pass


