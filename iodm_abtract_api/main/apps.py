from django.apps import AppConfig
import os

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':  # Prevent double-start with runserver
            return
        from .scheduler import start
        start()