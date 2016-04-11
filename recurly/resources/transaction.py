from .base import Resource


class TransactionBillingInfo(Resource):
    node_name = 'billing_info'
    attributes = (
        'first_name',
        'last_name',
        'address1',
        'address2',
        'city',
        'state',
        'country',
        'zip',
        'phone',
        'vat_number',
        'first_six',
        'last_four',
        'card_type',
        'month',
        'year',
        'transaction_uuid',
    )


class TransactionAccount(Resource):
    node_name = 'account'
    attributes = (
        'first_name',
        'last_name',
        'company',
        'email',
        'account_code',
    )
    _classes_for_nodename = {'billing_info': TransactionBillingInfo}


class TransactionDetails(Resource):
    node_name = 'details'
    attributes = ('account')
    _classes_for_nodename = {'account': TransactionAccount}


class TransactionError(Resource):
    node_name = 'transaction_error'
    attributes = (
        'id',
        'merchant_message',
        'error_caterogy',
        'customer_message',
        'error_code',
        'gateway_error_code',
    )


class Transaction(Resource):
    """An immediate one-time charge made to a customer's account."""

    member_path = 'transactions/%s'
    collection_path = 'transactions'

    nodename = 'transaction'

    attributes = (
        'uuid',
        'action',
        'account',
        'currency',
        'amount_in_cents',
        'tax_in_cents',
        'status',
        'reference',
        'test',
        'voidable',
        'description',
        'refundable',
        'cvv_result',
        'avs_result',
        'avs_result_street',
        'avs_result_postal',
        'created_at',
        'details',
        'transaction_error',
        'type',
        'ip_address',
        'tax_exempt',
        'tax_code',
        'accounting_code',
    )
    xml_attribute_attributes = ('type',)
    sensitive_attributes = ('number', 'verification_value',)
    _classes_for_nodename = {
        'details': TransactionDetails,
        'transaction_error': TransactionError
    }

    def _handle_refund_accepted(self, response):
        if response.status != 202:
            self.raise_http_error(response)

        self._refund_transaction_url = response.getheader('Location')
        return self

    def get_refund_transaction(self):
        """Retrieve the refund transaction for this transaction, immediately
        after refunding.

        After calling `refund()` to refund a transaction, call this method to
        retrieve the new transaction representing the refund.

        """
        try:
            url = self._refund_transaction_url
        except AttributeError:
            raise ValueError("No refund transaction is available for this transaction")

        resp, elem = self.element_for_url(url)
        value = self.value_for_element(elem)
        return value

    def refund(self, **kwargs):
        """Refund this transaction.

        Calling this method returns the refunded transaction (that is,
        ``self``) if the refund was successful, or raises a `ResponseError` if
        an error occurred requesting the refund. After a successful call to
        `refund()`, to retrieve the new transaction representing the refund,
        use the `get_refund_transaction()` method.

        """
        # Find the URL and method to refund the transaction.
        try:
            selfnode = self._elem
        except AttributeError:
            raise AttributeError('refund')

        url, method = None, None
        for anchor_elem in selfnode.findall('a'):
            if anchor_elem.attrib.get('name') == 'refund':
                url = anchor_elem.attrib['href']
                method = anchor_elem.attrib['method'].upper()

        if url is None or method is None:
            raise AttributeError("refund")  # should do something more specific probably

        actionator = self._make_actionator(url, method, extra_handler=self._handle_refund_accepted)
        return actionator(**kwargs)


Transaction._classes_for_nodename['transaction'] = Transaction
