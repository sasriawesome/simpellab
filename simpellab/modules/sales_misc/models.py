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
    'MiscService',
    'MiscOrder',
    'MiscOrderItem'
]


class MiscService(Service):
    """
        Service Concrete Class
    """
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def get_doc_prefix(self):
        return 'LNY'


class MiscOrder(SalesOrder):
    class Meta:
        verbose_name = _('Misc Order')
        verbose_name_plural = _('Misc Orders')

class MiscOrderItem(NumeratorMixin, OrderItemBase):
    class Meta:
        verbose_name = _('Misc Order Item')
        verbose_name_plural = _('Misc Order Items')
        ordering = ('product',)
        unique_together = ('order', 'product')

    doc_prefix = 'ILNY'

    order = models.ForeignKey(
        MiscOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        MiscService,
        on_delete=models.PROTECT,
        related_name='orders')