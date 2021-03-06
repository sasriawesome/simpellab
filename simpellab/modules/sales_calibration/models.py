from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils import translation, timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_numerators.models import NumeratorMixin

from simpellab.core.enums import MaxLength
from simpellab.core.models import SimpleBaseModel, BaseModel
from simpellab.modules.products.models import Service, Parameter
from simpellab.modules.sales.models import SalesOrder, OrderItem

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

    def get_order_items(self):
        """ Get child object order_items """
        return self.order_items


class CalibrationOrderItem(OrderItem):
    class Meta:
        verbose_name = _('Calibration Order Item')
        verbose_name_plural = _('Calibration Order Items')

    doc_prefix = 'IKAL'

    order = models.ForeignKey(
        CalibrationOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        CalibrationService,
        on_delete=models.PROTECT,
        related_name='orders')


@receiver(post_save, sender=CalibrationOrderItem)
def after_save_kal_item(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_delete, sender=CalibrationOrderItem)
def after_delete_kal_item(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()