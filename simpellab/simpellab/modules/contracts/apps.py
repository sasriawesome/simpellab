from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'simpellab.modules.contracts'
    label = 'simpellab_contracts'
    verbose_name = 'Contracts'