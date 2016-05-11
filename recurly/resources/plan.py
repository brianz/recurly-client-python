from .base import Resource

from ..utils import urljoin


class AddOn(Resource):
    """An additional benefit a customer subscribed to a particular plan can also subscribe to."""
    nodename = 'add_on'

    attributes = (
        'add_on_code',
        'name',
        'display_quantity_on_hosted_page',
        'display_quantity',
        'default_quantity',
        'accounting_code',
        'unit_amount_in_cents',
        'tax_code',
        'created_at',
    )


class SubscriptionAddOn(Resource):
    """A plan add-on as added to a customer's subscription.

    Use these instead of `AddOn` instances when specifying a `Subscription` instance's
    `subscription_add_ons` attribute.

    """
    nodename = 'subscription_add_on'
    inherits_currency = True

    attributes = (
        'add_on_code',
        'quantity',
        'unit_amount_in_cents',
        'address',
    )

class Plan(Resource):
    """A service level for your service to which a customer account can subscribe."""
    member_path = 'plans/%s'
    collection_path = 'plans'

    nodename = 'plan'

    attributes = (
        'plan_code',
        'name',
        'description',
        'success_url',
        'cancel_url',
        'display_donation_amounts',
        'display_quantity',
        'display_phone_number',
        'bypass_hosted_confirmation',
        'unit_name',
        'payment_page_tos_link',
        'plan_interval_length',
        'plan_interval_unit',
        'trial_interval_length',
        'trial_interval_unit',
        'accounting_code',
        'setup_fee_accounting_code',
        'created_at',
        'tax_exempt',
        'tax_code',
        'unit_amount_in_cents',
        'setup_fee_in_cents',
        'total_billing_cycles',
    )

    def get_add_on(self, add_on_code):
        """Return the `AddOn` for this plan with the given add-on code."""
        url = urljoin(self._url, '%s/add_ons/%s' % (self.plan_code, add_on_code))
        resp, elem = AddOn.element_for_url(url)
        return AddOn.from_element(elem)

    def create_add_on(self, add_on):
        """Make the given `AddOn` available to subscribers on this plan."""
        url = urljoin(self._url, '%s/add_ons' % self.plan_code)
        return add_on.post(url)


AddOn.register_nodename()
SubscriptionAddOn.register_nodename()
Plan.register_nodename()
