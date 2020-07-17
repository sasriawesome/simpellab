from django.db import models
from django.utils import translation, timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_numerators.models import NumeratorMixin

from simpellab.core.models import SimpleBaseModel
from simpellab.core.enums import MaxLength
from simpellab.modules.services.models import SertificationService
from simpellab.modules.sales.models import SalesOrder, OrderItemBase

_ = translation.ugettext_lazy


__all__ = [
    'SertificationOrder',
    'SertificationOrderItem'
]


class SertificationOrder(SalesOrder):
    class Meta:
        verbose_name = _('Sertification Order')
        verbose_name_plural = _('Sertification Orders')


class SertificationOrderItem(NumeratorMixin, OrderItemBase):
    class Meta:
        verbose_name = _('Sertification Order Item')
        verbose_name_plural = _('Sertification Order Items')
        ordering = ('product',)
        unique_together = ('order', 'product')

    doc_prefix = 'IPRO'

    order = models.ForeignKey(
        SertificationOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        SertificationService,
        on_delete=models.PROTECT,
        related_name='orders')