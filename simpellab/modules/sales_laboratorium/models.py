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
    'LaboratoriumService',
    'LaboratoriumServiceParameter',
    'LaboratoriumOrder',
    'LaboratoriumOrderItem',
    'LaboratoriumOrderItemExtraParameter'
]


class LaboratoriumService(Service):
    class Meta:
        verbose_name = _('Laboratorium Test')
        verbose_name_plural = _('Laboratorium Tests')
    
    parameter_price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Parameter'))

    def get_doc_prefix(self):
        return 'LAB'

    def get_parameter_price(self):
        return self.lab_parameters.aggregate(
            total_parameters=models.Sum('price')
        )['total_parameters'] or 0

    def get_price(self):
        return self.price

    def get_total_price(self):
        return self.price + self.fee + self.parameter_price

    def save(self, *args, **kwargs):
        self.parameter_price = self.get_parameter_price()
        super().save(*args, **kwargs)


class LaboratoriumServiceParameter(BaseModel):
    class Meta:
        verbose_name = _('Laboratorium Parameter')
        verbose_name_plural = _('Laboratorium Parameters')
        unique_together = ('service', 'parameter')

    _ori_parameter = None

    service = models.ForeignKey(
        LaboratoriumService,
        related_name='lab_parameters',
        on_delete=models.CASCADE,
        verbose_name=_('Service'))
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE,
        related_name='lab_services',
        verbose_name=_('Parameter'))
    price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Price'))
    date_effective = models.DateField(
        default=timezone.now,
        verbose_name=_('Date effective'))


class LaboratoriumOrder(SalesOrder):
    class Meta:
        verbose_name = _('Laboratorium Order')
        verbose_name_plural = _('Laboratorium Orders')


class LaboratoriumOrderItem(NumeratorMixin, OrderItemBase):
    class Meta:
        verbose_name = _('Laboratorium Order Item')
        verbose_name_plural = _('Laboratorium Order Items')
        ordering = ('product',)
        unique_together = ('order', 'product')

    doc_prefix = 'ILAB'

    order = models.ForeignKey(
        LaboratoriumOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        LaboratoriumService,
        on_delete=models.PROTECT,
        related_name='orders')
    
    def get_parameter_prices(self):
        return self.extra_parameters.aggregate(
            total_parameters=models.Sum('price')
        )['total_parameters'] or 0

    def calculate_unit_price(self):
        base_price = self.product.get_real_instance().total_price
        extra_parameters = self.get_parameter_prices()
        unit_price = base_price + extra_parameters
        return base_price


class LaboratoriumOrderItemExtraParameter(ExtraParameterBase):
    class Meta:
        verbose_name = _('Extra Parameter')
        verbose_name_plural = _('Extra Parameters')
        unique_together = ('order_item', 'parameter')

    order_item = models.ForeignKey(
        LaboratoriumOrderItem,
        related_name='extra_parameters',
        on_delete=models.CASCADE,
        verbose_name=_('Product'))
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE,
        related_name='lab_extra_parameters',
        verbose_name=_('Parameter'))

    def get_default_parameters(self):
        return self.order_item.product.lab_parameters