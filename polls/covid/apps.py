from django.apps import AppConfig


class CovidConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'covid'
    # FIXME: я хз как назвать, че за covid бля
    verbose_name = 'Главное приложение'
