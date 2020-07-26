# Generated by Django 3.0.8 on 2020-07-26 19:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sister_kurikulum', '0001_initial'),
        ('sister_personal', '0001_initial'),
        ('sister_ruang', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kelas',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('nama_kelas', models.CharField(max_length=225)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('AKTIF', 'Aktif'), ('SELESAI', 'Selesai')], default='PENDING', max_length=10)),
                ('guru_kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kelas', to='sister_personal.Guru')),
                ('kurikulum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_kurikulum.Kurikulum')),
                ('ruang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ruang', to='sister_ruang.Ruang')),
                ('tahun_ajaran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_kurikulum.TahunAjaran')),
            ],
            options={
                'verbose_name': 'Kelas',
                'verbose_name_plural': 'Kelas',
            },
        ),
        migrations.CreateModel(
            name='SiswaKelas',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('status', models.IntegerField(choices=[(1, 'Baru'), (2, 'Tinggal Kelas'), (99, 'Lainnya')], default=1)),
                ('status_lain', models.CharField(blank=True, max_length=56, null=True)),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='siswa', to='sister_pembelajaran.Kelas')),
                ('siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kelas', to='sister_personal.Siswa')),
            ],
            options={
                'verbose_name': 'Siswa Kelas',
                'verbose_name_plural': 'Siswa Kelas',
                'unique_together': {('siswa', 'kelas')},
            },
        ),
        migrations.CreateModel(
            name='PresensiSiswa',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('tanggal', models.DateField(default=django.utils.timezone.now)),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_pembelajaran.Kelas')),
            ],
            options={
                'verbose_name': 'Presensi Siswa',
                'verbose_name_plural': 'Presensi Siswa',
                'unique_together': {('kelas', 'tanggal')},
            },
        ),
        migrations.CreateModel(
            name='PiketKelas',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('hari', models.IntegerField(choices=[(1, 'Senin'), (2, 'Selasa'), (3, 'Rabu'), (4, 'Kamis'), (5, 'Jumat'), (6, 'Sabtu'), (7, 'Minggu')], default=1)),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='piket_kelas', to='sister_pembelajaran.Kelas')),
            ],
            options={
                'verbose_name': 'Piket Kelas',
                'verbose_name_plural': 'Piket Kelas',
                'unique_together': {('kelas', 'hari')},
            },
        ),
        migrations.CreateModel(
            name='MataPelajaranKelas',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mata_pelajaran', to='sister_personal.Guru')),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mata_pelajaran', to='sister_pembelajaran.Kelas')),
                ('mata_pelajaran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_kurikulum.MataPelajaranKurikulum')),
            ],
            options={
                'verbose_name': 'Mata Pelajaran Kelas',
                'verbose_name_plural': 'Mata Pelajaran Kelas',
                'unique_together': {('kelas', 'mata_pelajaran')},
            },
        ),
        migrations.CreateModel(
            name='JadwalKelas',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('hari', models.IntegerField(choices=[(0, 'Senin'), (1, 'Selasa'), (2, 'Rabu'), (3, 'Kamis'), (4, 'Jumat'), (5, 'Sabtu'), (6, 'Minggu')], default=1)),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_pembelajaran.Kelas')),
            ],
            options={
                'verbose_name': 'Jadwal Pelajaran',
                'verbose_name_plural': 'Jadwal Pelajaran',
                'unique_together': {('hari', 'kelas')},
            },
        ),
        migrations.CreateModel(
            name='ItemJadwalPelajaran',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('jam_mulai', models.TimeField(default=django.utils.timezone.now)),
                ('jam_berakhir', models.TimeField(default=django.utils.timezone.now)),
                ('deskripsi', models.CharField(blank=True, max_length=225, null=True)),
                ('jadwal_kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mata_pelajaran', to='sister_pembelajaran.JadwalKelas')),
                ('mata_pelajaran_kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jadwal', to='sister_pembelajaran.MataPelajaranKelas')),
            ],
            options={
                'verbose_name': 'Jadwal Pelajaran',
                'verbose_name_plural': 'Jadwal Pelajaran',
            },
        ),
        migrations.CreateModel(
            name='ItemJadwalEkstraKurikuler',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('jam_mulai', models.TimeField(default=django.utils.timezone.now)),
                ('jam_berakhir', models.TimeField(default=django.utils.timezone.now)),
                ('deskripsi', models.CharField(blank=True, max_length=225, null=True)),
                ('ekstra_kurikuler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jadwal', to='sister_kurikulum.EkstraKurikuler')),
                ('jadwal_kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ekskul', to='sister_pembelajaran.JadwalKelas')),
            ],
            options={
                'verbose_name': 'Jadwal Ekstra Kurikuler',
                'verbose_name_plural': 'Jadwal Ekstra Kurikuler',
            },
        ),
        migrations.CreateModel(
            name='RentangNilai',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('nilai_minimum', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('nilai_maximum', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('predikat', models.CharField(choices=[('A', 'Sangat Baik'), ('B', 'Baik'), ('C', 'Cukup baik'), ('D', 'Kurang baik'), ('E', 'Sangat kurang')], default='A', max_length=1)),
                ('aksi', models.CharField(choices=[('pertahankan', 'Pertahankan'), ('tingkatkan', 'Tingkatkan'), ('perlu_bimbingan', 'Perlu Bimbingan')], default='tingkatkan', max_length=125)),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentang_nilai', to='sister_pembelajaran.Kelas')),
            ],
            options={
                'verbose_name': 'Rentang Nilai',
                'verbose_name_plural': 'Rentang Nilai',
                'unique_together': {('kelas', 'predikat')},
            },
        ),
        migrations.CreateModel(
            name='ItemPresensiSiswa',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('status', models.CharField(choices=[('H', 'Hadir'), ('S', 'Sakit'), ('I', 'Izin'), ('A', 'Tanpa Keterangan')], default='H', max_length=3)),
                ('presensi_siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sister_pembelajaran.PresensiSiswa')),
                ('siswa_kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presensi', to='sister_pembelajaran.SiswaKelas')),
            ],
            options={
                'verbose_name': 'Item Presensi Siswa',
                'verbose_name_plural': 'Item Presensi Siswa',
                'unique_together': {('presensi_siswa', 'siswa_kelas')},
            },
        ),
        migrations.CreateModel(
            name='ItemPiketKelas',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('piket_kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sister_pembelajaran.PiketKelas')),
                ('siswa_kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='piket_kelas', to='sister_pembelajaran.SiswaKelas')),
            ],
            options={
                'verbose_name': 'Item PiketKelas',
                'verbose_name_plural': 'Item PiketKelas',
                'unique_together': {('piket_kelas', 'siswa_kelas')},
            },
        ),
    ]