import sys

__version__ = '2.2.19'
__python_version__ = '.'.join(map(str, sys.version_info[:3]))


class RecurlyConfig(object):
    USER_AGENT = 'recurly-python/%s; python %s' % (__version__, __python_version__)

    # The API endpoint to send requests to
    BASE_URI = 'https://%s.recurly.com/v2/'

    # The subdomain of the site authenticating API requests
    SUBDOMAIN = 'api'

    # The API key to use when authenticating API requests."""
    API_KEY = None

    # The API version to use when making API requests."""
    API_VERSION = '2.1'

    # A file contianing a set of concatenated certificate authority certs
    # for validating the server against.
    CA_CERTS_FILE = None

    # The currency to use creating `Money` instances when one is not specified."""
    DEFAULT_CURRENCY = 'USD'

    # The number of seconds after which to timeout requests to the Recurly API.
    # If unspecified, the global default timeout is used.
    SOCKET_TIMEOUT_SECONDS = None

    PRIVATE_KEY = None


def base_uri():
    if RecurlyConfig.SUBDOMAIN is None:
        raise ValueError('recurly.SUBDOMAIN not set')

    return RecurlyConfig.BASE_URI % (RecurlyConfig.SUBDOMAIN, )


def api_version():
    return RecurlyConfig.API_VERSION
