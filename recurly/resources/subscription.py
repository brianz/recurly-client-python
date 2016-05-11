from .base import Resource

from ..config import RecurlyConfig as config
from ..utils import urljoin


class Subscription(Resource):
    """A customer account's subscription to your service."""

    member_path = 'subscriptions/%s'
    collection_path = 'subscriptions'

    nodename = 'subscription'

    attributes = (
        'uuid',
        'state',
        'plan_code',
        'coupon_code',
        'coupon_codes',
        'quantity',
        'activated_at',
        'canceled_at',
        'starts_at',
        'expires_at',
        'current_period_started_at',
        'current_period_ends_at',
        'trial_started_at',
        'trial_ends_at',
        'unit_amount_in_cents',
        'tax_in_cents',
        'tax_type',
        'tax_rate',
        'total_billing_cycles',
        'remaining_billing_cycles',
        'timeframe',
        'currency',
        'subscription_add_ons',
        'account',
        'pending_subscription',
        'net_terms',
        'collection_method',
        'po_number',
        'first_renewal_date',
        'bulk',
        'terms_and_conditions',
        'customer_notes',
        'vat_reverse_charge_notes',
        'bank_account_authorized_at',
        'redemptions',
    )
    sensitive_attributes = ('number', 'verification_value', 'bulk')

    def preview(self):
        if hasattr(self, '_url'):
            url = self._url + '/preview'
            return self.post(url)
        else:
            url = urljoin(config.get_base_uri(), self.collection_path) + '/preview'
            return self.post(url)

    def update_notes(self, **kwargs):
        """Updates the notes on the subscription without generating a change"""
        for key, val in kwargs.iteritems():
            setattr(self, key, val)
        url = urljoin(self._url, '%s/notes' % self.uuid)
        self.put(url)

    def _update(self):
        if not hasattr(self, 'timeframe'):
            self.timeframe = 'now'
        return super(Subscription, self)._update()

    def __getpath__(self, name):
        if name == 'plan_code':
            return 'plan/plan_code'
        else:
            return name

Subscription.register_nodename()
