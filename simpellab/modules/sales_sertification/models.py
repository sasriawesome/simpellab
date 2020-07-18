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