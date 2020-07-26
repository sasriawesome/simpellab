import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from django_personals.models import AddressAbstract, ContactAbstract
from django_personals.enums import Gender, AddressName

from sister.core.enums import MaxLength
from sister.core.models import BaseModel, SimpleBaseModel
from sister.modules.personal.managers import PersonManager


__all__ = [
    'Person',
    'PersonAddress',
    'PersonContact',
    'Guru',
    'Wali',
    'Siswa'
]


class Person(BaseModel):
    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        permissions = (
            ('export_person', 'Can export Person'),
            ('import_person', 'Can import Person'),
            ('change_status_person', 'Can change status Person')
        )

    objects = PersonManager()

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name='profile',
        on_delete=models.CASCADE,
        verbose_name=_('User account'))
    full_name = models.CharField(_('full name'), max_length=30, blank=False)
    short_name = models.CharField(_('short name'), max_length=150, blank=True)
    title = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("Title"))
    pid = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("PID"),
        help_text=_('Personal Identifier Number'))
    gender = models.CharField(
        max_length=1,
        choices=Gender.CHOICES.value,
        default=Gender.MALE.value,
        verbose_name=_('gender'))
    date_of_birth = models.DateField(
        null=True, blank=True,
        default=timezone.now,
        verbose_name=_('date of birth'))
    place_of_birth = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('place of birth'))

    def __str__(self):
        return self.full_name


class ContactAbstract(BaseModel):
    class Meta:
        abstract = True

    phone = models.CharField(
        max_length=MaxLength.SHORT.value,
        null=True, blank=True,
        verbose_name=_('phone'))
    fax = models.CharField(
        max_length=MaxLength.SHORT.value,
        null=True, blank=True,
        verbose_name=_('fax'))
    email = models.CharField(
        max_length=MaxLength.SHORT.value,
        null=True, blank=True,
        verbose_name=_('email'),
        help_text=_('your public email'))
    whatsapp = models.CharField(
        max_length=MaxLength.SHORT.value,
        null=True, blank=True,
        verbose_name=_('whatsapp'))
    website = models.CharField(
        max_length=MaxLength.SHORT.value,
        null=True, blank=True,
        verbose_name=_('website'))


class AddressAbstract(BaseModel):

    class Meta:
        abstract = True

    is_primary = models.BooleanField(
        default=True, verbose_name=_('primary'))
    name = models.CharField(
        null=True, blank=False,
        max_length=MaxLength.MEDIUM.value,
        choices=AddressName.CHOICES.value,
        default=AddressName.HOME.value,
        verbose_name=_("name"),
        help_text=_('E.g. Home Address or Office Address'))
    street = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_('street'))
    city = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('city'))
    province = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('province'))
    country = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('country'))
    zipcode = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('zip code'))

    def __str__(self):
        return self.street

    @property
    def fulladdress(self):
        address = [self.street, self.city, self.province, self.country, self.zipcode]
        return ", ".join(map(str, address))


class PersonContact(ContactAbstract):
    class Meta:
        verbose_name = _('Person address')
        verbose_name_plural = _('Person addresses')

    person = models.OneToOneField(
        Person, on_delete=models.CASCADE)


class PersonAddress(AddressAbstract):

    class Meta:
        verbose_name = _('Person address')
        verbose_name_plural = _('Person addresses')

    person = models.ForeignKey(
        Person, on_delete=models.CASCADE,
        related_name='addresses'
    )


class Guru(BaseModel):
    class Meta:
        verbose_name = 'Guru'
        verbose_name_plural = 'Guru'

    person = models.ForeignKey(
        Person,
        null=True, blank=True,
        on_delete=models.CASCADE)
    nip = models.CharField(max_length=25)

    def __str__(self):
        return "%s" % self.person

    def get_jadwal(self, current_day=True):
        from sister.modules.pembelajaran.models import ItemJadwalPelajaran
        mapel = self.mata_pelajaran.all()
        filters = {
                'mata_pelajaran_kelas__in':[ x.id for x in mapel],
            }
        if current_day:
            filters['hari'] = timezone.now().weekday()
        return ItemJadwalPelajaran.objects.annotate(
                kelas = models.F('jadwal_pelajaran__kelas'),
                hari = models.F('jadwal_pelajaran__hari')
            ).filter(**filters)


class Wali(BaseModel):
    class Meta:
        verbose_name = 'Wali'
        verbose_name_plural = 'Wali'

    STATUS = (
        (1, 'Ayah'),
        (2, 'Ibu'),
        (3, 'Paman'),
        (4, 'Bibi'),
        (5, 'Kakek'),
        (6, 'Nenek'),
        (99, 'Lainnya'),
    )

    person = models.ForeignKey(
        Person,
        null=True, blank=True,
        on_delete=models.CASCADE)
    status = models.IntegerField(
        choices=STATUS,
        default=1
    )
    status_lain = models.CharField(max_length=56, null=True, blank=True)

    def __str__(self):
        return "%s" % self.person


class Siswa(BaseModel):
    class Meta:
        verbose_name = 'Siswa'
        verbose_name_plural = 'Siswa'

    person = models.ForeignKey(
        Person,
        null=True, blank=True,
        on_delete=models.CASCADE)
    wali = models.ForeignKey(
        Wali,
        on_delete=models.CASCADE)
    nis = models.CharField(max_length=25, null=True, blank=False)
    nisn = models.CharField(max_length=25, null=True, blank=False)
    status = models.IntegerField(
        choices=(
            (1, 'Aktif'),
            (2, 'Alumni'),
            (3, 'Drop Out'),
            (99, 'Lainnya'),
        ),
        default=1
    )
    status_lain = models.CharField(max_length=56, null=True, blank=True)

    def __str__(self):
        return "%s" % self.person
