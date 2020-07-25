from django.db import models
from django.utils import timezone


class PenilaianMataPelajaranManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def get_item_subquery(self, jenis_penilaian):
        from .models import ItemPenilaianMataPelajaran
        query = models.Subquery(
            ItemPenilaianMataPelajaran.objects.filter(
                penilaian_siswa=models.OuterRef('id'),
                jenis_penilaian=jenis_penilaian
            ).order_by().values('penilaian_mata_pelajaran_id').annotate(
                total=models.Sum('nilai'),
                count=models.Count('*'),
                average=models.F('total') / models.F('count')
            ).values('average')
        )
        return query

    def all_with_summary(self):
        qs = self.get_queryset()
        return qs.annotate(
            nilai_ph=self.get_item_subquery('PH'),
            nilai_pts=self.get_item_subquery('PTS'),
            nilai_pas=self.get_item_subquery('PAS')
        )

    def get_with_summary(self, **filters):
        qs = self.all_with_summary()
        return qs.get(**filters)