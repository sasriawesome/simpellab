from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import translation, timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from django_numerators.models import NumeratorMixin
from django_qrcodes.models import QRCodeMixin
from polymorphic.models import PolymorphicModel

from simpellab.utils.text import number_to_text_id
from simpellab.core.enums import MaxLength, Status
from simpellab.core.models import BaseModel, SimpleBaseModel
from simpellab.core.mixins import ThreeStepStatusMixin, StatusMixin, PaidMixin, TrashMixin, CloseMixin
from simpellab.modules.partners.models import Partner
from simpellab.modules.products.enums import ProductType
from simpellab.modules.products.models import Fee, Product
from simpellab.modules.sales.managers import SalesOrderManager


_ = translation.gettext_lazy

__all__ = [
    'SalesOrder', # Base Class
    'OrderItem', # Base Class
    'OrderItemParameter',
    'OrderFee',
    'CommonOrder',
    'CommonOrderItem',
    'Invoice'
]


class InvoiceStatusMixin(
        TrashMixin,
        PaidMixin,
        CloseMixin,
        StatusMixin):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.status = Status.PENDING.value
        super().save(*args, **kwargs)


class SalesOrder(NumeratorMixin, ThreeStepStatusMixin, PolymorphicModel, SimpleBaseModel):
    class Meta:
        verbose_name = _('Sales Order')
        verbose_name_plural = _('Sales Orders')
        permissions = (
            ('draft_salesorder', _('Can draft Sales Order')),
            ('trash_salesorder', 'Can trash Sales Order'),
            ('validate_salesorder', 'Can validate Sales Order'),
            ('complete_salesorder', 'Can complete Sales Order'),
        )

    doc_prefix = 'SPJ'
    parent_prefix = True
    parent_model = 'simpellab_sales.SalesOrder'

    contract = models.BooleanField(
        default=False,
        help_text=_('This order is based on customer contract')
        )
    contract_number = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_('Contract number')
    )
    customer = models.ForeignKey(
        Partner, on_delete=models.PROTECT,
        limit_choices_to={'is_customer':True},
        verbose_name=_('Customer'))
    customer_po = models.CharField(
        max_length=MaxLength.LONG.value,
        null=True, blank=True,
        verbose_name=_('Customer PO'))
    note = models.CharField(
        max_length=MaxLength.LONG.value,
        null=True, blank=True,
        verbose_name=_("Note"))
    total_order = models.DecimalField(
        default=0, max_digits=15,
        decimal_places=2,
        verbose_name=_('Total Order'))
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
        return "{}".format(self.inner_id)

    @property
    def grand_total_text(self):
        return number_to_text_id(self.grand_total)

    def get_order_items(self):
        """ Get child object order_items """
        raise NotImplementedError(
                ('SalesOrder subclass %s should implement' 
                + ' get_order_items() that '
                + 'return order_items queryset') % self.__class__.__name__)

    def calc_total_products(self):
        total_products = self.get_order_items().aggregate(
                val=models.Sum('total_price')
            )['val'] or 0
        return total_products

    def calc_total_fees(self):
        total_fees = self.order_fees.aggregate(
                val=models.Sum('total_fee')
            )['val'] or 0
        return total_fees

    def calc_total_order(self):
        total_products = self.calc_total_products()
        total_fees = self.calc_total_fees()
        print(total_fees)
        self.total_order = total_fees + total_products
        return self.total_order

    def calc_total_discount(self):
        self.discount = ((self.total_order * self.discount_percentage) / 100)

    def calc_grand_total(self):
        self.grand_total = self.total_order - self.discount

    def calc_all_total(self):
        self.calc_total_order()
        self.calc_total_discount()
        self.calc_grand_total()

    def save(self, *args, **kwargs):
        self.calc_all_total()
        self.clean()
        super().save(*args, **kwargs)


