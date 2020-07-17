from django.db import models
from django.utils import translation, timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from django_numerators.models import NumeratorMixin

from simpellab.core.models import SimpleBaseModel
from simpellab.core.enums import MaxLength
from simpellab.modules.services.models import InspectionService, Parameter
from simpellab.modules.sales.models import SalesOrder, OrderItemBase, ExtraParameterBase

_ = translation.ugettext_lazy


__all__ = [
    'InspectionOrder',
    'InspectionOrderItem',
    'InspectionOrderItemExtraParameter'
]


class InspectionOrder(SalesOrder):
    class Meta:
        verbose_name = _('Inspection Order')
        verbose_name_plural = _('Inspection Orders')

class InspectionOrderItem(NumeratorMixin, OrderItemBase):
    class Meta:
        verbose_name = _('Inspection Order Item')
        verbose_name_plural = _('Inspection Order Items')
        ordering = ('product',)
        unique_together = ('order', 'product')

    doc_prefix = 'ILIT'

    order = models.ForeignKey(
        InspectionOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        InspectionService,
        on_delete=models.PROTECT,
        related_name='orders')


class InspectionOrderItemExtraParameter(ExtraParameterBase):
    class Meta:
        verbose_name = _('Extra Parameter')
        verbose_name_plural = _('Extra Parameters')
        unique_together = ('order_item', 'parameter')

    order_item = models.ForeignKey(
        InspectionOrderItem,
        related_name='extra_parameters',
        on_delete=models.CASCADE,
        verbose_name=_('Product'))
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE,
        related_name='lit_extra_parameters',
        verbose_name=_('Parameter'))
    
    def get_default_parameters(self):
        return self.order_item.product.lit_parameters