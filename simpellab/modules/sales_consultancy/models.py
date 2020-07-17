from django.db import models
from django.utils import translation, timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_numerators.models import NumeratorMixin

from simpellab.core.models import SimpleBaseModel
from simpellab.core.enums import MaxLength
from simpellab.modules.services.models import ConsultancyService
from simpellab.modules.sales.models import SalesOrder, OrderItemBase

_ = translation.ugettext_lazy


__all__ = ['ConsultancyOrder', 'ConsultancyOrderItem']


class ConsultancyOrder(SalesOrder):
    class Meta:
        verbose_name = _('Consultancy Order')
        verbose_name_plural = _('Consultancy Orders')


class ConsultancyOrderItem(NumeratorMixin, OrderItemBase):
    class Meta:
        verbose_name = _('Consultancy Order Item')
        verbose_name_plural = _('Consultancy Order Items')
        ordering = ('product',)
        unique_together = ('order', 'product')

    doc_prefix = 'IKSL'

    order = models.ForeignKey(
        ConsultancyOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        ConsultancyService,
        on_delete=models.PROTECT,
        related_name='orders')