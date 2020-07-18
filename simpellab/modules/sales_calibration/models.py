from django.db import models
from django.utils import translation, timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_numerators.models import NumeratorMixin

from simpellab.core.enums import MaxLength
from simpellab.core.models import SimpleBaseModel, BaseModel
from simpellab.modules.products.models import Service, Parameter
from simpellab.modules.sales.models import SalesOrder, OrderItemBase, ExtraParameterBase

_ = translation.ugettext_lazy


__all__ = [
    'CalibrationService',
    'CalibrationOrder',
    'CalibrationOrderItem'
]


class CalibrationService(Service):
    class Meta:
        verbose_name = _('Calibration')
        verbose_name_plural = _('Calibration')

    def get_doc_prefix(self):
        return 'KAL'


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