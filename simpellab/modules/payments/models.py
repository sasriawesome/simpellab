from django.db import models, transaction
from django.utils import translation, timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django_numerators.models import NumeratorMixin
from polymorphic.models import PolymorphicModel
from simpellab.core.models import BaseModel, SimpleBaseModel
from simpellab.core.enums import MaxLength
from simpellab.modules.partners.models import Partner, BalanceMutation
from simpellab.modules.sales.models import Invoice
from simpellab.modules.payments.enums import PaymentStatus


_ = translation.ugettext_lazy


__all__ = [
    'PaymentMethod',
    'ManualTransferMethod',
    'CashPaymentMethod',
    'CashFlow',
    'Payment',
    'Receipt',
]


class PaymentMethod(PolymorphicModel, BaseModel):
    class Meta:
        verbose_name = _('Method')
        verbose_name_plural = _('Methods')
    
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


class CashPaymentMethod(PaymentMethod):
    class Meta:
        verbose_name = _('Cash Payment')
        verbose_name_plural = _('Cash Payment')


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

    DOWN_PAYMENT = 'DP'
    REPAYMENT = 'RP'
    PAYMENT_TYPES = (
        (DOWN_PAYMENT,_('Down Payment')),
        (REPAYMENT,_('Repayment')),
    )

    partner = models.ForeignKey(
        Partner, 
        on_delete=models.PROTECT
        )
    status = models.CharField(
        max_length=15,
        choices=PaymentStatus.CHOICES,
        default=PaymentStatus.WAITING,
        verbose_name=_('Status'))
    ptype = models.CharField(
        max_length=2,
        choices=PAYMENT_TYPES,
        default=None, null=True, blank=True,
        verbose_name=_('Payment Type'),
        help_text=_('Determine Down Payment or Repayment')
    )
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
    
    date_confirmed = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date confirmed")
    )

    date_rejected = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date rejected")
    )

    date_refunded = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date refunded")
    )

    def __str__(self):
        return self.inner_id

    @property
    def is_waiting(self):
        return self.status == PaymentStatus.WAITING

    @property
    def is_editable(self):
        return self.is_waiting

    @property
    def is_confirmed(self):
        """ Check order status is approved """
        return self.status == PaymentStatus.CONFIRMED

    @property
    def confirm_ignore_condition(self):
        return self.is_confirmed

    @property
    def confirm_valid_condition(self):
        return self.is_waiting 

    def pre_confirm_action(self):
        pass

    def post_confirm_action(self):
        pass
    
    @transaction.atomic
    def confirm(self):
        """ Comfirm valid payment """
        if self.confirm_ignore_condition:
            return
        if self.confirm_valid_condition:
            self.pre_confirm_action()
            self.status = PaymentStatus.CONFIRMED
            self.date_confirmed = timezone.now()
            self.save()
            self.post_confirm_action()
        else:
            raise PermissionError(self.get_status_msg('confirmed'))
    
    @property
    def is_rejected(self):
        """ Check payment status is rejected """
        return self.status == PaymentStatus.REJECTED

    @property
    def reject_ignore_condition(self):
        return self.is_rejected

    @property
    def reject_valid_condition(self):
        return self.is_waiting 

    def pre_reject_action(self):
        pass

    def post_reject_action(self):
        pass
    
    @transaction.atomic
    def reject(self):
        """ Comfirm valid payment """
        if self.reject_ignore_condition:
            return
        if self.reject_valid_condition:
            self.pre_reject_action()
            self.status = PaymentStatus.REJECTED
            self.date_rejected = timezone.now()
            self.save()
            self.post_reject_action()
        else:
            raise PermissionError(self.get_status_msg('rejected'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Payment(CashFlow):
    """ Send cash to partner """
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')


class Refund(CashFlow):
    """ Refund cash to partner """
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')


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

    def pre_confirm_action(self):
        # Use this if you want to prevent confirmation 
        # if receipt amount greater than invoice receivable
        # if self.amount > self.item.receivable:
        #     raise Exception({
        #           'error':_('Receipt amount greater than Invoice receivable amount')
        #         })
        pass

    def post_confirm_action(self):
        if self.amount > self.item.receivable:
            # transfer refundable to partner balance
            refundable_value = self.amount - self.item.receivable
            mutation = BalanceMutation(
                partner=self.partner,
                flow=BalanceMutation.IN,
                amount = refundable_value,
                reference=self.inner_id,
                note='Invoice #%s refund' % self.item.inner_id,
            )
            mutation.save()
            self.item.pay(self.item.receivable, refund=refundable_value)
        else:
            self.item.pay(self.amount)
