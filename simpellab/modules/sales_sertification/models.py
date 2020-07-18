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
from simpellab.modules.sales.models import SalesOrder, OrderItem, ExtraParameterBase

_ = translation.ugettext_lazy


__all__ = [
    'SertificationService',
    'SertificationOrder',
    'SertificationOrderItem'
]


class SertificationService(Service):
    class Meta:
        verbose_name = _('Product Sertification')
        verbose_name_plural = _('Product Sertifications')

    def get_doc_prefix(self):
        return 'PRO'


class SertificationOrder(SalesOrder):
    class Meta:
        verbose_name = _('Sertification Order')
        verbose_name_plural = _('Sertification Orders')

    def get_order_items(self):
        """ Get child object order_items """
        return self.order_items


class SertificationOrderItem(OrderItem):
    class Meta:
        verbose_name = _('Sertification Order Item')
        verbose_name_plural = _('Sertification Order Items')
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


@receiver(post_save, sender=SertificationOrderItem)
def after_save_order_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_delete, sender=SertificationOrderItem)
def after_delete_order_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()