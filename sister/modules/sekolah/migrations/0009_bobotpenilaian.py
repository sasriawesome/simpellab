# Generated by Django 3.0.8 on 2020-07-24 16:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sister_sekolah', '0008_auto_20200724_0848'),
    ]

    operations = [
        migrations.CreateModel(
            name='BobotPenilaian',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('jenis_penilaian', models.CharField(choices=[('PH', 'Penilaian Harian'), ('PTS', 'Penilaian Tengah Semester'), ('PAS', 'Penilaian Akhir Semester')], default='PH', max_length=3)),
                ('bobot', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('mata_pelajaran_kelas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sister_sekolah.MataPelajaranKelas')),
            ],
            options={
                'verbose_name': 'Bobot Penilaian',
                'verbose_name_plural': 'Bobot Penilaian',
                'unique_together': {('jenis_penilaian', 'mata_pelajaran_kelas')},
            },
        ),
    ]
