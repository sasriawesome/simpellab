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
from sister.auth.models import Person
from sister.modules.ruang.models import Ruang
from sister.modules.sekolah import managers


_ = translation.ugettext_lazy


class TahunAjaran(BaseModel):
    class Meta:
        verbose_name = 'Tahun Ajaran'
        verbose_name_plural = 'Tahun Ajaran'

    kode = models.CharField(
        max_length=10,
        editable=False, unique=True
    )
    tahun_mulai = models.IntegerField(
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(3000),
        ]
    )
    tahun_akhir = models.IntegerField(
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(3000),
        ]
    )

    def __str__(self):
        return self.kode

    def generate_kode(self):
        return "%s/%s" % (self.tahun_mulai, self.tahun_akhir)

    def save(self, *args, **kwargs):
        self.kode = self.generate_kode()
        super().save(*args, **kwargs)


class Sekolah(BaseModel):
    class Meta:
        verbose_name = 'Sekolah'
        verbose_name_plural = 'Sekolah'

    npsn = models.CharField(max_length=25)
    nss = models.CharField(max_length=25)
    nama_sekolah = models.CharField(max_length=225)

    def __str__(self):
        return self.nama_sekolah


class Kurikulum(BaseModel):
    class Meta:
        verbose_name = 'Kurikulum'
        verbose_name_plural = 'Kurikulum'
        unique_together = ('tahun', 'kkni', 'tingkat', 'revisi')

    kode = models.CharField(
        max_length=25, editable=False, unique=True)
    nama = models.CharField(max_length=225)
    tahun = models.IntegerField(default=0)
    kkni = models.IntegerField(
        choices=[(x, x) for x in range(1, 10)],
        default=1
    )
    tingkat = models.IntegerField(
        choices=[(x, x) for x in range(1, 13)],
        default=1
    )
    revisi = models.IntegerField(default=0)

    def __str__(self):
        return self.kode

    def generate_kode(self):
        return "K%s.T%s.K%s.R%s" % (
            self.tahun, self.tingkat, self.kkni, self.revisi
        )

    def save(self, *args, **kwargs):
        self.kode = self.generate_kode()
        super(Kurikulum, self).save(*args, **kwargs)


class MataPelajaran(BaseModel):
    class Meta:
        verbose_name = 'Mata Pelajaran'
        verbose_name_plural = 'Mata Pelajaran'

    kode = models.CharField(max_length=25)
    nama = models.CharField(max_length=225)

    def __str__(self):
        return self.kode


class MataPelajaranKurikulum(BaseModel):
    class Meta:
        verbose_name = 'Mata Pelajaran Kurikulum'
        verbose_name_plural = 'Mata Pelajaran Kurikulum'

    mata_pelajaran = models.ForeignKey(
        MataPelajaran,
        on_delete=models.CASCADE)
    kurikulum = models.ForeignKey(
        Kurikulum,
        on_delete=models.CASCADE)

    def __str__(self):
        return "%s.%s" % (self.kurikulum, self.mata_pelajaran)


