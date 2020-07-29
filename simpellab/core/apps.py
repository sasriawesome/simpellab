from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = 'simpellab.core'
    label = 'simpellab_core'
    verbose_name = _('Simpellab Core')