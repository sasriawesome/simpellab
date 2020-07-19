from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils import translation, timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from django_numerators.models import NumeratorMixin

from simpellab.core.enums import MaxLength
from simpellab.core.models import SimpleBaseModel, BaseModel
from simpellab.modules.products.models import Service, Parameter
from simpellab.modules.sales.models import SalesOrder, OrderItem, OrderItemParameter

_ = translation.ugettext_lazy


__all__ = [
    'InspectionService',
    'InspectionOrder',
    'InspectionOrderItem',
    'InspectionOrderItemParameter'
]


class InspectionService(Service):
    class Meta:
        verbose_name = _('Technical Inspection')
        verbose_name_plural = _('Technical Inspections')

    def get_doc_prefix(self):
        return 'LIT'


class InspectionOrder(SalesOrder):
    class Meta:
        verbose_name = _('Inspection Order')
        verbose_name_plural = _('Inspection Orders')

    def get_order_items(self):
        """ Get child object order_items """
        return self.order_items

        
class InspectionOrderItem(OrderItem):
    class Meta:
        verbose_name = _('Inspection Order Item')
        verbose_name_plural = _('Inspection Order Items')

    doc_prefix = 'ILIT'

    order = models.ForeignKey(
        InspectionOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        InspectionService,
        on_delete=models.PROTECT,
        related_name='orders')

    def get_parameter_prices(self):
        return self.parameters.aggregate(
            total_parameters=models.Sum('price')
        )['total_parameters'] or 0

    def calculate_unit_price(self):
        base_price = self.product.get_real_instance().total_price
        parameters = self.get_parameter_prices()
        unit_price = base_price + parameters
        return unit_price


class InspectionOrderItemParameter(OrderItemParameter):
    class Meta:
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')
        unique_together = ('order_item', 'parameter')

    order_item = models.ForeignKey(
        InspectionOrderItem,
        related_name='parameters',
        on_delete=models.CASCADE,
        verbose_name=_('Product'))
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE,
        related_name='lit_parameters',
        verbose_name=_('Parameter'))
    

@receiver(post_save, sender=InspectionOrderItem)
def after_save_lit_item(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_delete, sender=InspectionOrderItem)
def after_delete_lit_item(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_save, sender=InspectionOrderItemParameter)
def after_save_lit_parameter(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    print(instance.order_item)
    instance.order_item.save()


@receiver(post_delete, sender=InspectionOrderItemParameter)
def after_delete_lit_parameter(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    print(instance.order_item)
    instance.order_item.save()