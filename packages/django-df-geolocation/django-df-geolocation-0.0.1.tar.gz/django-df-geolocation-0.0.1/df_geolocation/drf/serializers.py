from django_countries.serializer_fields import CountryField
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(read_only=True)
    country = CountryField(required=False)

    class Meta:
        read_only_fields = ("id",)
        fields = read_only_fields + (
            "formatted",
            "street",
            "city",
            "postcode",
            "country",
            "notes",
            "is_current",
            "lat",
            "lon",
        )


class PositionSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()
