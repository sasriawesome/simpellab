from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'simpellab.modules.products'
    label = 'simpellab_products'
    verbose_name = 'Simpellab Products'
