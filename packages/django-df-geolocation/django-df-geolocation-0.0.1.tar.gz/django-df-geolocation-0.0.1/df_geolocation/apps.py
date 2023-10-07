from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DfGeolocationConfig(AppConfig):
    name = "df_geolocation"
    verbose_name = _("Django DF GEO Location")
