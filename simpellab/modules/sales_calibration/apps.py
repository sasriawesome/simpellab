from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'simpellab.modules.sales_calibration'
    label = 'simpellab_sales_calibration'
    verbose_name = 'Simpellab Sales Calibration'
