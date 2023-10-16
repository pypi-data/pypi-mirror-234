from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RpsMileaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rps_milea'
    verbose_name = _("Configuration")
