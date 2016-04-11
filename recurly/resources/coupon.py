from ..utils import urljoin
from ..utils import ElementTree

from .base import Resource
from .base import Page


class Coupon(Resource):
    """A coupon for a customer to apply to their account."""

    member_path = 'coupons/%s'
    collection_path = 'coupons'

    nodename = 'coupon'

    attributes = (
        'coupon_code',
        'name',
        'discount_type',
        'discount_percent',
        'discount_in_cents',
        'redeem_by_date',
        'invoice_description',
        'single_use',
        'applies_for_months',
        'duration',
        'temporal_unit',
        'temporal_amount',
        'max_redemptions',
        'applies_to_all_plans',
        'applies_to_non_plan_charges',
        'redemption_resource',
        'created_at',
        'plan_codes',
        'hosted_description',
        'max_redemptions_per_account',
        'coupon_type',
        'unique_code_template',
        'unique_coupon_codes',
    )

    @classmethod
    def value_for_element(cls, elem):
        if not elem or elem.tag != 'plan_codes' or elem.attrib.get('type') != 'array':
            return super(Coupon, cls).value_for_element(elem)

        return [code_elem.text for code_elem in elem]

    @classmethod
    def element_for_value(cls, attrname, value):
        if attrname != 'plan_codes':
            return super(Coupon, cls).element_for_value(attrname, value)

        elem = ElementTree.Element(attrname)
        elem.attrib['type'] = 'array'
        for code in value:
            code_el = ElementTree.Element('plan_code')
            code_el.text = code
            elem.append(code_el)

        return elem

    @classmethod
    def all_redeemable(cls, **kwargs):
        """Return a `Page` of redeemable coupons.

        This is a convenience method for `Coupon.all(state='redeemable')`.

        """
        return cls.all(state='redeemable', **kwargs)

    @classmethod
    def all_expired(cls, **kwargs):
        """Return a `Page` of expired coupons.

        This is a convenience method for `Coupon.all(state='expired')`.

        """
        return cls.all(state='expired', **kwargs)

    @classmethod
    def all_maxed_out(cls, **kwargs):
        """Return a `Page` of coupons that have been used the maximum
        number of times.

        This is a convenience method for `Coupon.all(state='maxed_out')`.

        """
        return cls.all(state='maxed_out', **kwargs)

    def has_unlimited_redemptions_per_account(self):
        return self.max_redemptions_per_account == None

    def generate(self, amount):
        elem = ElementTree.Element(self.nodename)
        elem.append(Resource.element_for_value('number_of_unique_codes', amount))

        url = urljoin(self._url, '%s/generate' % (self.coupon_code, ))
        body = ElementTree.tostring(elem, encoding='UTF-8')

        response = self.http_request(url, 'POST', body, { 'Content-Type':
            'application/xml; charset=utf-8' })

        if response.status not in (200, 201, 204):
            self.raise_http_error(response)

        return Page.page_for_url(response.getheader('Location'))

    def restore(self):
        url = urljoin(self._url, '%s/restore' % self.coupon_code)
        self.put(url)


class Redemption(Resource):
    """A particular application of a coupon to a customer account."""

    nodename = 'redemption'

    attributes = (
        'account_code',
        'single_use',
        'total_discounted_in_cents',
        'subscription_uuid',
        'currency',
        'created_at',
    )
