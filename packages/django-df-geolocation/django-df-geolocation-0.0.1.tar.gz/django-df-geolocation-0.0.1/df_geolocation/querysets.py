from typing import Any

from django.db import models

from .functions import EarthDistance, LLToEarth


class PositionQuerySet(models.QuerySet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.lat_field = getattr(self.model, "position_field_name", "") + "lat"
        self.lon_field = getattr(self.model, "position_field_name", "") + "lon"

    # This was an old implementation that did not seem to work
    # def in_range(self, lat, lon, meters):
    #     return self.annotate(
    #         earthbox=EarthBox(LLToEarth(lat, lon), meters),
    #     ).filter(earthbox__in_georange=LLToEarth(self.lat_field, self.lon_field))

    def in_range(
        self, lat: float, lon: float, meters: float = 0.0, miles: float = 0.0
    ) -> models.QuerySet:
        meters = meters or (miles * 1609.34)
        return self.annotate_range(lat, lon).filter(range__lte=meters)

    def annotate_range(self, lat: float, lon: float) -> models.QuerySet:
        return self.annotate(
            range=EarthDistance(
                LLToEarth(self.lat_field, self.lon_field), LLToEarth(lat, lon)
            )
        )
