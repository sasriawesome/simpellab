from django.apps import AppConfig as AppConfigBase
from django.utils.translation import gettext_lazy as _

class AppConfig(AppConfigBase):
    name = 'simpellab.modules.partners'
    label = 'simpellab_partners'
    verbose_name = _('Simpellab Partners')