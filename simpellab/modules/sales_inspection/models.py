from django.db import models
from django.utils import translation, timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from django_numerators.models import NumeratorMixin

from simpellab.core.enums import MaxLength
from simpellab.core.models import SimpleBaseModel, BaseModel
from simpellab.modules.products.models import Service, Parameter
from simpellab.modules.sales.models import SalesOrder, OrderItemBase, ExtraParameterBase

_ = translation.ugettext_lazy


__all__ = [
    'InspectionService',
    'InspectionServiceParameter',
    'InspectionOrder',
    'InspectionOrderItem',
    'InspectionOrderItemExtraParameter'
]


class InspectionService(Service):
    class Meta:
        verbose_name = _('Technical Inspection')
        verbose_name_plural = _('Technical Inspections')

    parameter_price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Parameter'))

    def get_doc_prefix(self):
        return 'LIT'

    def get_parameter_price(self):
        return self.lit_parameters.aggregate(
            total_parameters=models.Sum('price')
        )['total_parameters'] or 0

    def get_price(self):
        return self.price

    def get_total_price(self):
        return self.price + self.fee + self.parameter_price

    def save(self, *args, **kwargs):
        self.parameter_price = self.get_parameter_price()
        super().save(*args, **kwargs)


class InspectionServiceParameter(BaseModel):
    class Meta:
        verbose_name = _('Inspection Parameter')
        verbose_name_plural = _('Inspection Parameters')
        unique_together = ('service', 'parameter')

    _ori_parameter = None

    service = models.ForeignKey(
        InspectionService,
        related_name='lit_parameters',
        on_delete=models.CASCADE,
        verbose_name=_('Service'))
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE,
        related_name='lit_services',
        verbose_name=_('Parameter'))
    price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Price'))
    date_effective = models.DateField(
        default=timezone.now,
        verbose_name=_('Date effective'))

    def __str__(self):
        return str(self.parameter)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self, 'parameter', False):
            self._ori_parameter = self.parameter

    def clean(self):
        not_adding = self._state.adding is False
        is_changed = self._ori_parameter != self.parameter
        if not_adding and is_changed:
            msg = _("Parameter can't be changed, please delete instead.")
            raise ValidationError({"parameter": msg})
        pass

    def save(self, *args, **kwargs):
        self.clean()
        if not self.price:
            self.price = self.parameter.price
        if not self.date_effective:
            self.date_effective = self.parameter.date_effective
        super().save(*args, **kwargs)


class InspectionOrder(SalesOrder):
    class Meta:
        verbose_name = _('Inspection Order')
        verbose_name_plural = _('Inspection Orders')


class InspectionOrderItem(NumeratorMixin, OrderItemBase):
    class Meta:
        verbose_name = _('Inspection Order Item')
        verbose_name_plural = _('Inspection Order Items')
        ordering = ('product',)
        unique_together = ('order', 'product')

    doc_prefix = 'ILIT'

    order = models.ForeignKey(
        InspectionOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        InspectionService,
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


class InspectionOrderItemExtraParameter(ExtraParameterBase):
    class Meta:
        verbose_name = _('Extra Parameter')
        verbose_name_plural = _('Extra Parameters')
        unique_together = ('order_item', 'parameter')

    order_item = models.ForeignKey(
        InspectionOrderItem,
        related_name='extra_parameters',
        on_delete=models.CASCADE,
        verbose_name=_('Product'))
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE,
        related_name='lit_extra_parameters',
        verbose_name=_('Parameter'))
    
    def get_default_parameters(self):
        return self.order_item.product.lit_parameters


# @receiver(post_save, sender=ServiceParameter)
# def after_save_product_parameter(sender, **kwargs):
#     instance = kwargs.pop('instance', None)
#     instance.product.save()


# @receiver(post_delete, sender=ServiceParameter)
# def after_delete_product_parameter(sender, **kwargs):
#     instance = kwargs.pop('instance', None)
#     instance.product.save()