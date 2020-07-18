from django.db import models
from django.db.utils import cached_property
from django.utils import translation, timezone, timesince

from polymorphic.models import PolymorphicModel
from django_numerators.models import NumeratorMixin

from simpellab.core.models import SimpleBaseModel
from simpellab.core.enums import MaxLength
from simpellab.modules.partners.models import Partner
from simpellab.modules.contracts.managers import *

_ = translation.ugettext_lazy

__all__ = [
    'Contract',
    'CustomerContract'
]


class Contract(NumeratorMixin, PolymorphicModel, SimpleBaseModel):
    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

    doc_prefix = 'CTR'

    objects = ContractManager()

    title = models.CharField(
        max_length=MaxLength.TEXT.value,
        verbose_name=_('Title')
        )
    description = models.TextField(
        verbose_name=_('Description')
        )
    issued_at = models.DateField(
        default=timezone.now,
        verbose_name=_('Date issued'),
        help_text=_('Contract cretaed')
        )
    active_at = models.DateField(
        default=timezone.now,
        verbose_name=_('Date start'),
        help_text=_('Contract start')
        )
    expired_at = models.DateField(
        default=timezone.now,
        verbose_name=_('Date end'),
        help_text=_('Contract end')
        )

    @cached_property
    def is_valid(self):
        return str(self.valid_days) == str(translation.gettext('0 minutes'))

    @cached_property
    def valid_days(self):
        time_left = timesince.timeuntil(
            self.expired_at,
            timezone.make_naive(timezone.now())
        )
        return time_left

    def __str__(self):
        return self.inner_id


class CustomerContract(Contract):
    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

    doc_prefix = 'CTRC'

    objects = CustomerContractManager()

    customer = models.ForeignKey(
        Partner, on_delete=models.PROTECT,
        limit_choices_to={'is_customer':True}
    )