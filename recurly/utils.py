from xml.etree import ElementTree

try:
    from six.moves.urllib.parse import urljoin
    from six.moves.urllib.parse import urlsplit
except ImportError:
    from urlparse import urljoin
    from urlparse import urlsplit

try:
    from six.moves.urllib.parse import quote_plus
    from six.moves.urllib.parse import urlencode
except ImportError:
    from urllib import quote_plus
    from urllib import urlencode
