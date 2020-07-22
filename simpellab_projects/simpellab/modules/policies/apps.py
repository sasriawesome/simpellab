from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'simpellab.modules.policies'
    label = 'simpellab_policies'
    verbose_name = 'Policies'