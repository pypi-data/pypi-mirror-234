"""Init."""
from dkist_service_configuration import logger  # first import to set logging.BasicConfig
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = "unknown"
