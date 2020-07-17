from django.db import models
from django.utils import translation, timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_numerators.models import NumeratorMixin

from simpellab.core.models import SimpleBaseModel
from simpellab.core.enums import MaxLength
from simpellab.modules.services.models import CalibrationService
from simpellab.modules.sales.models import SalesOrder, OrderItemBase

_ = translation.ugettext_lazy


__all__ = ['CalibrationOrder', 'CalibrationOrderItem']


class CalibrationOrder(SalesOrder):
    class Meta:
        verbose_name = _('Calibration Order')
        verbose_name_plural = _('Calibration Orders')


class CalibrationOrderItem(NumeratorMixin, OrderItemBase):
    class Meta:
        verbose_name = _('Calibration Order Item')
        verbose_name_plural = _('Calibration Order Items')
        ordering = ('product',)
        unique_together = ('order', 'product')

    doc_prefix = 'IKAL'

    order = models.ForeignKey(
        CalibrationOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        CalibrationService,
        on_delete=models.PROTECT,
        related_name='orders')