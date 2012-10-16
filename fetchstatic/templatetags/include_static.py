import fnmatch
import os

from django import template
from django.conf import settings


register = template.Library()
STATIC_FOLDER = settings.STATIC_LIBS["fetch_directory"]


def get_js(filename):
    """Return HTML JS include by filename"""

    return "<script type='text/javascript' src='%s'></script>" \
        % os.path.join(settings.STATIC_URL, "js", filename)

def get_css(filename):
    """Return HTML CSS include by filename"""

    filename = filename.replace(STATIC_FOLDER, "")
    return "<link rel='stylesheet' type='text/css' href='%s'/>" \
        % os.path.join(settings.STATIC_URL, filename)

@register.simple_tag
def include_static():
    """Include JS and CSS includes for all libraries"""
    
    _includes = []
    
    for _root, _dirnames, _filenames in os.walk(STATIC_FOLDER):
        for _filename in fnmatch.filter(_filenames, "*.css"):
            _includes.append(get_css(os.path.join(_root, _filename)))

    for _lib in settings.STATIC_LIBS["libraries"]:
        if _lib.has_key("js"):
            for _file in _lib["js"]:
                _filename = os.path.basename(_file)
                _includes.append(get_js(_filename))

    return "\n".join(_includes)
