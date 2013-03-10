from distutils.dir_util import copy_tree
import logging
import os
import shutil
import sys
import urllib2
import zipfile


class StaticFetcher(object):
    """Static files fetcher into local directories"""

    def __init__(self, static_libs, static_dir, temp_dir):
        self.static_libs = static_libs
        self.static_dir = static_dir
        self.temp_dir = temp_dir

    def fetch_all(self, force=False, logger=None):
        """Fetch all libraries in static libs dict"""
        self.fetch(None, force, logger)

    def fetch_one(self, libname, force=False, logger=None):
        """Fetch one library by given name"""
        self.fetch(libname, force, logger)

    def fetch(self, libname, force, logger):
        """Fetch one library if specified else all libraries"""

        self.force = force
        self.log = logger if logger else get_default_logger()
        self.make_dirs()

        try:
            for _lib in self.static_libs:
                if not libname or _lib["name"] == libname:
                    self.get_library(_lib)
        finally:
            shutil.rmtree(self.temp_dir)

    def make_dirs(self):
        """Make temp and lib dirs for libraries if don't exist"""

        if not os.path.exists(self.static_dir):
            os.makedirs(self.static_dir)
        os.makedirs(self.temp_dir)

    def download_file(self, url, dest):
        """Download file from url with progressbar"""

        BLOCK_SIZE = 8192
        UNKNOWN_SIZE = -1

        _response = urllib2.urlopen(url)
        _base_filename = os.path.basename(url)

        _meta = _response.info()
        _con_length = _meta.getheaders("Content-Length")
        if _con_length:
            _file_size = int(_meta.getheaders("Content-Length")[0])
            self.log.info(
                "Downloading %s (%s bytes)", _base_filename, _file_size)
        else:
            _file_size = UNKNOWN_SIZE
            self.log.info("Downloading %s (size unknown)", _base_filename)

        _file = open(dest, "wb")
        _file_size_dl = 0
        _buffer = _response.read(BLOCK_SIZE)
        while _buffer:
            _file_size_dl += len(_buffer)
            _file.write(_buffer)
            _buffer = _response.read(BLOCK_SIZE)

            if _file_size != UNKNOWN_SIZE:
                _progress = _file_size_dl * 100. / _file_size
                print r"File '%s': %10d bytes  [%3.2f%%]" \
                    % (_base_filename, _file_size_dl, _progress)
                sys.stdout.flush()

        _file.close()

    def get_file(self, file_params, folder):
        """Load file from url to folder

        @param file_params: tuple (url, path to download relative to folder)
        @param folder: path to download

        @return: Downloaded file name if all ok,
                 or None if there were problems during download

        """
        (_url, _plus_path) = file_params
        _base_filename = os.path.basename(_url)
        _dest_file_path = os.path.join(folder, _plus_path)
        _filename = os.path.join(_dest_file_path, _base_filename)

        if (not self.force) and os.path.exists(_filename):
            return _filename
        if (not os.path.exists(_dest_file_path)):
            os.makedirs(_dest_file_path)

        _download_filename = \
            os.path.join(self.temp_dir, _base_filename + ".part")
        try:
            self.download_file(_url, _download_filename)
        except urllib2.URLError, _ex:
            self.log.error("%s, while downloading '%s'", _ex.reason, _url)
            return None

        shutil.copyfile(_download_filename, _filename)
        self.log.info("'%s' succesfully downloaded", _base_filename)
        return _filename

    def paths_exist(self, paths, folder):
        """Check and return if all paths from zip exist in folder"""

        for (_zip_path, _static_path) in paths:
            _path_to_check = os.path.join(folder, _static_path)
            if not os.path.exists(_path_to_check):
                return False
        return True

    def file_is_not_min(self, filename):
        """Check if file if .js or .css, but not .min.js or .min.css"""

        #another type of file
        if (not filename.endswith(".js")) and (not filename.endswith(".css")):
            return False

        #mininized file
        if filename.endswith(".min.js") or filename.endswith(".min.css"):
            return False

        return True

    def make_only_min_js_css(self, folder):
        """Delete all .js and .css files that are not .min.js or .min.css"""

        for (_root, _dirnames, _filenames) in os.walk(folder):
            for _filename in _filenames:
                if self.file_is_not_min(_filename):
                    os.remove(os.path.join(_root, _filename))

    def copy_zip(self, zip_includes, folder, only_min):
        """Copy includes of zip file into folder"""

        for (_path, _dst) in zip_includes:
            _src = os.path.join(self.temp_dir, _path)
            _dst = os.path.join(folder, _dst)
            if not os.path.exists(_dst):
                os.makedirs(_dst)

            if os.path.isdir(_src):
                copy_tree(_src, _dst)

                if only_min:
                    self.make_only_min_js_css(_dst)
            else:
                if (not only_min) or (not file_is_not_min(_dst)):
                    shutil.copy(_src, _dst)


    def get_zip(self, zip_params, folder):
        """Download and extract zip file

        @param zip_params: dict {"url", "unpack", "only_min"}
        @param folder: path to unpack

        """
        if (not self.force) \
            and self.paths_exist(zip_params["unpack"], folder):
            return

        _url = zip_params["url"]
        _zipname = self.get_file((_url, "."), self.temp_dir)

        if not _zipname:
            return

        _zip = zipfile.ZipFile(_zipname)
        _zip.extractall(self.temp_dir)
        _zip.close()

        _only_min = zip_params.get("only_min")
        self.copy_zip(zip_params["unpack"], folder, _only_min)

    def force_static_dir(self, dir_name):
        """Create directory in static folder if not exist. Return it."""

        _path = os.path.join(self.static_dir, dir_name)
        if not os.path.exists(_path):
            os.makedirs(_path)
        return _path

    def get_library(self, lib):
        """Download lib's files to static folder

        @param lib: dictionary with optional keys: js, css, images, theme

        """
        _lib_path = self.force_static_dir(lib["name"])

        if lib.has_key("files"):
            for _url in lib["files"]:
                self.get_file(_url, _lib_path)

        if lib.has_key("zips"):
            for _zip_params in lib["zips"]:
                self.get_zip(_zip_params, _lib_path)


def get_default_logger():
    """Default console logger for simple usage"""

    _formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    _ch = logging.StreamHandler()
    _ch.setLevel(logging.DEBUG)
    _ch.setFormatter(_formatter)

    _logger = logging.getLogger("console_logger")
    _logger.setLevel(logging.DEBUG)
    _logger.addHandler(_ch)
    return _logger
