import uuid
import decimal
from django.db import models
from django.db.utils import cached_property
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone, translation
from django.core.validators import MinValueValidator, MaxValueValidator

from sister.core.models import BaseModel
from sister.modules.ruang.models import Ruang
from sister.modules.personal.models import Guru, Siswa
from sister.modules.kurikulum.models import TahunAjaran, Kurikulum, MataPelajaranKurikulum, EkstraKurikuler


__all__ = [
    'Kelas',
    'SiswaKelas',
    'RentangNilai',
    'MataPelajaranKelas',
    'JadwalKelas',
    'ItemJadwalPelajaran',
    'ItemJadwalEkstraKurikuler',
    'PresensiSiswa',
    'ItemPresensiSiswa',
    'PiketKelas',
    'ItemPiketKelas'
]

_ = translation.ugettext_lazy


class Kelas(BaseModel):
    class Meta:
        verbose_name = 'Kelas'
        verbose_name_plural = 'Kelas'

    nama_kelas = models.CharField(max_length=225)
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    guru_kelas = models.ForeignKey(
        Guru, 
        on_delete=models.CASCADE,
        related_name='kelas'
        )
    kurikulum = models.ForeignKey(Kurikulum, on_delete=models.CASCADE)
    ruang = models.ForeignKey(
        Ruang, null=True, blank=False,
        on_delete=models.PROTECT,
        related_name='ruang')
    status = models.CharField(
        max_length=10,
        choices=(
            ('PENDING', 'Pending'),
            ('AKTIF', 'Aktif'),
            ('SELESAI', 'Selesai'),
        ),
        default='PENDING'
    )

    def __str__(self):
        return "%s %s" % (self.nama_kelas, self.tahun_ajaran)

    def get_jadwal_pelajaran(self, current_day=True):
        mapel = self.mata_pelajaran.all()
        filters = {
                'kelas': self.id,
            }
        if current_day:
            filters['hari'] = timezone.now().weekday()
        return ItemJadwalPelajaran.objects.annotate(
                kelas = models.F('jadwal_kelas__kelas'),
                hari = models.F('jadwal_kelas__hari')
            ).filter(**filters)

    def get_jadwal_ekskul(self, current_day=True):
        filters = {
                'kelas': self.id,
            }
        if current_day:
            filters['hari'] = timezone.now().weekday()
        return ItemJadwalEkstraKurikuler.objects.annotate(
                kelas = models.F('jadwal_kelas__kelas'),
                hari = models.F('jadwal_kelas__hari')
            ).filter(**filters)

class SiswaKelas(BaseModel):
    class Meta:
        verbose_name = 'Siswa Kelas'
        verbose_name_plural = 'Siswa Kelas'
        unique_together = ('siswa', 'kelas')

    siswa = models.ForeignKey(
        Siswa, related_name='kelas',
        on_delete=models.CASCADE
        )
    kelas = models.ForeignKey(
        Kelas, related_name='siswa',
        on_delete=models.CASCADE
        )
    status = models.IntegerField(
        choices=(
            (1, 'Baru'),
            (2, 'Tinggal Kelas'),
            (99, 'Lainnya'),
        ),
        default=1
    )
    status_lain = models.CharField(max_length=56, null=True, blank=True)

    def __str__(self):
        return "%s" % self.siswa


class RentangNilai(BaseModel):
    class Meta:
        verbose_name = 'Rentang Nilai'
        verbose_name_plural = 'Rentang Nilai'
        unique_together = ('kelas', 'predikat')

    PREDIKAT = (
        ('A', 'Sangat Baik'),
        ('B', 'Baik'),
        ('C', 'Cukup baik'),
        ('D', 'Kurang baik'),
        ('E', 'Sangat kurang'),
    )

    PERTAHANKAN = 'pertahankan' 
    TINGKATKAN =  'tingkatkan'
    PERLU_BIMBINGAN = 'perlu_bimbingan'

    AKSI = (
        (PERTAHANKAN, 'Pertahankan'),
        (TINGKATKAN, 'Tingkatkan'),
        (PERLU_BIMBINGAN, 'Perlu Bimbingan'),
    )

    kelas = models.ForeignKey(
        Kelas, on_delete=models.CASCADE,
        related_name='rentang_nilai'
        )
    nilai_minimum = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    nilai_maximum = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    predikat = models.CharField(
        max_length=1,
        choices=PREDIKAT,
        default='A'
    )
    aksi = models.CharField(
        max_length=125,
        choices=AKSI,
        default=TINGKATKAN
    )

    def __str__(self):
        return self.predikat


