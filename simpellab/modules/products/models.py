import uuid
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils import translation, timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

from taggit.models import TaggedItemBase, TagBase
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey
from polymorphic.models import PolymorphicModel
from django_numerators.models import NumeratorMixin

from simpellab.core.enums import MaxLength
from simpellab.core.models import BaseModel, SimpleBaseModel
from simpellab.core.managers import BasePolymorphicManager
from simpellab.utils.slugify import unique_slugify
from simpellab.modules.partners.models import Partner
from simpellab.modules.products.mixins import SellableMixin, StockableMixin

_ = translation.gettext_lazy


__all__ = [
    'UnitOfMeasure',
    'Fee',
    'Category',
    'Parameter',
    'Tag',
    'Product',
    'TaggedProduct',
    'Specification',
    'ProductFee',
    'Inventory',
    'Asset',
    'Service'
]


class SnippetBaseManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class SnippetBase(SimpleBaseModel):
    """ Base snippet """

    class Meta:
        abstract = True

    objects = SnippetBaseManager()

    name = models.CharField(
        max_length=255,
        unique=True, verbose_name=_('Name'))
    description = models.TextField(
        null=True, blank=True,
        max_length=512,
        verbose_name=_('Description'))

    def __str__(self):
        return self.name

    def natural_key(self):
        key = (self.name,)
        return key


class UnitOfMeasure(SnippetBase):
    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')


class Fee(NumeratorMixin, SimpleBaseModel):
    class Meta:
        verbose_name = _('Fee')
        verbose_name_plural = _('Fees')

    doc_prefix = 'EXT'

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
        verbose_name=_('Price'))
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure, on_delete=models.PROTECT,
        verbose_name=_('Unit'))
    date_effective = models.DateField(
        default=timezone.now,
        verbose_name=_('Date effective'))

    def __str__(self):
        return self.name

    def natural_key(self):
        keys = (self.inner_id,)
        return keys


class Category(BaseModel, MPTTModel):
    class Meta:
        ordering = ['name']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    parent = TreeForeignKey(
        'self', blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name="children",
        help_text=_(
            'Categories, unlike tags, can have a hierarchy. You might have a '
            'Jazz category, and under that have children categories for Bebop'
            ' and Big Band. Totally optional.'), )
    name = models.CharField(
        max_length=80,
        unique=True,
        verbose_name=_('Category Name'))
    slug = models.SlugField(
        unique=True,
        max_length=80,
        null=True,
        blank=True)
    description = models.TextField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_('Description'))

    def __str__(self):
        return self.name

    @property
    def opts(self):
        return self._meta

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError('Parent category cannot be self.')
            if parent.parent and parent.parent == self:
                raise ValidationError('Cannot have circular Parents.')

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        return super().save(*args, **kwargs)


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


class Tag(TagBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    @property
    def opts(self):
        return self._meta


class Product(NumeratorMixin, SimpleBaseModel, PolymorphicModel):
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        permissions = (
            ('lock_product', 'Can lock Product'),
            ('unlock_product', 'Can unlock Product'),
            ('export_product', 'Can export Product'),
            ('import_product', 'Can import Product')
        )

    objects = BasePolymorphicManager()

    name = models.CharField(
        verbose_name=_('name'),
        max_length=255)
    alias_name = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name=_('Alias name'))
    slug = models.SlugField(
        unique=True, null=True, blank=True,
        editable=False, max_length=80)
    description = models.TextField(
        null=True, blank=True,
        max_length=1000,
        verbose_name=_('Description'))
    category = models.ForeignKey(
        Category, related_name='products',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_("Category"))
    tags = TaggableManager(
        through='TaggedProduct',
        blank=True,
        related_name='products',
        verbose_name=_("Tags"))
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure,
        null=True, blank=False,
        on_delete=models.PROTECT,
        verbose_name=_('Unit'))
    price = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        verbose_name=_("price"))
    fee = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        verbose_name=_("fee"))
    total_price = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        verbose_name=_("total price"))
    suppliers = models.ManyToManyField(
        Partner, related_name='products', blank=True,
        limit_choices_to={'is_supplier':True},
        verbose_name=_('Suppliers'))
    is_locked = models.BooleanField(
        default=False,
        editable=False,
        verbose_name=_("Locked"),
        help_text=_("Lock to prevent unwanted editing"))
    is_active = models.BooleanField(
        default=True,
        editable=False,
        verbose_name=_("Active"),
        help_text=_("Deletion is not good, set to inactive instead"))

    @property
    def opts(self):
        return self.get_real_instance_class()._meta

    def __str__(self):
        return "{} - {}".format(self.inner_id, self.name)

    def natural_key(self):
        keys = (self.inner_id,)
        return keys

    def get_public_url(self):
        return self.get_absolute_url()

    def lock(self):
        if not self.is_locked:
            self.is_locked = True
            self.save()

    def unlock(self):
        if self.is_locked:
            self.is_locked = False
            self.save()

    def get_fee(self):
        if not self.product_fees.count():
            return 0
        else:
            return sum(map(lambda x: x.price, self.product_fees.all()))

    def get_price(self):
        return self.price

    def get_total_price(self):
        return self.price + self.fee

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        self.fee = self.get_fee()
        self.price = self.get_price()
        self.total_price = self.get_total_price()
        super().save(**kwargs)


