import logging
from optparse import make_option
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from fetchstatic.fetcher import StaticFetcher

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Download libraries from internet to static folder"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--force", action="store_true",
            dest="force", default=False,
            help="Overwrite existing files while downloading",
        )
        parser.add_argument("directory", help="Target directory path")

    def handle(self, *args, **options):
        self.force = options["force"]
        _static_dir = options["directory"]
        _temp_dir = os.path.join(_static_dir, "__temp")

        _fetcher = StaticFetcher(settings.STATIC_LIBS, _static_dir, _temp_dir)
        _fetcher.fetch_all(options["force"], log)
