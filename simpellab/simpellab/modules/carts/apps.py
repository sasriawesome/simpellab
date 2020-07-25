from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'simpellab.modules.carts'
    label = 'simpellab_carts'
    verbose_name = 'Carts'