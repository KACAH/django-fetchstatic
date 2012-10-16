import fnmatch
import os

from django import template
from django.conf import settings


register = template.Library()

ROOT_FOLDER = settings.STATIC_LIBS["root_directory"]
STATIC_FOLDER = os.path.join(
    ROOT_FOLDER,
    settings.STATIC_LIBS["fetch_directory"]
)

def get_static_name(filename):
    """Return filename relative to static URL"""
    
    filename = filename.replace(ROOT_FOLDER, "")
    if filename.startswith(os.sep):
        filename = filename[1:]
    return os.path.join(settings.STATIC_URL, filename)

def get_js(filename):
    """Return HTML JS include by filename"""

    return "<script type='text/javascript' src='%s'></script>" \
        % get_static_name(filename)

def get_css(filename):
    """Return HTML CSS include by filename"""

    return "<link rel='stylesheet' type='text/css' href='%s'/>" \
        % get_static_name(filename)

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