class MataPelajaranKelas(BaseModel):
    class Meta:
        verbose_name = 'Mata Pelajaran Kelas'
        verbose_name_plural = 'Mata Pelajaran Kelas'
        unique_together = ('kelas', 'mata_pelajaran')

    kelas = models.ForeignKey(
        Kelas,
        on_delete=models.CASCADE,
        related_name='mata_pelajaran')
    guru = models.ForeignKey(
        Guru,
        on_delete=models.CASCADE,
        related_name='mata_pelajaran')
    mata_pelajaran = models.ForeignKey(
        MataPelajaranKurikulum,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s %s" % (self.kelas, self.mata_pelajaran.mata_pelajaran)


class JadwalKelas(BaseModel):
    class Meta:
        verbose_name = 'Jadwal Kelas'
        verbose_name_plural = 'Jadwal Kelas'
        unique_together = ('hari', 'kelas')

    HARI = (
        (0, 'Senin'),
        (1, 'Selasa'),
        (2, 'Rabu'),
        (3, 'Kamis'),
        (4, 'Jumat'),
        (5, 'Sabtu'),
        (6, 'Minggu'),
    )
    hari = models.IntegerField(
        choices=HARI,
        default=1
    )
    kelas = models.ForeignKey(
        Kelas,
        on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.kelas, self.hari)


class ItemJadwalPelajaran(BaseModel):
    class Meta:
        verbose_name = 'Jadwal Pelajaran'
        verbose_name_plural = 'Jadwal Pelajaran'

    jadwal_kelas = models.ForeignKey(
        JadwalKelas,
        related_name='mata_pelajaran',
        on_delete=models.CASCADE
    )
    mata_pelajaran_kelas = models.ForeignKey(
        MataPelajaranKelas,
        on_delete=models.CASCADE,
        related_name='jadwal'
    )
    jam_mulai = models.TimeField(default=timezone.now)
    jam_berakhir = models.TimeField(default=timezone.now)
    deskripsi = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return "%s" % self.mata_pelajaran_kelas


class ItemJadwalEkstraKurikuler(BaseModel):
    class Meta:
        verbose_name = 'Jadwal Ekstra Kurikuler'
        verbose_name_plural = 'Jadwal Ekstra Kurikuler'

    jadwal_kelas = models.ForeignKey(
        JadwalKelas,
        related_name='ekskul',
        on_delete=models.CASCADE
    )
    ekstra_kurikuler = models.ForeignKey(
        EkstraKurikuler,
        on_delete=models.CASCADE,
        related_name='jadwal'
    )
    jam_mulai = models.TimeField(default=timezone.now)
    jam_berakhir = models.TimeField(default=timezone.now)
    deskripsi = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return "%s" % self.ekstra_kurikuler


class PresensiSiswa(BaseModel):
    class Meta:
        verbose_name = 'Presensi Siswa'
        verbose_name_plural = 'Presensi Siswa'
        unique_together = ('kelas', 'tanggal')

    kelas = models.ForeignKey(
        Kelas, on_delete=models.CASCADE)
    tanggal = models.DateField(default=timezone.now)

    def __str__(self):
        return "%s %s" % (self.kelas, self.tanggal)


class ItemPresensiSiswa(BaseModel):
    class Meta:
        verbose_name = 'Item Presensi Siswa'
        verbose_name_plural = 'Item Presensi Siswa'
        unique_together = ('presensi_siswa', 'siswa_kelas')

    presensi_siswa = models.ForeignKey(
        PresensiSiswa, related_name='items',
        on_delete=models.CASCADE
    )
    siswa_kelas = models.ForeignKey(
        SiswaKelas, related_name='presensi',
        on_delete=models.CASCADE)
    status = models.CharField(
        max_length=3,
        choices=(
            ('H', 'Hadir'),
            ('S', 'Sakit'),
            ('I', 'Izin'),
            ('A', 'Tanpa Keterangan'),
        ),
        default='H'
    )

    def __str__(self):
        return "%s %s" % (self.presensi_siswa, self.siswa_kelas)


class PiketKelas(BaseModel):
    class Meta:
        verbose_name = 'Piket Kelas'
        verbose_name_plural = 'Piket Kelas'
        unique_together = ('kelas', 'hari')

    HARI = (
        (1, 'Senin'),
        (2, 'Selasa'),
        (3, 'Rabu'),
        (4, 'Kamis'),
        (5, 'Jumat'),
        (6, 'Sabtu'),
        (7, 'Minggu'),
    )
    kelas = models.ForeignKey(
        Kelas, on_delete=models.CASCADE,
        related_name='piket_kelas')
    hari = models.IntegerField(
        choices=HARI,
        default=1
    )

    def __str__(self):
        return "%s %s" % (self.kelas, self.get_hari_display())


class ItemPiketKelas(BaseModel):
    class Meta:
        verbose_name = 'Item PiketKelas'
        verbose_name_plural = 'Item PiketKelas'
        unique_together = ('piket_kelas', 'siswa_kelas')

    piket_kelas = models.ForeignKey(
        PiketKelas, related_name='items',
        on_delete=models.CASCADE
    )
    siswa_kelas = models.ForeignKey(
        SiswaKelas, related_name='piket_kelas',
        on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.piket_kelas, self.siswa_kelas)


@receiver(post_save, sender=Kelas)
def after_save_kelas(sender, **kwargs):
    created = kwargs.pop('created', None)
    instance = kwargs.pop('instance', None)
    if created:
        # create jadwal pelajaran kosong
        jadwal = []
        for hari in JadwalKelas.HARI:
            jadwal.append(JadwalKelas(
                kelas=instance,
                hari=hari[0]
            ))
        JadwalKelas.objects.bulk_create(jadwal)
        # create piket kelas kosong
        piket = []
        for hari in PiketKelas.HARI:
            piket.append(PiketKelas(
                kelas=instance,
                hari=hari[0]
            ))
        PiketKelas.objects.bulk_create(jadwal)
        # create rentang nilai kosong
        rentang = []
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='A',
                nilai_minimum = 81,
                nilai_maximum = 100,
                aksi = RentangNilai.PERTAHANKAN,
            )
        )
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='B',
                nilai_minimum = 66,
                nilai_maximum = 80,
                aksi = RentangNilai.TINGKATKAN,
            )
        )
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='C',
                nilai_minimum = 56,
                nilai_maximum = 65,
                aksi = RentangNilai.TINGKATKAN,
            )
        )
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='D',
                nilai_minimum = 41,
                nilai_maximum = 55,
                aksi = RentangNilai.PERLU_BIMBINGAN,
            )
        )
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='E',
                nilai_minimum = 0,
                nilai_maximum = 40,
                aksi = RentangNilai.PERLU_BIMBINGAN,
            )
        )
        RentangNilai.objects.bulk_create(rentang)


@receiver(post_save, sender=PresensiSiswa)
def after_save_presensi_siswa(sender, **kwargs):
    created = kwargs.pop('created', None)
    instance = kwargs.pop('instance', None)
    if created:
        # add initial items
        items = []
        for siswa in instance.kelas.siswa.all():
            items.append(
                ItemPresensiSiswa(
                    siswa_kelas=siswa,
                    presensi_siswa=instance
                )
            )
        ItemPresensiSiswa.objects.bulk_create(items)