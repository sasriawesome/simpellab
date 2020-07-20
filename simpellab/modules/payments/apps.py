from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'simpellab.modules.payments'
    label = 'simpellab_payments'
    verbose_name = 'Payments'