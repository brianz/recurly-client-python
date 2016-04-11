import six

from recurly.errors import ConfigurationError

from recurly.config import RecurlyConfig as config


def test_authentication(self):
    config.API_KEY = None

    account_code = 'test%s' % self.test_id
    try:
        Account.get(account_code)
    except UnauthorizedError as exc:
        pass
    else:
        self.fail("Updating account with invalid email address did not raise a ValidationError")


def test_config_string_types(self):
    config.API_KEY = six.u('\xe4 unicode string')

    account_code = 'test%s' % self.test_id
    try:
        Account.get(account_code)
    except ConfigurationError as exc:
        pass
    else:
        self.fail("Updating account with invalid email address did not raise a ValidationError")

