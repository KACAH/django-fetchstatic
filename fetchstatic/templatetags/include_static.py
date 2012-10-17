import fnmatch
import os

from django import template
from django.conf import settings
from django.contrib.staticfiles.finders import get_finders


register = template.Library()


def get_js(filename):
    """Return HTML JS include by filename"""

    return "<script type='text/javascript' src='%s'></script>" \
        % os.path.join(settings.STATIC_URL, filename)

def get_css(filename):
    """Return HTML CSS include by filename"""

    return "<link rel='stylesheet' type='text/css' href='%s'/>" \
        % os.path.join(settings.STATIC_URL, filename)

def list_static_includes():
    """List all known js and css static files"""

    _files = []

    for _finder in get_finders():
        for (_path, _storage) in _finder.list(None):
            if _path.endswith(".css") or _path.endswith(".js"):
                _files.append(_path)
    return _files

def include_library(lib_name, static_files):
    """Generate list of includes for directory"""

    _includes = []
    _files = [_file for _file in static_files if _file.find(lib_name) != -1]

    if not _files:
        _includes.append("<!-- Library '%s' not found -->" % lib_name)
        return _includes

    for _filename in fnmatch.filter(_files, "*.css"):
        _includes.append(get_css(_filename))
    for _filename in fnmatch.filter(_files, "*.js"):
        _includes.append(get_js(_filename))

    return _includes

@register.simple_tag
def include_static(library_name=None):
    """Include JS and CSS includes for all libraries"""

    _includes = []
    _static_files = list_static_includes()
    if library_name:
        _includes.extend(include_library(library_name, _static_files))
    else:
        for _lib in settings.STATIC_LIBS["libraries"]:
            _includes.extend(include_library(_lib["name"], _static_files))
    return "\n".join(_includes)
