from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'sister.modules.ruang'
    label = 'sister_ruang'
    verbose_name = _('Ruang')