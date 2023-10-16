from django.apps import AppConfig


class BootstrapDarkThemeConfig(AppConfig):
    name = "allianceauth.theme.bootstrap_dark"
    label = "bootstrap_dark"
    version = "5.3.0"
    verbose_name = f"Bootstrap Dark v{version}"

    def ready(self):
        pass
