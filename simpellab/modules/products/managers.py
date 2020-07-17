from django.db import models
from simpellab.core.managers import BasePolymorphicManager


class ParameterManager(models.Manager):
    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)


class ProductManager(BasePolymorphicManager):
    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)

    def get_spareparts(self):
        return self.get_queryset().filter(is_spareparts=True)

    def get_stockable(self):
        return self.get_queryset().filter(is_stockable=True)

    def can_be_purchased(self):
        return self.get_queryset().filter(can_be_purchased=True)

    def can_be_sold(self):
        return self.get_queryset().filter(can_be_sold=True)
