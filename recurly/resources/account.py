import logging

from ..utils import urljoin
from ..utils import ElementTree

from .base import Resource

from .address import Address
from .billing import BillingInfo
from .invoice import Invoice
from .note import Note


__all__ = ('Account', )


class Account(Resource):
    """A customer account."""

    member_path = 'accounts/%s'
    collection_path = 'accounts'
    nodename = 'account'

    attributes = (
        'account_code',
        'username',
        'email',
        'first_name',
        'last_name',
        'company_name',
        'vat_number',
        'tax_exempt',
        'entity_use_code',
        'accept_language',
        'cc_emails',
        'created_at',
    )

    _classes_for_nodename = {'address': Address}

    sensitive_attributes = ('number', 'verification_value',)

    def to_element(self):
        elem = super(Account, self).to_element()

        # Make sure the account code is always included in a serialization.
        if 'account_code' not in self.__dict__:  # not already included
            try:
                account_code = self.account_code
            except AttributeError:
                pass
            else:
                elem.append(self.element_for_value('account_code', account_code))
        if 'billing_info' in self.__dict__:
            elem.append(self.billing_info.to_element())
        if 'address' in self.__dict__:
            elem.append(self.address.to_element())
        return elem

    @classmethod
    def all_active(cls, **kwargs):
        """Return a `Page` of active customer accounts.

        This is a convenience method for `Account.all(state='active')`.

        """
        return cls.all(state='active', **kwargs)

    @classmethod
    def all_closed(cls, **kwargs):
        """Return a `Page` of closed customer accounts.

        This is a convenience method for `Account.all(state='closed')`.

        """
        return cls.all(state='closed', **kwargs)

    @classmethod
    def all_past_due(cls, **kwargs):
        """Return a `Page` of past-due customer accounts.

        This is a convenience method for `Account.all(state='past_due').

        """
        return cls.all(state='past_due', **kwargs)

    @classmethod
    def all_subscribers(cls, **kwargs):
        """Return a `Page` of customer accounts that are subscribers.

        This is a convenience method for `Account.all(state='subscriber').

        """
        return cls.all(state='subscriber', **kwargs)

    @classmethod
    def all_non_subscribers(cls, **kwargs):
        """Return a `Page` of customer accounts that are not subscribers.

        This is a convenience method for `Account.all(state='non_subscriber').

        """
        return cls.all(state='non_subscriber', **kwargs)

    def __getattr__(self, name):
        if name == 'billing_info':
            try:
                billing_info_url = self._elem.find('billing_info').attrib['href']
            except (AttributeError, KeyError):
                raise AttributeError(name)
            resp, elem = BillingInfo.element_for_url(billing_info_url)
            return BillingInfo.from_element(elem)
        try:
            return super(Account, self).__getattr__(name)
        except AttributeError:
            if name == 'address':
                self.address = Address()
                return self.address
            else:
              raise AttributeError(name)

    def charge(self, charge):
        """Charge (or credit) this account with the given `Adjustment`."""
        url = urljoin(self._url, '%s/adjustments' % self.account_code)
        return charge.post(url)

    def invoice(self, **kwargs):
        """Create an invoice for any outstanding adjustments this account has."""
        url = urljoin(self._url, '%s/invoices' % self.account_code)

        if kwargs:
            response = self.http_request(url, 'POST', Invoice(**kwargs), {'Content-Type':
                'application/xml; charset=utf-8'})
        else:
            response = self.http_request(url, 'POST')

        if response.status != 201:
            self.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        elem = ElementTree.fromstring(response_xml)

        invoice = Invoice.from_element(elem)
        invoice._url = response.getheader('Location')
        return invoice

    def build_invoice(self):
        """Preview an invoice for any outstanding adjustments this account has."""
        url = urljoin(self._url, '%s/invoices/preview' % self.account_code)

        response = self.http_request(url, 'POST')
        if response.status != 200:
            self.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        elem = ElementTree.fromstring(response_xml)

        invoice = Invoice.from_element(elem)
        return invoice

    def notes(self):
        """Fetch Notes for this account."""
        url = urljoin(self._url, '%s/notes' % self.account_code)
        return Note.paginated(url)

    def redemption(self):
        try:
            return self.redemptions()[0]
        except AttributeError:
            raise AttributeError("redemption")

    def reopen(self):
        """Reopen a closed account."""
        url = urljoin(self._url, '%s/reopen' % self.account_code)
        response = self.http_request(url, 'PUT')
        if response.status != 200:
            self.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        self.update_from_element(ElementTree.fromstring(response_xml))

    def subscribe(self, subscription):
        """Create the given `Subscription` for this existing account."""
        url = urljoin(self._url, '%s/subscriptions' % self.account_code)
        return subscription.post(url)

    def update_billing_info(self, billing_info):
        """Change this account's billing information to the given `BillingInfo`."""
        url = urljoin(self._url, '%s/billing_info' % self.account_code)
        response = billing_info.http_request(url, 'PUT', billing_info,
            {'Content-Type': 'application/xml; charset=utf-8'})
        if response.status == 200:
            pass
        elif response.status == 201:
            billing_info._url = response.getheader('Location')
        else:
            billing_info.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        billing_info.update_from_element(ElementTree.fromstring(response_xml))


Account.register_nodename()
