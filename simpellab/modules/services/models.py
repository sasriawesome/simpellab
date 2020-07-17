from django.db import models
from django.utils import timezone, translation
from django.core.validators import MinValueValidator
from django_numerators.models import NumeratorMixin

from simpellab.core.models import BaseModel, SimpleBaseModel
from simpellab.core.enums import MaxLength
from simpellab.modules.products.models import Product, UnitOfMeasure

_ = translation.ugettext_lazy


class Service(Product):
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        permissions = (
            ('lock_service', 'Can lock Service'),
            ('unlock_service', 'Can unlock Service'),
            ('export_service', 'Can export Service'),
            ('import_service', 'Can import Service')
        )

    doc_prefix = 'SRV'


class Parameter(NumeratorMixin, SimpleBaseModel):
    class Meta:
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')

    doc_prefix = 'PRM'

    LAB = _('Laboratory')
    LIT = _('Inspection')

    TYPE = (
        ('LAB', _('Laboratory')),
        ('LIT', _('Inspection')),
    )

    ptype = models.CharField(
        max_length=3,
        choices=TYPE,
        default=LAB,
        verbose_name=_('Parameter type'))
    code = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('code'))
    name = models.CharField(
        max_length=MaxLength.LONG.value,
        verbose_name=_('Name'))
    description = models.TextField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_('Description'))
    price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('price'))
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure, on_delete=models.PROTECT,
        verbose_name=_('Unit'))
    date_effective = models.DateField(
        default=timezone.now,
        verbose_name=_('Date effective'))

    def __str__(self):
        return "{} - {}".format(self.ptype, self.name)

    def natural_key(self):
        keys = (self.inner_id,)
        return keys


class LaboratoriumService(Service):
    class Meta:
        verbose_name = _('Laboratorium Service')
        verbose_name_plural = _('Laboratorium Services')
    
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
        verbose_name = _('Laboratorium Service Parameter')
        verbose_name_plural = _('Laboratorium Service Parameters')
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


class CalibrationService(Service):
    class Meta:
        verbose_name = _('Calibration')
        verbose_name_plural = _('Calibration')

    def get_doc_prefix(self):
        return 'KAL'


class ConsultancyService(Service):
    class Meta:
        verbose_name = _('Consultancy')
        verbose_name_plural = _('Consultancies')

    def get_doc_prefix(self):
        return 'KSL'


class ResearchService(Service):
    class Meta:
        verbose_name = _('Research and Development')
        verbose_name_plural = _('Research and Developments')

    def get_doc_prefix(self):
        return 'LIB'


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


class SertificationService(Service):
    class Meta:
        verbose_name = _('Product Sertification')
        verbose_name_plural = _('Product Sertifications')

    def get_doc_prefix(self):
        return 'PRO'


class MiscService(Service):
    class Meta:
        verbose_name = _('Common Service')
        verbose_name_plural = _('Common Services')

    def get_doc_prefix(self):
        return 'LNY'


# @receiver(post_save, sender=ServiceParameter)
# def after_save_product_parameter(sender, **kwargs):
#     instance = kwargs.pop('instance', None)
#     instance.product.save()


# @receiver(post_delete, sender=ServiceParameter)
# def after_delete_product_parameter(sender, **kwargs):
#     instance = kwargs.pop('instance', None)
#     instance.product.save()
