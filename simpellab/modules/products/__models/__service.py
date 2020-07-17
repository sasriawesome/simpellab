from django.db import models
from django.utils import translation, timezone
from django.core.validators import ValidationError

from ...core.models import BaseModel
from ..enums import ProductType
from .base import Product, Parameter

_ = translation.gettext_lazy


class ServiceMixin(models.Model):
    class Meta:
        abstract = True

    def get_doc_prefix(self):
        return "%s." % self.product_type

    def get_product_type(self):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        self.product_type = self.get_product_type()
        self.is_stockable = False
        self.is_consumable = False
        self.is_bundle = False
        self.is_sparepart = False
        self.can_be_sold = True
        self.can_be_purchased = True
        super().save(*args, **kwargs)


class ANYService(ServiceMixin, Product):
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def get_product_type(self):
        return ProductType.ANY.name


class KALService(ServiceMixin, Product):
    class Meta:
        verbose_name = _('Calibration')
        verbose_name_plural = _('Calibrations')

    def get_product_type(self):
        return ProductType.KAL.name


class KSLService(ServiceMixin, Product):
    class Meta:
        verbose_name = _('Consultancy')
        verbose_name_plural = _('Consultancies')

    def get_product_type(self):
        return ProductType.KSL.name


class LIBService(ServiceMixin, Product):
    class Meta:
        verbose_name = _('Research and Development')
        verbose_name_plural = _('Research and Developments')

    def get_product_type(self):
        return ProductType.LIB.name


class LATService(ServiceMixin, Product):
    class Meta:
        verbose_name = _('Training')
        verbose_name_plural = _('Trainings')

    def get_product_type(self):
        return ProductType.LAT.name


class PROService(ServiceMixin, Product):
    class Meta:
        verbose_name = _('Product Certification')
        verbose_name_plural = _('Product Certifications')

    def get_product_type(self):
        return ProductType.PRO.name


class LABService(ServiceMixin, Product):
    class Meta:
        verbose_name = _('Laboratory')
        verbose_name_plural = _('Laboratories')

    def get_product_type(self):
        return ProductType.LAB.name

    def get_price(self):
        if not self.parameters.count():
            return 0
        else:
            return sum(map(lambda x: x.price, self.parameters.all()))


class LABParameter(BaseModel):
    class Meta:
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')
        unique_together = ('product', 'parameter')

    _ori_paramater = None

    product = models.ForeignKey(
        LABService,
        related_name='parameters',
        on_delete=models.CASCADE,
        verbose_name=_('Product'))
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE,
        related_name='lab_parameters',
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
            msg = _("Tarif can't be changed, please delete instead.")
            raise ValidationError({"parameter": msg})
        pass

    def save(self, *args, **kwargs):
        self.clean()
        if not self.price:
            self.price = self.parameter.price
        if not self.date_effective:
            self.date_effective = self.parameter.date_effective
        super().save(*args, **kwargs)


class LITService(ServiceMixin, Product):
    class Meta:
        verbose_name = _('Inspection')
        verbose_name_plural = _('Inspections')

    def get_product_type(self):
        return ProductType.LIT.name

    def get_price(self):
        if not self.parameters.count():
            return 0
        else:
            return sum(map(lambda x: x.price, self.parameters.all()))


class LITParameter(BaseModel):
    class Meta:
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')
        unique_together = ('product', 'parameter')

    _ori_paramater = None

    product = models.ForeignKey(
        LITService,
        related_name='parameters',
        on_delete=models.CASCADE,
        verbose_name=_('Product'))
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE,
        related_name='lit_parameters',
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
        return self.parameter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self, 'tarif', False):
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
