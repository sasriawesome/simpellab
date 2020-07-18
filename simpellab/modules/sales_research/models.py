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