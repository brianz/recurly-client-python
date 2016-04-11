import collections
import logging
import time

from xml.etree import ElementTree

import six

from recurly.utils import urljoin

#from recurly.config import RecurlyConfig as config

from recurly.resources import Account
from recurly.resources import AddOn
from recurly.resources import Adjustment
from recurly.resources import BillingInfo
from recurly.resources import Coupon
from recurly.resources import Plan
from recurly.resources import Redemption
from recurly.resources import Subscription
from recurly.resources import SubscriptionAddOn
from recurly.resources import Transaction

from recurly.resources.base import Money

from recurly.errors import BadRequestError
from recurly.errors import NotFoundError
from recurly.errors import PageError
from recurly.errors import ValidationError
from recurly.errors import UnauthorizedError

#recurly.SUBDOMAIN = 'api'


import mock


def test_account_not_found(mock_config):
    account_code = 'testmock'

    Account.get(account_code)

    #with self.mock_request('account/does-not-exist.xml'):
    #self.assertRaises(NotFoundError, Account.get, account_code)


def fooey():
        account = Account(account_code=account_code)
        account.vat_number = '444444-UK'
        with self.mock_request('account/created.xml'):
            account.save()
        self.assertEqual(account._url, urljoin(base_uri(), 'accounts/%s' % account_code))
        self.assertEqual(account.vat_number, '444444-UK')
        self.assertEqual(account.vat_location_enabled, True)
        self.assertEqual(account.cc_emails,
                'test1@example.com,test2@example.com')

        with self.mock_request('account/list-active.xml'):
            active = Account.all_active()
        self.assertTrue(len(active) >= 1)
        self.assertEqual(active[0].account_code, account_code)

        with self.mock_request('account/exists.xml'):
            same_account = Account.get(account_code)
        self.assertTrue(isinstance(same_account, Account))
        self.assertTrue(same_account is not account)
        self.assertEqual(same_account.account_code, account_code)
        self.assertTrue(same_account.first_name is None)
        self.assertTrue(same_account.entity_use_code == 'I')
        self.assertEqual(same_account._url, urljoin(base_uri(), 'accounts/%s' % account_code))

        account.username = 'shmohawk58'
        account.email = 'larry.david'
        account.first_name = six.u('L\xe4rry')
        account.last_name = 'David'
        account.company_name = 'Home Box Office'
        account.accept_language = 'en-US'
        with self.mock_request('account/update-bad-email.xml'):
            try:
                account.save()
            except ValidationError as exc:
                self.assertTrue(isinstance(exc.errors, collections.Mapping))
                self.assertTrue('account.email' in exc.errors)
                suberror = exc.errors['account.email']
                self.assertEqual(suberror.symbol, 'invalid_email')
                self.assertTrue(suberror.message)
                self.assertEqual(suberror.message, suberror.message)
            else:
                self.fail("Updating account with invalid email address did not raise a ValidationError")

        account.email = 'larry.david@example.com'
        with self.mock_request('account/updated.xml'):
            account.save()

        with self.mock_request('account/deleted.xml'):
            account.delete()

        with self.mock_request('account/list-closed.xml'):
            closed = Account.all_closed()
        self.assertTrue(len(closed) >= 1)
        self.assertEqual(closed[0].account_code, account_code)

        with self.mock_request('account/list-active-when-closed.xml'):
            active = Account.all_active()
        self.assertTrue(len(active) < 1 or active[0].account_code != account_code)

        # Make sure we can reopen a closed account.
        with self.mock_request('account/reopened.xml'):
            account.reopen()
        try:
            with self.mock_request('account/list-active.xml'):
                active = Account.all_active()
            self.assertTrue(len(active) >= 1)
            self.assertEqual(active[0].account_code, account_code)
        finally:
            with self.mock_request('account/deleted.xml'):
                account.delete()

        # Make sure numeric account codes work.
        if self.test_id == 'mock':
            numeric_test_id = 58
        else:
            numeric_test_id = int(self.test_id)

        account = Account(account_code=numeric_test_id)
        with self.mock_request('account/numeric-created.xml'):
            account.save()
        try:
            self.assertEqual(account._url, urljoin(base_uri(), 'accounts/%d' % numeric_test_id))
        finally:
            with self.mock_request('account/numeric-deleted.xml'):
                account.delete()

        """Create an account with an account level address"""
        account = Account(account_code=account_code)
        account.address.address1 = '123 Main St'
        account.address.city = 'San Francisco'
        account.address.zip = '94105'
        account.address.state = 'CA'
        account.address.country = 'US'
        account.address.phone = '8015559876'
        with self.mock_request('account/created-with-address.xml'):
            account.save()
        self.assertEqual(account.address.address1, '123 Main St')
        self.assertEqual(account.address.city, 'San Francisco')
        self.assertEqual(account.address.zip, '94105')
        self.assertEqual(account.address.state, 'CA')
        self.assertEqual(account.address.country, 'US')
        self.assertEqual(account.address.phone, '8015559876')

        """Get taxed account"""
        with self.mock_request('account/show-taxed.xml'):
            account = Account.get(account_code)
            self.assertTrue(account.tax_exempt)
