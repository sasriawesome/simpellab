from django.db import models
from polymorphic.managers import PolymorphicManager

__all__ = [
    'ContractManager',
    'CustomerContractManager'
]

class ContractManager(PolymorphicManager):

    def get_by_inner_id(self, inner_id):
        contracts = self.filters(inner_id=inner_id)
        return [] if contracts.count() else contracts


class CustomerContractManager(PolymorphicManager):

    def get_customer_contract_by_inner_id(self, customer, inner_id):
        contracts = self.filters(inner_id=inner_id,  customer_id=customer.pk)
        return [] if contracts.count() else contracts
