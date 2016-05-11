from .base import Resource


class BillingInfo(Resource):
    """A set of billing information for an account."""

    nodename = 'billing_info'

    attributes = (
        'type',
        'name_on_account',
        'first_name',
        'last_name',
        'number',
        'verification_value',
        'year',
        'month',
        'start_month',
        'start_year',
        'issue_number',
        'company',
        'address1',
        'address2',
        'city',
        'state',
        'zip',
        'country',
        'phone',
        'vat_number',
        'ip_address',
        'ip_address_country',
        'card_type',
        'first_six',
        'last_four',
        'paypal_billing_agreement_id',
        'amazon_billing_agreement_id',
        'token_id',
        'account_type',
        'routing_number',
        'account_number',
        'currency',
    )
    sensitive_attributes = ('number', 'verification_value', 'account_number')
    xml_attribute_attributes = ('type',)

BillingInfo.register_nodename()
