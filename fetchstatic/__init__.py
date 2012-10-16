from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


if not hasattr(settings, "STATIC_LIBS"):
    raise ImproperlyConfigured(
        "You must specify STATIC_LIBS option in settings.py")
        
if not "libraries" in settings.STATIC_LIBS:
    raise ImproperlyConfigured(
        "You must specify libraries option in settings.STATIC_LIBS")
        
if not "fetch_directory" in settings.STATIC_LIBS:
    raise ImproperlyConfigured(
        "You must specify fetch_directory option in settings.STATIC_LIBS")
        
fetch_dir = settings.STATIC_LIBS["fetch_directory"]
if not fetch_dir in settings.STATICFILES_DIRS:
    settings.STATICFILES_DIRS = settings.STATICFILES_DIRS + (fetch_dir,)
