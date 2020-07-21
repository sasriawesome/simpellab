from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'simpellab.modules.blueprints'
    label = 'simpellab_blueprints'
    verbose_name = 'Blueprints'