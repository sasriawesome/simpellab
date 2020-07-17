from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = 'simpellab.modules.todo'
    label = 'simpellab_todo'
    verbose_name = _('Work and Service')