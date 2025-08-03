from django.apps import AppConfig


class AppConfig(AppConfig): # 將 MyappConfig 改為 AppConfig
    default_auto_field = "django.db.models.BigAutoField"
    name = "app" # 將 myapp 改為 app
