from django.db import models
from django.utils import translation
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from django_numerators.models import NumeratorMixin

from simpellab.utils.text import number_to_text_id
from simpellab.core.enums import MaxLength
from simpellab.core.models import BaseModel, SimpleBaseModel
from simpellab.modules.partners.models import Partner
from simpellab.modules.products.models import Product, Fee
from simpellab.modules.sales.models.managers import SalesQuotationManager

_ = translation.gettext_lazy


class SalesQuotationTemplate(SimpleBaseModel):
    class Meta:
        verbose_name = _('Sales Quotation (Template)')
        verbose_name_plural = _('Sales Quotations (Templates)')

    name = models.CharField(
        max_length=MaxLength.LONG.value,
        verbose_name=_('Template name'))
    body = models.TextField(
        max_length=MaxLength.RICHTEXT.value,
        verbose_name=_('Quotation body'))

    def __str__(self):
        return self.name


class SalesQuotation(NumeratorMixin, SimpleBaseModel):
    class Meta:
        verbose_name = _('Sales Quotation')
        verbose_name_plural = _('Sales Quotations')
        permissions = (
            ('draft_salesquotation', _('Can draft Sales Quotation')),
            ('trash_salesquotation', 'Can trash Sales Quotation'),
            ('validate_salesquotation', 'Can validate Sales Quotation'),
            ('revision_salesquotation', 'Can revision Sales Quotation'),
            ('apply_salesquotation', 'Can apply Sales Quotation'),
        )

    objects = SalesQuotationManager()

    doc_code = 'SSQ'

    template = models.ForeignKey(
        SalesQuotationTemplate,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Letter Template"))
    title = models.CharField(
        max_length=MaxLength.LONG.value,
        verbose_name=_('Title'))
    description = models.TextField(
        max_length=MaxLength.RICHTEXT.value,
        null=True, blank=True,
        verbose_name=_('Description'))
    due_date = models.DateTimeField(
        verbose_name=_("Due date"))
    customer = models.ForeignKey(
        Partner, on_delete=models.PROTECT,
        verbose_name=_('Customer'))
    total_amount = models.DecimalField(
        default=0, max_digits=15,
        decimal_places=2,
        verbose_name=_('Total Amount'))
    discount_percentage = models.DecimalField(
        default=0, max_digits=15,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ], verbose_name=_('Discount'),
        help_text=_('Discount in percent'))
    discount = models.DecimalField(
        default=0, max_digits=15,
        decimal_places=2,
        verbose_name=_('Total discount'))
    grand_total = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Grand Total'))

    def __str__(self):
        return "{} ({})".format(self.inner_id, self.customer.name)

    @property
    def grand_total_text(self):
        return number_to_text_id(self.grand_total)

    def calc_total_amount(self):
        total_products = self.order_products.aggregate(val=models.Sum('total_price'))['val'] or 0
        total_fees = self.order_fees.aggregate(val=models.Sum('total_fee'))['val'] or 0
        self.total_amount = total_fees + total_products
        return self.total_amount

    def calc_total_discount(self):
        self.discount = ((self.total_amount * self.discount_percentage) / 100)

    def calc_grand_total(self):
        self.grand_total = self.total_amount - self.discount

    def calc_all_total(self):
        self.calc_total_amount()
        self.calc_total_discount()
        self.calc_grand_total()

    def save(self, *args, **kwargs):
        self.calc_all_total()
        self.clean()
        super().save(*args, **kwargs)


class QuotationExtraFee(BaseModel):
    class Meta:
        verbose_name = _('Quotation Fees')
        verbose_name_plural = _('Quotation Fees')
        ordering = ('fee',)
        unique_together = ('quotation', 'fee')

    _ori_fee = None

    quotation = models.ForeignKey(
        SalesQuotation,
        related_name='quotation_fees',
        on_delete=models.CASCADE,
        verbose_name=_('Quotation'))
    fee = models.ForeignKey(
        Fee,
        on_delete=models.PROTECT,
        related_name='quotation_fees')
    amount = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Fee amount'))
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=_('Quantity'),
        validators=[
            MinValueValidator(1, message=_('Minimal value: 1')),
            MaxValueValidator(500, message=_('Maximal value: 500'))
        ])
    total_fee = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Total fee'))
    note = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_('Note'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self, 'fee', None):
            self._ori_fee = self.fee

    def __str__(self):
        return self.fee.name

    def clean(self):
        if self._state.adding is False and self._ori_fee.id != self.fee.id:
            msg = _("Fee can't be changed, please delete instead.")
            raise ValidationError({"fee": msg})

    def save(self, *args, **kwargs):
        self.amount = self.fee.price
        self.total_fee = self.fee.price * self.quantity
        self.clean()
        super().save(*args, **kwargs)


class QuotationProduct(BaseModel):
    class Meta:
        verbose_name = _('Quotation Item')
        verbose_name_plural = _('Quotation Items')
        ordering = ('product',)
        unique_together = ('quotation', 'product')

    _ori_product = None

    quotation = models.ForeignKey(
        SalesQuotation,
        related_name='quotation_products',
        on_delete=models.CASCADE,
        verbose_name=_('Quotation'))
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='quotation_products')
    unit_price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Product price'))
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=_('Quantity'),
        validators=[
            MinValueValidator(1, message=_('Minimal value: 1')),
            MaxValueValidator(500, message=_('Maximal value: 500'))
        ])
    total_price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Total Price'))
    note = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_('Note'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self, 'product', False):
            self._ori_product = self.product

    def __str__(self):
        return self.product.name

    def clean(self):
        # Make sure price don't change directly when tarif price changed
        if self._state.adding is False and self._ori_product.id != self.product.id:
            msg = _("Product can't be changed, please delete instead.")
            raise ValidationError({"product": msg})

    def save(self, *args, **kwargs):
        product = self.product.get_real_instance()
        self.unit_price = product.total_price
        self.total_price = self.unit_price * self.quantity
        self.clean()
        super().save(*args, **kwargs)


class QuotationTerm(BaseModel):
    class Meta:
        verbose_name = _('Quotation Term')
        verbose_name_plural = _('Quotation Terms')

    quotation = models.ForeignKey(
        SalesQuotation,
        related_name='quotation_terms',
        on_delete=models.CASCADE,
        verbose_name=_('Quotation'))
    term = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_('Term'))
    condition = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_('Condition'))

    def __str__(self):
        return self.term




@receiver(post_save, sender=QuotationExtraFee)
def after_save_quotation_fee(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.quotation.save()


@receiver(post_delete, sender=QuotationExtraFee)
def after_delete_quotation_fee(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.quotation.save()


@receiver(post_save, sender=QuotationProduct)
def after_save_quotation_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.quotation.save()


@receiver(post_delete, sender=QuotationProduct)
def after_delete_quotation_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.quotation.save()