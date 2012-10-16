from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


if not hasattr(settings, "STATIC_LIBS"):
    raise ImproperlyConfigured(
        "You must specify STATIC_LIBS option in settings.py")

if not "libraries" in settings.STATIC_LIBS:
    raise ImproperlyConfigured(
        "You must specify libraries option in settings.STATIC_LIBS")

if settings.STATIC_LIBS.get("include_root_to_static"):
    root_dir = settings.STATIC_LIBS["root_directory"]
    if not root_dir in settings.STATICFILES_DIRS:
        settings.STATICFILES_DIRS = settings.STATICFILES_DIRS + (root_dir,)
