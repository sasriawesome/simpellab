from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'sister.modules.penilaian'
    label = 'sister_penilaian'
    verbose_name = _('Penilaian')