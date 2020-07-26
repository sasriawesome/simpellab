from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'sister.modules.pembelajaran'
    label = 'sister_pembelajaran'
    verbose_name = _('Pembelajaran')