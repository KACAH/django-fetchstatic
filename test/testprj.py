import os

from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template

from staticlibs import *

filepath, extension = os.path.splitext(__file__)

ROOT_URLCONF = os.path.basename(filepath)
DEBUG = TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (os.path.dirname(filepath),)
INSTALLED_APPS = ("django.contrib.staticfiles", "fetchstatic")
STATIC_URL = "/static/"

urlpatterns = patterns("", 
    (r"^$", direct_to_template, dict(
        template="test.html",
    )),
)
