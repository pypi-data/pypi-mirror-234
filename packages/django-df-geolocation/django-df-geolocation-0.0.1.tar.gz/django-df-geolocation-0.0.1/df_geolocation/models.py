from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from .querysets import PositionQuerySet


class AddressMixin(models.Model):
    formatted = models.CharField(max_length=256, null=True, blank=True)
    street = models.CharField(
        _("Street Address"), max_length=255, blank=True, null=True
    )
    city = models.CharField(_("City"), max_length=100, blank=True, null=True)
    postcode = models.CharField(_("Postcode"), max_length=8, null=True, blank=True)
    country = CountryField(_("Country"), default="NL")

    def __str__(self) -> str:
        return f"{self.street}, {self.postcode} {self.city}, {self.country}"

    class Meta:
        abstract = True


class PositionMixin(models.Model):
    lat = models.FloatField(_("Latitude"))
    lon = models.FloatField(_("Longitude"))

    objects = PositionQuerySet.as_manager()

    class Meta:
        abstract = True


class Address(AddressMixin, PositionMixin):
    class Meta:
        abstract = True
