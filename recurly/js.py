import base64
import hashlib
import hmac
import os
import re
import six
import time

from .utils import quote_plus
from .utils import urljoin

from .config import base_uri
from .config import RecurlyConfig
from .resources.base import Resource


def sign(*records):
    """ Signs objects or data dictionary with your Recurly.js private key."""
    if RecurlyConfig.PRIVATE_KEY is None:
        raise ValueError("Recurly.js private key is not set.")
    records = list(records)
    try:
        data = records.pop() if type(records[-1]) is dict else {}
    except IndexError:
        data = {}
    for record in records:
        data[record.__class__.nodename] = record.__dict__
    if 'timestamp' not in data:
        data['timestamp'] = int(time.time())
    if 'nonce' not in data:
        data['nonce'] = re.sub(six.b('\W+'), six.b(''), base64.b64encode(os.urandom(32)))
    unsigned = to_query(data)
    signed = hmac.new(six.b(RecurlyConfig.PRIVATE_KEY), six.b(unsigned), hashlib.sha1).hexdigest()
    return '|'.join([signed, unsigned])


def fetch(token):
    url = urljoin(base_uri(), 'recurly_js/result/%s' % token)
    resp, elem = Resource.element_for_url(url)
    cls = Resource.value_for_element(elem)
    return cls.from_element(elem)


def to_query(object, key=None):
    """ Dumps a dictionary into a nested query string."""
    object_type = type(object)
    if object_type is dict:
        return '&'.join([to_query(object[k], '%s[%s]' % (key, k) if key else k) for k in sorted(object)])
    elif object_type in (list, tuple):
        return '&'.join([to_query(o, '%s[]' % key) for o in object])
    else:
        return '%s=%s' % (quote_plus(str(key)), quote_plus(str(object)))
