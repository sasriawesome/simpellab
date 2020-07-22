from django.db import models

class PersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_employees(self):
        return self.filter(employee__isnull=False)

    def get_partners(self):
        return self.filter(partners__isnull=False)

    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)