class Tema(BaseModel):
    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Tema'

    nomor = models.IntegerField()
    judul = models.CharField(max_length=225)
    deskripsi = models.TextField(null=True, blank=True)
    mata_pelajaran_kurikulum = models.ForeignKey(
        MataPelajaranKurikulum,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s Tema %s" % (self.mata_pelajaran_kurikulum, self.nomor)


class KompetensiInti(BaseModel):
    class Meta:
        verbose_name = 'Kompetensi Inti'
        verbose_name_plural = 'Kompetensi Inti'

    nomor = models.IntegerField()
    deskripsi = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return "%s. %s" % (self.nomor, self.deskripsi)


class KompetensiDasar(BaseModel):
    class Meta:
        verbose_name = 'Kompetensi Dasar'
        verbose_name_plural = 'Kompetensi Dasar'
        unique_together = (
            'mata_pelajaran_kurikulum',
            'kompetensi_inti',
            'nomor'
        )

    mata_pelajaran_kurikulum = models.ForeignKey(
        MataPelajaranKurikulum,
        on_delete=models.CASCADE)
    kompetensi_inti = models.ForeignKey(
        KompetensiInti,
        on_delete=models.CASCADE
    )
    nomor = models.IntegerField()
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    keyword = models.CharField(
        max_length=255,
        verbose_name=_('Kata kunci')
        )
    deskripsi = models.TextField(
        verbose_name=_('Kata kunci')
        )
    ph = models.BooleanField(default=True)
    pts = models.BooleanField(default=False)
    pas = models.BooleanField(default=True)

    @property
    def kode(self):
        return "%s.%s" % (self.kompetensi_inti.nomor, self.nomor)

    def __str__(self):
        return "%s KD %s" % (
            self.mata_pelajaran_kurikulum,
            self.kode
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

    def get_jadwal(self, current_day=True):
        mapel = self.mata_pelajaran.all()
        filters = {
                'kelas': self.id,
            }
        if current_day:
            filters['hari'] = timezone.now().weekday()
        return ItemJadwalPelajaran.objects.annotate(
                kelas = models.F('jadwal_pelajaran__kelas'),
                hari = models.F('jadwal_pelajaran__hari')
            ).filter(**filters)

class RentangNilai(BaseModel):
    class Meta:
        verbose_name = 'Rentang Nilai'
        verbose_name_plural = 'Rentang Nilai'

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
        choices=(
            ('A', 'Sangat Baik'),
            ('B', 'Baik'),
            ('C', 'Cukup baik'),
            ('D', 'Kurang baik'),
            ('E', 'Sangat kurang'),
        ),
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


class JadwalPelajaran(BaseModel):
    class Meta:
        verbose_name = 'Jadwal Pelajaran'
        verbose_name_plural = 'Jadwal Pelajaran'
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

    jadwal_pelajaran = models.ForeignKey(
        JadwalPelajaran,
        related_name='items',
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

class JenisPenilaian:
    TGS = 'TGS'
    PH = 'PH'
    PTS = 'PTS'
    PAS = 'PAS'
    TYPE = (
        (TGS, 'Tugas'),
        (PH, 'Penilaian Harian'),
        (PTS, 'Penilaian Tengah Semester'),
        (PAS, 'Penilaian Akhir Semester')
    )


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
        default=0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Tugas dan Pekerjaan Rumah'
    )
    ph = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Penilaian Harian'
    )
    pts = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Penilaian Tengah Semester'
    )
    pas = models.PositiveIntegerField(
        default=0,
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


class MetodePenilaianBase(models.Model):
    class Meta:
        abstract = True

    @cached_property
    def nilai_ph(self):
        raise NotImplementedError

    @cached_property
    def nilai_pts(self):
        raise NotImplementedError

    @cached_property
    def nilai_pas(self):
        raise NotImplementedError

    @cached_property
    def nilai_total(self):
        raise NotImplementedError

    def build_description(self):
        # get all value keyword from kd
        pass

    @cached_property
    def predikat(self):
        raise NotImplementedError

    def _get_rentang(self, kelas, nilai):
        try:
            rentang = RentangNilai.objects.get(
                kelas=kelas,
                nilai_minimum__lt=nilai,
                nilai_maximum__gt=nilai
            )
            return rentang
        except:
            return 'Rentang Nilai tidak ditemukan'


class MetodePenilaianTerbobot(MetodePenilaianBase):
    """ (Average PH * Bobot PH) + (Average PTS * Bobot PTS) + (Average PAS * Bobot PAS) """
    class Meta:
        abstract = True

    @cached_property
    def nilai_tugas(self):
        score = self._get_nilai('TUGAS')
        weight = self.mata_pelajaran_kelas.bobot.tugas
        weighted_score = (score * weight)/100
        return weighted_score

    @cached_property
    def nilai_ph(self):
        score = self._get_nilai('PH')
        weight = self.mata_pelajaran_kelas.bobot.ph
        weighted_score = (score * weight)/100
        return weighted_score

    @cached_property
    def nilai_pts(self):
        score = self._get_nilai('PTS')
        weight = self.mata_pelajaran_kelas.bobot.pts
        weighted_score = (score * weight)/100
        return weighted_score

    @cached_property
    def nilai_pas(self):
        score = self._get_nilai('PAS')
        weight = self.mata_pelajaran_kelas.bobot.pas
        weighted_score = (score * weight)/100
        return weighted_score

    @cached_property
    def nilai_total(self):
        return round(self.nilai_ph + self.nilai_pts + self.nilai_pas)

    def build_description(self):
        # get all value keyword from kd
        pass

    @cached_property
    def predikat(self):
        rentang_nilai = self._get_rentang(
            self.siswa_kelas.kelas,
            self.nilai_total
            )
        return rentang_nilai.predikat

    def _get_nilai(self, jenis):
        items = getattr(self, 'items', None)
        result = items.filter(jenis_penilaian=jenis).aggregate(
            total=models.Sum('nilai'),
            count=models.Count('*'),
        )
        if not result['total'] or not result['count']:
            return 0
        else:
            total = result['total'] or 0
            count = result['count'] or 0
            average = total / count
            return average

    def _get_rentang(self, kelas, nilai):
        try:
            rentang = RentangNilai.objects.get(
                kelas=kelas,
                nilai_minimum__lt=nilai,
                nilai_maximum__gt=nilai
            )
            return rentang
        except:
            return 'Rentang Nilai tidak ditemukan'


class PenilaianMataPelajaran(MetodePenilaianTerbobot, BaseModel):
    class Meta:
        verbose_name = 'Penilaian Mata Pelajaran'
        verbose_name_plural = 'Penilaian Mata Pelajaran'
        unique_together = (
            'siswa_kelas',
            'mata_pelajaran_kelas'
        )

    objects = managers.PenilaianMataPelajaranManager()

    siswa_kelas = models.ForeignKey(
        SiswaKelas,
        on_delete=models.CASCADE)
    mata_pelajaran_kelas = models.ForeignKey(
        MataPelajaranKelas,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='penilaian'
    )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )

    def __str__(self):
        return "%s %s" % (
            self.siswa_kelas,
            self.mata_pelajaran_kelas,
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ItemPenilaianMataPelajaran(BaseModel):
    class Meta:
        verbose_name = 'Item Penilaian Siswa'
        verbose_name_plural = 'Item Penilaian Siswa'
        ordering=['jenis_penilaian', 'kompetensi_dasar__nomor']
        unique_together = (
            'penilaian_siswa',
            'kompetensi_dasar',
            'jenis_penilaian'
        )

    penilaian_siswa = models.ForeignKey(
        PenilaianMataPelajaran, related_name='items',
        on_delete=models.PROTECT
    )
    jenis_penilaian = models.CharField(
        max_length=3,
        choices=JenisPenilaian.TYPE,
        default=JenisPenilaian.PH
    )
    kompetensi_dasar = models.ForeignKey(
        KompetensiDasar,
        on_delete=models.PROTECT
    )
    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    def clean(self):
        # Memastikan mata pelajaran kelas dan mata pelajaran pada
        # kompetensi yang dipilih sesuai
        mpk = self.penilaian_siswa.mata_pelajaran_kelas
        kd = self.kompetensi_dasar
        if mpk.mata_pelajaran != kd.mata_pelajaran_kurikulum:
            raise ValidationError({
                'kompetensi_dasar': 'Mata pelajaran Kelas dan Mata '
                                    'Pelajaran pada Kompetensi tidak sesuai'
            })


class EkstraKurikuler(BaseModel):
    class Meta:
        verbose_name = 'Ekstra Kurikuler'
        verbose_name_plural = 'Ekstra Kurikuler'

    nama = models.CharField(
        max_length=225,
        verbose_name=_('nama')
    )

    def __str__(self):
        return self.nama


class PenilaianEkstraKurikuler(BaseModel):
    class Meta:
        verbose_name = 'Penilaian Ekstra Kurikuler'
        verbose_name_plural = 'Penilaian Ekstra Kurikuler'

    siswa_kelas = models.ForeignKey(
        SiswaKelas, 
        on_delete=models.CASCADE)
    ekskul = models.ForeignKey(
        EkstraKurikuler,
        editable=True,
        on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(
        TahunAjaran,
        on_delete=models.CASCADE)
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

    @cached_property
    def rentang(self):
        return self._get_rentang()

    @cached_property
    def predikat(self):
        return self.rentang.predikat
        
    def _get_rentang(self):
        try:
            rentang = RentangNilai.objects.get(
                kelas=self.siswa_kelas.kelas,
                nilai_minimum__lt=self.nilai,
                nilai_maximum__gt=self.nilai
            )
            return rentang
        except:
            return 'Rentang Nilai tidak ditemukan'

class NilaiSiswa(BaseModel):
    class Meta:
        verbose_name = 'Nilai Siswa'
        verbose_name_plural = 'Nilai Siswa'

    siswa_kelas = models.ForeignKey(
        SiswaKelas, on_delete=models.CASCADE)
    kelas = models.ForeignKey(
        Kelas,
        editable=False,
        on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(
        TahunAjaran,
        on_delete=models.CASCADE)
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    mata_pelajaran = models.ForeignKey(
        MataPelajaranKurikulum,
        on_delete=models.CASCADE)
    nilai = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


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


@receiver(post_save, sender=PresensiSiswa)
def after_save_order_fee(sender, **kwargs):
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