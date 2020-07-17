from django.db import models
from django.utils import translation, timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_numerators.models import NumeratorMixin

from simpellab.core.models import SimpleBaseModel
from simpellab.core.enums import MaxLength
from simpellab.modules.services.models import TrainingService
from simpellab.modules.sales.models import SalesOrder, OrderItemBase

_ = translation.ugettext_lazy


__all__ = [
    'TrainingOrder',
    'TrainingOrderItem'
]


class TrainingOrder(SalesOrder):
    class Meta:
        verbose_name = _('Training Order')
        verbose_name_plural = _('Training Orders')


class TrainingOrderItem(NumeratorMixin, OrderItemBase):
    class Meta:
        verbose_name = _('Training Order Item')
        verbose_name_plural = _('Training Order Items')
        ordering = ('product',)
        unique_together = ('order', 'product')

    doc_prefix = 'ILAT'

    order = models.ForeignKey(
        TrainingOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        TrainingService,
        on_delete=models.PROTECT,
        related_name='orders')