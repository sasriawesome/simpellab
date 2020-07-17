from django.db import models
from django.utils import translation, timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_numerators.models import NumeratorMixin

from simpellab.core.models import SimpleBaseModel
from simpellab.core.enums import MaxLength
from simpellab.modules.services.models import ResearchService
from simpellab.modules.sales.models import SalesOrder, OrderItemBase

_ = translation.ugettext_lazy


__all__ = [
    'ResearchOrder',
    'ResearchOrderItem'
]


class ResearchOrder(SalesOrder):
    class Meta:
        verbose_name = _('Research Order')
        verbose_name_plural = _('Research Orders')


class ResearchOrderItem(NumeratorMixin, OrderItemBase):
    class Meta:
        verbose_name = _('Research Order Item')
        verbose_name_plural = _('Research Order Items')
        ordering = ('product',)
        unique_together = ('order', 'product')

    doc_prefix = 'ILIB'

    order = models.ForeignKey(
        ResearchOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        ResearchService,
        on_delete=models.PROTECT,
        related_name='orders')