from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = 'simpellab.auth'
    label = 'simpellab_auth'
    verbose_name = _('Authentication and Authorization')