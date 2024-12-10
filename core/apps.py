from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
   
    def ready(self):
        # Importer les signaux lorsque l'application est prête
        import core.signals