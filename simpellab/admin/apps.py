from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = 'simpellab.admin'
    label = 'simpellab_admin'
    verbose_name = _('Simpellab Admin')