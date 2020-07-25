from django.db import models
from django.db.utils import cached_property
from django.utils import timezone, translation
from django.core.validators import MinValueValidator, MaxValueValidator

from sister.core.models import BaseModel

class Ruang(BaseModel):
    class Meta:
        verbose_name = 'Ruang'
        verbose_name_plural = 'Ruang'

    kode = models.CharField(
        max_length=10,
        unique=True
    )
    nama = models.CharField(
        max_length=100,
    )
    fungsi = models.TextField(
        null=True, blank=True,
    )
    kapasitas = models.IntegerField(
        validators=[
            MinValueValidator(10),
            MaxValueValidator(100),
        ]
    )

    def __str__(self):
        return self.kode