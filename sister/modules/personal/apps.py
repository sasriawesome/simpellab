from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'sister.modules.personal'
    label = 'sister_personal'
    verbose_name = _('Personal')