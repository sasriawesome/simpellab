from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = 'sister.api'
    label = 'sister_api'
    verbose_name = _('Simpellab API')