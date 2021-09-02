from pyQuARC.main import ARC

from pyQuARC.code.checker import Checker
from pyQuARC.code.downloader import Downloader

from pyQuARC.code.base_validator import BaseValidator
from pyQuARC.code.datetime_validator import DatetimeValidator
from pyQuARC.code.schema_validator import SchemaValidator
from pyQuARC.code.string_validator import StringValidator
from pyQuARC.code.url_validator import UrlValidator


with open("pyQuARC/version.txt") as version_file:
    __version__ = version_file.read().strip()

def get_version():
    return __version__
