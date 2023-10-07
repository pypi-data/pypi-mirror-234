# Django DF GEO Location

DjangoFlow utilities to work with geolocations and addresses

## Installation:

- Install the package

```
pip install django-df-geolocation
```


- Include default `INSTALLED_APPS` from `df_geolocation.defaults` to your `settings.py`

```python
from df_geolocation.defaults import DF_GEOLOCATION_INSTALLED_APPS

INSTALLED_APPS = [
    ...
    *DF_GEOLOCATION_INSTALLED_APPS,
    ...
]

```


## Development

Installing dev requirements:

```
pip install -e .[test]
```

Installing pre-commit hook:

```
pre-commit install
```

Running tests:

```
pytest
```
