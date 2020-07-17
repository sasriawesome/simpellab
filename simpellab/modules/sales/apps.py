from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'simpellab.modules.sales'
    label = 'simpellab_sales'
    verbose_name = 'Simpellab Sales'
