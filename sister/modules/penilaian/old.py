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

    objects = PenilaianMataPelajaranManager()

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



# class NilaiSiswa(BaseModel):
#     class Meta:
#         verbose_name = 'Nilai Siswa'
#         verbose_name_plural = 'Nilai Siswa'

#     siswa_kelas = models.ForeignKey(
#         SiswaKelas, on_delete=models.CASCADE)
#     kelas = models.ForeignKey(
#         Kelas,
#         editable=False,
#         on_delete=models.CASCADE)
#     tahun_ajaran = models.ForeignKey(
#         TahunAjaran,
#         on_delete=models.CASCADE)
#     semester = models.IntegerField(
#         choices=((1, 1), (2, 2),),
#         default=1
#     )
#     mata_pelajaran = models.ForeignKey(
#         MataPelajaranKurikulum,
#         on_delete=models.CASCADE)
#     nilai = models.IntegerField(
#         validators=[
#             MinValueValidator(0),
#             MaxValueValidator(100)
#         ]
#     )
