from django.db import models
from simpellab.core.managers import PolymorphicManager


class SalesQuotationManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs


class SalesOrderManager(PolymorphicManager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs
        