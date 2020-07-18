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
    'TrainingService',
    'TrainingTopic',
    'TrainingOrder',
    'TrainingOrderItem'
]


class TrainingService(Service):
    class Meta:
        verbose_name = _('Training and Coaching')
        verbose_name_plural = _('Training and Coachings')

    audience_min = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(0)],
        verbose_name=_('Minimum audience')
        )
    audience_criterias = models.TextField(
        max_length=MaxLength.TEXT.value,
        verbose_name=_('Audience criterias')
        )
        
    def get_doc_prefix(self):
        return 'LAT'


class TrainingTopic(SimpleBaseModel):
    class Meta:
        verbose_name = _('Training Topic')
        verbose_name_plural = _('Training Topics')

    service = models.ForeignKey(
        TrainingService,
        related_name='topics',
        on_delete=models.CASCADE,
        verbose_name=_('Service'))
    title = models.CharField(max_length=MaxLength.MEDIUM.value)
    description = models.TextField(max_length=MaxLength.TEXT.value)

    def __str__(self):
        return self.topic


class TrainingOrder(SalesOrder):
    class Meta:
        verbose_name = _('Training Order')
        verbose_name_plural = _('Training Orders')

    def get_order_items(self):
        """ Get child object order_items """
        return self.order_items


class TrainingOrderItem(OrderItem):
    class Meta:
        verbose_name = _('Training Order Item')
        verbose_name_plural = _('Training Order Items')
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


@receiver(post_save, sender=TrainingOrderItem)
def after_save_order_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_delete, sender=TrainingOrderItem)
def after_delete_order_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()