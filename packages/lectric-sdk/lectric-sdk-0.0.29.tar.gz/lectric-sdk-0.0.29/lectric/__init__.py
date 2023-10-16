""" A client library (SDK) for accessing Lectric a Vector Database service """
from .client import AuthenticatedClient, Client
from .models import *
from .api import *
from .types import *
from .lectric_client import LectricClient
from .lectric_types import *
import os


with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION")) as version_fh:
  __version__ = version_fh.read().strip()

def version():
    return __version__
