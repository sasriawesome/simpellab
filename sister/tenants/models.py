from django.db import models
from tenant_users.tenants.models import TenantBase
from django_tenants.models import DomainMixin


class Client(TenantBase):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)


class Domain(DomainMixin):
    pass