from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'simpellab.modules.quotations'
    label = 'simpellab_quotations'
    verbose_name = 'Quotations'