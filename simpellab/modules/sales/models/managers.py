from django.db import models


class SalesQuotationManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs


class SalesOrderManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs
