from django.apps import AppConfig


class HashtagConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "hashtag"
    verbose_name = "HashTag"

    def ready(self):
        from . import signals
