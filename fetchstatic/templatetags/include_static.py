import fnmatch
import os

from django import template
from django.conf import settings


register = template.Library()
STATIC_FOLDER = settings.STATIC_LIBS["fetch_directory"]


def get_js(filename):
    """Return HTML JS include by filename"""

    filename = filename.replace(STATIC_FOLDER, "")
    return "<script type='text/javascript' src='%s'></script>" \
        % os.path.join(settings.STATIC_URL, filename)

def get_css(filename):
    """Return HTML CSS include by filename"""

    filename = filename.replace(STATIC_FOLDER, "")
    return "<link rel='stylesheet' type='text/css' href='%s'/>" \
        % os.path.join(settings.STATIC_URL, filename)

def include_library(lib_name):
    """Generate list of includes for directory"""

    _includes = []

    _lib_path = os.path.join(STATIC_FOLDER, lib_name)
    if (not os.path.exists(_lib_path)):
        _includes.append("<!-- Library '%s' not found -->" % lib_name)
        return _includes

    for (_root, _dirnames, _filenames) in os.walk(_lib_path):
        for _filename in fnmatch.filter(_filenames, "*.css"):
            _includes.append(get_css(os.path.join(_root, _filename)))
        for _filename in fnmatch.filter(_filenames, "*.js"):
            _includes.append(get_js(os.path.join(_root, _filename)))

    return _includes

@register.simple_tag
def include_static(library_name=None):
    """Include JS and CSS includes for all libraries"""

    _includes = []
    if library_name:
        _includes.extend(include_library(library_name))
    else:
        for _lib in settings.STATIC_LIBS["libraries"]:
            _includes.extend(include_library(_lib["name"]))
    return "\n".join(_includes)
