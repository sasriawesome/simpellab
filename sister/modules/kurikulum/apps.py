from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'sister.modules.kurikulum'
    label = 'sister_kurikulum'
    verbose_name = _('Kurikulum')