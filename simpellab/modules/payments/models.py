from django.db import models
from django.utils import translation, timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django_numerators.models import NumeratorMixin
from polymorphic.models import PolymorphicModel
from simpellab.core.models import BaseModel, SimpleBaseModel
from simpellab.core.enums import MaxLength
from simpellab.modules.partners.models import Partner
from simpellab.modules.sales.models import Invoice
from simpellab.modules.payments.enums import PaymentStatus


_ = translation.ugettext_lazy


__all__ = [
    'PaymentMethod',
    'ManualTransferMethod',
    'CashFlow',
    'Payment',
    'Receipt',
]


class PaymentMethod(PolymorphicModel, BaseModel):
    class Meta:
        verbose_name = _('Payment Method')
        verbose_name_plural = _('Payment Methods')
    
    PERCENT = 'PERCENT'
    NOMINAL = 'NOMINAL'

    RATE_METHOD = (
        (PERCENT, _('Percentage')),
        (NOMINAL, _('Nominal'))
    )

    name = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name = _('Name')
        )
    rate_method = models.CharField(
        max_length=MaxLength.SHORT.value,
        default=PERCENT,
        choices=RATE_METHOD,
        verbose_name=_('Rate method')
    )
    transfer_fee = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, validators=[
            MinValueValidator(0)
        ],
        verbose_name=_('Transfer fee')
        )
    auto_confirm = models.BooleanField(
        default=False,
        verbose_name=_('Auto confirmation'),
        help_text=_('Customer should inform payment manual if false')
        )

    def __str__(self):
        return self.name

    def receive_payment(self):
        """ Receive payment will create Payment"""
        raise NotImplementedError('%s must implement make_payment method')

    def clean(self):
        if self.rate_method == PaymentMethod.PERCENT and self.transfer_fee > 100:
            raise ValidationError({'transfer_fee': _('%s is not valid percent number') % self.transfer_fee })

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class CashOnDelivery(PaymentMethod):
    class Meta:
        verbose_name = _('Cash on Delivery')
        verbose_name_plural = _('Manual Transfers')


class ManualTransferMethod(PaymentMethod):
    class Meta:
        verbose_name = _('Manual Transfer')
        verbose_name_plural = _('Manual Transfers')

    bank_name = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name = _('Bank Name')
        )
    bank_branch_office = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name = _('Branch Office')
        )
    bank_account = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name = _('Account number')
        )
    bank_holder_name = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name = _('Account holder')
        )


class CashFlow(PolymorphicModel, NumeratorMixin, SimpleBaseModel):
    class Meta:
        verbose_name = _('Cash Flow')
        verbose_name_plural = _('Cash Flows')

    partner = models.ForeignKey(
        Partner, 
        on_delete=models.PROTECT
        )
    status = models.CharField(
        max_length=15,
        choices=PaymentStatus.CHOICES,
        default=PaymentStatus.WAITING,
        verbose_name=_('Status'))
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
        verbose_name=_('Payment method')
        )
    amount = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Amount'))
    memo = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_('Memo'))

    def __str__(self):
        return self.inner_id

    @property
    def is_editable(self):
        return self.status == PaymentStatus.WAITING
    
    def calc_amount(self):
        total = self.payment_items.aggregate(
            total=models.Sum('amount')
            )['total']
        return total or 0

    def get_items(self):
        print('get payment items')

    def confirm(self):
        print('confirming payment')
    
    def reject(self):
        print('rejecting payment')

    def refund(self):
        print('make refund')

    def save(self, *args, **kwargs):
        self.amount = self.calc_amount()
        super().save(*args, **kwargs)


class Payment(CashFlow):
    """ Send cash to partner """
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def get_items(self):
        print('get payment items')

    def confirm(self):
        print('confirming payment')
    
    def reject(self):
        print('rejecting payment')

    def refund(self):
        print('refund payment')


class Receipt(CashFlow):
    """ Receive cash from partner """
    class Meta:
        verbose_name = _('Receipt')
        verbose_name_plural = _('Receipts')

    item = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        verbose_name=_('Item')
    )

    def __str__(self):
        return self.inner_id
    
    def get_items(self):
        print('get receipt items')

    def confirm(self):
        print('confirming receipt')
    
    def reject(self):
        print('rejecting receipt')

    def refund(self):
        print('refund receipt')