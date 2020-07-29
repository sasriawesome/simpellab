from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'simpellab.modules.sales_training'
    label = 'simpellab_sales_training'
    verbose_name = 'Sales Training'
