from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'sister.tenants'
    label = 'sister_tenants'
    verbose_name = _('Tenants')