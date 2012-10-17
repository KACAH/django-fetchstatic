django-fetchstatic
==================

Django application, that allows download and store static libraries like "jquery" and "bootstrap" without keeping them in development repository.

How to use
---------------------

1. Add STATIC_LIBS option into settings file.
    Read 'STATIC_LIBS structure' section or check test/staticlibs.py for more information 
2. Add fetchstatic into INSTALLED_APPS
    Note: "django.contrib.staticfiles" must be included in INSTALLED_APPS
    Note: STATIC_URL must be specified
3. Download JS and CSS files using command
    python manage.py fetch_static /path/to/some/folder
4. Make sure, that Django searches for static files in /path/to/some/folder
5. Add into template file
    {% load include_static %}
6. Add into template file header
    {% include_static %}
    This will include all js and css of all libraries files into HTML
    You can also specify one library using
    {% include_static "Library_Name" %}

STATIC_LIBS structure
---------------------

TODO:
