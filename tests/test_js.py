import re
import time

import mock
import pytest

from recurly.resources.resources import Account
from recurly.js import to_query
from recurly.js import sign


@pytest.fixture
def private_key(request):
    patcher = mock.patch('recurly.js.RecurlyConfig')
    config = patcher.start()
    config.PRIVATE_KEY = '0cc86846024a4c95a5dfd3111a532d13'
    request.addfinalizer(patcher.stop)
    return config



def test_serialize(private_key):
    message = {
        'a': {
            'a1': 123,
            'a2': 'abcdef',
        },
        'b': [1,2,3],
        'c': {
            '1':4,
            '2':5,
            '3':6,
        },
        'd': ':',
    }
    assert to_query(message) == 'a%5Ba1%5D=123&a%5Ba2%5D=abcdef&b%5B%5D=1&b%5B%5D=2&b%5B%5D=3&c%5B1%5D=4&c%5B2%5D=5&c%5B3%5D=6&d=%3A'


def test_nonce_in_sign(private_key):
    assert re.search('nonce=', sign())

def test_timestamp_in_sign(private_key):
    assert re.search('timestamp=', sign())

def test_sign_timestamp_and_nonce(private_key):
    assert sign({'timestamp': 1312701386, 'nonce': 1}) == \
        '015662c92688f387159bcac9bc1fb250a1327886|nonce=1&timestamp=1312701386'

def test_sign_account_with_extras(private_key):
    assert sign(Account(account_code='1'), {'timestamp': 1312701386, 'nonce': 1}) == \
        '82bcbbd4deb8b1b663b7407d9085dc67e2922df7|account%5Baccount_code%5D=1&nonce=1&timestamp=1312701386'
