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
    'ResearchService',
    'ResearchOrder',
    'ResearchOrderItem'
]


class ResearchService(Service):
    class Meta:
        verbose_name = _('Research and Development')
        verbose_name_plural = _('Research and Developments')

    def get_doc_prefix(self):
        return 'LIB'


class ResearchOrder(SalesOrder):
    class Meta:
        verbose_name = _('Research Order')
        verbose_name_plural = _('Research Orders')

    def get_order_items(self):
        """ Get child object order_items """
        return self.order_items


class ResearchOrderItem(OrderItem):
    class Meta:
        verbose_name = _('Research Order Item')
        verbose_name_plural = _('Research Order Items')

    doc_prefix = 'ILIB'

    order = models.ForeignKey(
        ResearchOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        ResearchService,
        on_delete=models.PROTECT,
        related_name='orders')


@receiver(post_save, sender=ResearchOrderItem)
def after_save_order_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_delete, sender=ResearchOrderItem)
def after_delete_order_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()