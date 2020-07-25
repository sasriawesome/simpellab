from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = 'sister.admin'
    label = 'sister_admin'
    verbose_name = _('Sister Admin')