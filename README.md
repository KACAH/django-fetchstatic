django-fetchstatic
==================

Django application, that allows download and store static libraries like "jquery" and "bootstrap" without keeping them in development repository.

How to use:

1) Add STATIC_LIBS option into settings file. For example check test/staticlibs.py
2) Add fetchstatic into INSTALLED_APPS. 
    Note: "django.contrib.staticfiles" must be included in INSTALLED_APPS
    Note: STATIC_URL must be specified
3) Download JS and CSS files into fetch_directory using command
    python manage.py fetch_static
4) Add into template file
    {% load include_static %}
5) Add into template file header
    {% include_static %}
   This will include downloaded js and css files into HTML
