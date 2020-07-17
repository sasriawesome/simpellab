from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'simpellab.modules.sales_inspection'
    label = 'simpellab_sales_inspection'
    verbose_name = 'Simpellab Sales Inspection'