class TaggedProduct(TaggedItemBase):
    class Meta:
        verbose_name = _("Tagged")
        verbose_name_plural = _("Taggeds")

    content_object = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='tagged_products')
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE,
        related_name="tagged_products")

    def __str__(self):
        return self.tag


class Specification(BaseModel):
    class Meta:
        verbose_name = _("Specification")
        verbose_name_plural = _("Specifications")
        unique_together = ('product', 'feature')

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='specifications',
        verbose_name=_("Product"))
    feature = models.CharField(
        max_length=255, verbose_name=_("Feature"))
    description = models.TextField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_('Description'))
    value = models.CharField(
        max_length=255, verbose_name=_("Value"))
    note = models.CharField(
        null=True, blank=True,
        max_length=255, verbose_name=_("Note"))

    def __str__(self):
        return "{} ({})".format(self.product.name, self.feature.name)


class ProductFee(BaseModel):
    class Meta:
        verbose_name = _('Product Fee')
        verbose_name_plural = _('Product Fees')
        unique_together = ('product', 'fee')

    _ori_fee = None

    product = models.ForeignKey(
        Product,
        related_name='product_fees',
        on_delete=models.CASCADE,
        verbose_name=_('Product'))
    fee = models.ForeignKey(
        Fee, on_delete=models.CASCADE,
        related_name='product_fees',
        verbose_name=_('Fee'))
    price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Price'))
    date_effective = models.DateField(
        default=timezone.now,
        verbose_name=_('Date effective'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self, 'fee', False):
            self._ori_fee = self.fee

    def __str__(self):
        return self.fee.name

    def clean(self):
        if self._state.adding is False and self._ori_fee != self.fee:
            msg = _("Fee can't be changed, please delete instead.")
            raise ValidationError({"fee": msg})
        pass

    def save(self, *args, **kwargs):
        self.clean()
        if not self.price:
            self.price = self.fee.price
        if not self.date_effective:
            self.date_effective = self.fee.date_effective
        super().save(*args, **kwargs)


class Inventory(StockableMixin, SellableMixin, Product):
    class Meta:
        verbose_name = _('Inventory')
        verbose_name_plural = _('Inventories')
        permissions = (
            ('lock_inventory', 'Can lock Inventory'),
            ('unlock_inventory', 'Can unlock Inventory'),
            ('export_inventory', 'Can export Inventory'),
            ('import_inventory', 'Can import Inventory')
        )

    def get_doc_prefix(self):
        return 'INV'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Asset(StockableMixin, Product):
    class Meta:
        verbose_name = _('Asset')
        verbose_name_plural = _('Assets')
        permissions = (
            ('lock_asset', 'Can lock Asset'),
            ('unlock_asset', 'Can unlock Asset'),
            ('export_asset', 'Can export Asset'),
            ('import_asset', 'Can import Asset')
        )

    def get_doc_prefix(self):
        return 'AST'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


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

    def get_doc_prefix(self):
        return 'SRV'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


@receiver(post_save, sender=ProductFee)
def after_save_product_fee(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.product.save()


@receiver(post_delete, sender=ProductFee)
def after_delete_product_fee(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.product.save()