class OrderFee(BaseModel):
    class Meta:
        verbose_name = _('Order Fees')
        verbose_name_plural = _('Order Fees')
        ordering = ('fee',)
        unique_together = ('order', 'fee')

    _ori_fee = None

    order = models.ForeignKey(
        SalesOrder,
        related_name='order_fees',
        on_delete=models.CASCADE,
        verbose_name=_('Order'))
    fee = models.ForeignKey(
        Fee,
        on_delete=models.PROTECT,
        related_name='order_fees')
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
        # Make sure price don't change directly when tarif price changed
        if self._state.adding is False and self._ori_fee.id != self.fee.id:
            msg = _("Fee can't be changed, please delete instead.")
            raise ValidationError({"fee": msg})

    def save(self, *args, **kwargs):
        self.amount = self.fee.price
        self.total_fee = self.fee.price * self.quantity
        self.clean()
        super().save(*args, **kwargs)


class OrderItem(NumeratorMixin, PolymorphicModel, SimpleBaseModel):
    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        ordering = ('created_at',)

    _ori_product = None

    name = models.CharField(
        null=True, blank=False,
        max_length=MaxLength.LONG.value,
        verbose_name=_('Name'))
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
        return str(self.inner_id)

    def clean(self):
        not_adding = self._state.adding is False
        if self._ori_product:
            is_changed = self._ori_product.id != self.product.id
        else:
            is_changed = False
        if not_adding and is_changed:
            msg = _("Product can't be changed, please delete instead.")
            raise ValidationError({"product": msg})
        super().clean()

    def calculate_unit_price(self):
        unit_price = self.product.get_real_instance().total_price
        return unit_price

    def save(self, *args, **kwargs):
        self.unit_price = self.calculate_unit_price()
        self.total_price = self.quantity * self.unit_price
        self.clean()
        super().save(*args, **kwargs)


class CommonOrder(SalesOrder):
    class Meta:
        verbose_name = _('Common Order')
        verbose_name_plural = _('Common Orders')

    def get_order_items(self):
        """ Get child object order_items """
        return self.order_items


class CommonOrderItem(OrderItem):
    class Meta:
        verbose_name = _('Common Order Item')
        verbose_name_plural = _('Common Order Items')
        
    doc_prefix = 'SOI'
    order = models.ForeignKey(
        CommonOrder,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_('sales order'))
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='sales_orders')


class OrderItemParameter(BaseModel):
    class Meta:
        abstract = True

    _ori_parameter = None

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
        # Prevent parameter change
        if getattr(self, 'parameter', None):
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


class Invoice(QRCodeMixin, NumeratorMixin, InvoiceStatusMixin, SimpleBaseModel):
    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')

    sales_order = models.OneToOneField(
        SalesOrder,
        on_delete=models.PROTECT,
        verbose_name=_('sales order'))
    billed_to = models.ForeignKey(
        Partner, null=True, blank=False,
        editable=False,
        limit_choices_to={'is_customer':True},
        on_delete=models.PROTECT, 
        verbose_name=_('Customer')
        )
    due_date = models.DateTimeField(
        default=timezone.now, verbose_name=_('Due date'))
    description = models.TextField(
        max_length=MaxLength.TEXT.value,
        blank=True, null=True, verbose_name=_('Description'))
    total_order = models.DecimalField(
        default=0, max_digits=15,
        decimal_places=2,
        verbose_name=_('Total Order'))
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
    downpayment = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('down payment'))
    repayment = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('repayment'))
    paid = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('paid'))
    receivable = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('receivable'))
    refund = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('refund'))

    @property
    def is_payment_complete(self):
        return self.grand_total == self.paid

    @property
    def close_ignore_condition(self):
        return self.is_closed

    @property
    def close_valid_condition(self):
        return self.is_paid and self.grand_total == self.paid

    def save(self, *args, **kwargs):
        self.billed_to = self.sales_order.customer
        super().save(*args, **kwargs)


@receiver(post_save, sender=OrderFee)
def after_save_order_fee(sender, **kwargs):
    print('save orderfee')
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_delete, sender=OrderFee)
def after_delete_order_fee(sender, **kwargs):
    print('delete orderfee')
    instance = kwargs.pop('instance', None)
    instance.order.get_real_instance().save()


@receiver(post_save, sender=CommonOrderItem)
def after_save_common_item(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_delete, sender=CommonOrderItem)
def after_delete_common_item(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()