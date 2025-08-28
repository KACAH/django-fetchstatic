import os
import sys
import logging

from django.conf import settings
from django.urls import path

from staticlibs import STATIC_LIBS


filepath, extension = os.path.splitext(__file__)


def test_view(request, *args, **kwargs):
    """Simple html render view

    @note: render_to_response imported insode to avoid Django
        errors running this file

    """
    from django.shortcuts import render
    return render(request, "test.html", None)

urlpatterns = [
    path("", test_view),
]


def setup_log():
    """Logging setup for demonstration purposes"""

    _formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s")

    _ch = logging.StreamHandler()
    _ch.setLevel(logging.DEBUG)
    _ch.setFormatter(_formatter)

    _logger = logging.getLogger(
        "fetchstatic.management.commands.fetch_static"
    )
    _logger.setLevel(logging.DEBUG)
    _logger.addHandler(_ch)

def run():
    settings.configure(
        ROOT_URLCONF = os.path.basename(filepath),
        DEBUG = True, TEMPLATE_DEBUG = True,
        TEMPLATES = [{
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.dirname(filepath)],
        }],
        INSTALLED_APPS = ("django.contrib.staticfiles", "fetchstatic"),
        SECRET_KEY = "+%i79h+o7@nlv9g(%*(qdcq89keb^4v-&$7r-sg@ic81&j6d)z",
        STATIC_URL = "/static/",
        STATIC_LIBS = STATIC_LIBS,
        STATICFILES_DIRS = ("./static/",),
    )
    setup_log()

    from django.core.management import execute_from_command_line
    execute_from_command_line()


if __name__ == "__main__":
    run()
