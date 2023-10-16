from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArtdNequiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "artd_nequi"
    verbose_name = _("ArtD Nequi")
