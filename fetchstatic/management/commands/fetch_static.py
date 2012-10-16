import logging
from optparse import make_option
import os
import shutil
import sys
import urllib2
import zipfile

from django.core.management.base import BaseCommand
from django.conf import settings


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Download libraries from internet to static folder"

    static_folder = settings.STATIC_LIBS["fetch_directory"]
    temp_folder = os.path.join(static_folder, "__temp")

    option_list = BaseCommand.option_list + (
        make_option("--force",
            action="store_true",
            dest="force",
            default=False,
            help="Overwrite existing files while downloading"),
        )

    def download_file(self, url, filename):
        """Download file from url with progressbar"""

        BLOCK_SIZE = 8192
        UNKNOWN_SIZE = -1

        _response = urllib2.urlopen(url)

        _meta = _response.info()
        _con_length = _meta.getheaders("Content-Length")
        if _con_length:
            _file_size = int(_meta.getheaders("Content-Length")[0])
            log.info("Downloading %s (%s bytes)", filename, _file_size)
        else:
            _file_size = UNKNOWN_SIZE
            log.info("Downloading %s (size unknown)", filename)    

        _file = open(filename, "wb")
        _file_size_dl = 0
        _buffer = _response.read(BLOCK_SIZE)
        while _buffer:
            _file_size_dl += len(_buffer)
            _file.write(_buffer)
            _buffer = _response.read(BLOCK_SIZE)

            if _file_size != UNKNOWN_SIZE:
                print r"%10d  [%3.2f%%]" \
                    % (_file_size_dl, _file_size_dl * 100. / _file_size)
                sys.stdout.flush()

        _file.close()

    def get_files(self, urls, folder):
        """Load files from urls to folder

        @param urls: list of url strings to files
        @param folder: path to download

        """
        for _url in urls:
            _base_filename = os.path.basename(_url)
            _filename = os.path.join(folder, _base_filename)
            if (not self.force) and os.path.exists(_filename):
                continue

            _file_resp = None
            try:
                self.download_file(_url, _filename)
            except urllib2.URLError, _ex:
                log.error("%s, while downloading '%s'", _ex.reason, _url)
                continue
            except:
                log.error("Unexpected error while downloading %s", _url)
                raise

            log.info("'%s' succesfully downloaded", _base_filename)

    def get_zip(self, zip_params, folder):
        """Download and extract zip file"""

        (_url, _zip_path) = zip_params
        _base_zipname = os.path.basename(_url)
        _zipname = os.path.join(self.temp_folder, _base_zipname)

        _base_folder = os.path.basename(_zip_path)
        _foldername = os.path.join(folder, _base_folder)

        if (not self.force) and os.path.exists(_foldername):
            return

        try:
            self.download_file(_url, _zipname)
        except urllib2.URLError, _ex:
            log.error("%s, while downloading '%s'", _ex.reason, _url)
            return
        except:
            log.error("Unexpected error while downloading %s", _url)
            raise

        _zip = zipfile.ZipFile(_zipname)
        _zip.extractall(self.temp_folder)
        _zip.close()

        shutil.copytree(os.path.join(self.temp_folder, _zip_path), _foldername)

    def force_static_dir(self, dir_name):
        """Create directory in static folder if not exist. Return it."""
        
        _path = os.path.join(self.static_folder, dir_name)
        if not os.path.exists(_path):
            os.makedirs(_path)
        return _path
        
    def get_library(self, lib):
        """Download lib's files to static folder

        @param lib: dictionary with optional keys: js, css, images, theme

        """
        FILES = ["js", "css", "images"]
        for _key in FILES:
            if lib.has_key(_key):
                self.get_files(lib[_key], self.force_static_dir(_key))

        if lib.has_key("theme"):
            self.get_zip(lib["theme"], self.force_static_dir("theme"))

    def clean_temp_dir(self):
        for _file in os.listdir(self.temp_folder):
            _file_path = os.path.join(self.temp_folder, _file)
            try:
                if os.path.isfile(_file_path):
                    os.unlink(_file_path)
                else:
                    shutil.rmtree(_file_path)
            except:
                log.exception()

    def handle(self, **options):
        self.force = options["force"]
        
        os.makedirs(self.temp_folder)
        for _lib in settings.STATIC_LIBS["libraries"]:
            self.get_library(_lib)
        shutil.rmtree(self.temp_folder)
