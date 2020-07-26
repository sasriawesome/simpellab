import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from polymorphic.models import PolymorphicModel

from sister.core.enums import MaxLength
from sister.core.models import BaseModel, SimpleBaseModel
from sister.modules.kurikulum.models import *
from sister.modules.pembelajaran.models import *
from .managers import PenilaianMataPelajaranManager


__all__ = [
    'BobotPenilaian',
    'Penilaian',
    'PenilaianPembelajaran',
    'ItemPenilaianTugas',
    'ItemPenilaianHarian',
    'ItemPenilaianTengahSemester',
    'ItemPenilaianAkhirSemester',
    'PenilaianEkstraKurikuler'
]


class BobotPenilaian(BaseModel):
    class Meta:
        verbose_name = 'Bobot Penilaian'
        verbose_name_plural = 'Bobot Penilaian'

    mata_pelajaran_kelas = models.OneToOneField(
        MataPelajaranKelas,
        related_name='bobot',
        on_delete=models.CASCADE
    )
    tugas = models.PositiveIntegerField(
        default=10,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Tugas dan Pekerjaan Rumah'
    )
    ph = models.PositiveIntegerField(
        default=20,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Penilaian Harian'
    )
    pts = models.PositiveIntegerField(
        default=30,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Penilaian Tengah Semester'
    )
    pas = models.PositiveIntegerField(
        default=40,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Penilaian Akhir Semester'
    )
    kkm = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Kriteria Ketuntasan Minimal'
    )

    @property
    def total(self):
        total_bobot = (
            self.tugas 
            + self.ph 
            + self.pts 
            + self.pas)
        return total_bobot

    def clean(self):
        
        if self.total != 100:
            raise ValidationError({'mata_pelajaran_kelas':'Total bobot harus berjumlah 100'})

    def __str__(self):
        return str(self.mata_pelajaran_kelas)


class Penilaian(PolymorphicModel, BaseModel):
    class Meta:
        verbose_name = _('Penilaian')
        verbose_name_plural = _('Penilaian')

    siswa = models.ForeignKey(
        SiswaKelas, 
        on_delete=models.CASCADE
    )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    nilai = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


class PenilaianPembelajaran(Penilaian):
    class Meta:
        verbose_name = _('Penilaian Pembelajaran')
        verbose_name_plural = _('Penilaian Pembelajaran')

    mata_pelajaran = models.ForeignKey(
        MataPelajaranKelas,
        on_delete=models.CASCADE,
        related_name='penilaian'
    )


class ItemPenilaianTugas(BaseModel):
    class Meta:
        verbose_name = _('Penilaian Tugas')
        verbose_name_plural = _('Penilaian Tugas')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='tugas'
    )
    kompetensi_dasar = models.ForeignKey(
        KompetensiDasar,
        on_delete=models.PROTECT,
        related_name='tugas'
    )
    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


class ItemPenilaianHarian(BaseModel):
    class Meta:
        verbose_name = _('Penilaian Harian')
        verbose_name_plural = _('Penilaian Harian')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='harian'
    )
    kompetensi_dasar = models.ForeignKey(
        KompetensiDasar,
        on_delete=models.PROTECT,
        related_name='harian'
    )
    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


class ItemPenilaianTengahSemester(BaseModel):
    class Meta:
        verbose_name = _('Penilaian Tengah Semester')
        verbose_name_plural = _('Penilaian Tengah Semester')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='tengah_semester'
    )
    kompetensi_dasar = models.ForeignKey(
        KompetensiDasar,
        on_delete=models.PROTECT,
        related_name='tengah_semester'
    )
    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


class ItemPenilaianAkhirSemester(BaseModel):
    class Meta:
        verbose_name = _('Penilaian Akhir Semester')
        verbose_name_plural = _('Penilaian Akhir Semester')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='akhir_semester'
    )
    kompetensi_dasar = models.ForeignKey(
        KompetensiDasar,
        on_delete=models.PROTECT,
        related_name='akhir_semester'
    )
    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


class PenilaianEkstraKurikuler(Penilaian):
    class Meta:
        verbose_name = 'Penilaian Ekstra Kurikuler'
        verbose_name_plural = 'Penilaian Ekstra Kurikuler'

    ekskul = models.ForeignKey(
        EkstraKurikuler,
        editable=True,
        on_delete=models.CASCADE,
        related_name='penilaian'
        )
