from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'sister.modules.sekolah'
    label = 'sister_sekolah'
    verbose_name = _('Sekolah')