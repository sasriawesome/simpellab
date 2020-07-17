from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django.conf import settings

from django_numerators.models import NumeratorMixin
from simpellab.core.models import SimpleBaseModel
from simpellab.core.managers import BaseManager
from simpellab.auth.models import AddressAbstract, ContactAbstract


class PartnerManager(BaseManager):
    def get_queryset(self):
        return super().get_queryset()

    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)


class Partner(NumeratorMixin, SimpleBaseModel):
    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')
        permissions = (
            ('export_partner', 'Can export Partner'),
            ('import_partner', 'Can import Partner')
        )

    doc_code = 'PRT'
    objects = PartnerManager()
    name = models.CharField(
        max_length=255, verbose_name=_('Partner name'),
        help_text=_('Partner name eg. Google .Inc or person name if partner is personal'))
    is_company = models.BooleanField(
        default=True, verbose_name=_("Company"))
    is_customer = models.BooleanField(
        default=False, verbose_name=_("Customer"))
    is_supplier = models.BooleanField(
        default=False, verbose_name=_("Supplier"))
    is_active = models.BooleanField(
        default=True, verbose_name=_("Active"))
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        related_name='partner',
        on_delete=models.CASCADE,
        verbose_name=_('User account'))

    @cached_property
    def full_address(self):
        address = self.get_primary_address
        if address:
            line1 = []
            if address.street1:
                line1.append(address.street1)
            line2 = []
            if address.street2:
                line2.append(address.street2)
            if address.city:
                line2.append(address.city)
            line3 = []
            if address.province:
                line3.append(address.province)
            if address.country:
                line3.append(address.country)
            if address.zipcode:
                line3.append(address.zipcode)

            line1 = " ".join(line1)
            line2 = ", ".join(line2)
            line3 = ", ".join(line3)
            return line1, line2, line3
        return None

    @cached_property
    def full_contactinfo(self):
        contact = self.get_contact_info
        text = []
        text2 = []
        if contact.phone1:
            text.append('Phone: %s' % contact.phone)
        if contact.fax:
            text.append('Fax: %s' % contact.fax)
        if contact.whatsapp:
            text.append('WA: %s' % contact.whatsapp)
        if contact.email:
            text2.append('Email: %s' % contact.email)
        if contact.website:
            text2.append('Website: %s' % contact.website)
        return ", ".join(text), ", ".join(text2)

    def __str__(self):
        return self.name

    @cached_property
    def get_primary_address(self):
        address_set = getattr(self, 'partneraddress_set', None)
        primaries = address_set.filter(is_primary=True)
        return None if not primaries else primaries[0]

    def natural_key(self):
        key = (self.inner_id,)
        return key


class PartnerContact(ContactAbstract):
    class Meta:
        verbose_name = _('Partner Contact')
        verbose_name_plural = _('Partner Contacts')

    privacy = None # remove name from contact abstract
    partner = models.OneToOneField(
        Partner, on_delete=models.CASCADE,
        related_name='contact',
        verbose_name=_('Partner'))


class PartnerAddress(AddressAbstract):
    class Meta:
        verbose_name = _('Partner Address')
        verbose_name_plural = _('Partner Addresses')

    name = None  # remove name from address abstract
    title = None # remove name from address abstract
    privacy = None # remove name from address abstract
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name=_('Partner'))

    def __str__(self):
        return str(self.partner)

    @cached_property
    def verbose_name(self):
        return "Address %s" % str(self.partner)

class ContactPerson(SimpleBaseModel):
    class Meta:
        verbose_name = _('Contact Person')
        verbose_name_plural = _('Contact Persons')

    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE,
        related_name='contact_persons',
        verbose_name=_('Partner'))
    name = models.CharField(
        null=False, blank=False,
        max_length=255,
        verbose_name=_("Name"))
    phone = models.CharField(
        null=False, blank=False,
        max_length=255,
        verbose_name=_("Phone"))
    email = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_("Email"))
    department = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_("Department"))

    def __str__(self):
        return self.name
