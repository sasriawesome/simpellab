from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'simpellab.modules.services'
    label = 'simpellab_services'
    verbose_name = 'Simpellab Services'
