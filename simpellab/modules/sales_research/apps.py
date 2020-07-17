from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'simpellab.modules.sales_research'
    label = 'simpellab_sales_research'
    verbose_name = 'Simpellab Sales Research'
