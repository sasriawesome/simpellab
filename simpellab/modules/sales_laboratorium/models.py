from django.db import models
from django.utils import translation, timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_numerators.models import NumeratorMixin

from simpellab.core.models import SimpleBaseModel
from simpellab.core.enums import MaxLength
from simpellab.modules.services.models import LaboratoriumService, Parameter
from simpellab.modules.sales.models import SalesOrder, OrderItemBase, ExtraParameterBase

_ = translation.ugettext_lazy


__all__ = [
    'LaboratoriumOrder',
    'LaboratoriumOrderItem',
    'LaboratoriumOrderItemExtraParameter'
]


class LaboratoriumOrder(SalesOrder):
    class Meta:
        verbose_name = _('Laboratorium Order')
        verbose_name_plural = _('Laboratorium Orders')


class LaboratoriumOrderItem(NumeratorMixin, OrderItemBase):
    class Meta:
        verbose_name = _('Laboratorium Order Item')
        verbose_name_plural = _('Laboratorium Order Items')
        ordering = ('product',)
        unique_together = ('order', 'product')

    doc_prefix = 'ILAB'

    order = models.ForeignKey(
        LaboratoriumOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        LaboratoriumService,
        on_delete=models.PROTECT,
        related_name='orders')


class LaboratoriumOrderItemExtraParameter(ExtraParameterBase):
    class Meta:
        verbose_name = _('Extra Parameter')
        verbose_name_plural = _('Extra Parameters')
        unique_together = ('order_item', 'parameter')

    order_item = models.ForeignKey(
        LaboratoriumOrderItem,
        related_name='extra_parameters',
        on_delete=models.CASCADE,
        verbose_name=_('Product'))
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE,
        related_name='lab_extra_parameters',
        verbose_name=_('Parameter'))

    def get_default_parameters(self):
        return self.order_item.product.lab_parameters