from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


if not hasattr(settings, "STATIC_LIBS"):
    raise ImproperlyConfigured(
        "You must specify STATIC_LIBS option in settings.py")
