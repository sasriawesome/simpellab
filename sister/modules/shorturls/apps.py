from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'sister.modules.shorturls'
    label = 'sister_shorturls'
    verbose_name = _('Short URLs')