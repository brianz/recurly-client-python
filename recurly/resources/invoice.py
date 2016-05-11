from ..utils import urljoin
from ..utils import ElementTree

from .base import Resource
from .tax import TaxDetail

from ..config import RecurlyConfig as config


class Adjustment(Resource):
    """A charge or credit applied (or to be applied) to an account's invoice."""

    nodename = 'adjustment'
    member_path = 'adjustments/%s'

    attributes = (
        'uuid',
        'description',
        'accounting_code',
        'quantity',
        'unit_amount_in_cents',
        'discount_in_cents',
        'tax_in_cents',
        'tax_type',
        'tax_region',
        'tax_rate',
        'total_in_cents',
        'currency',
        'tax_exempt',
        'tax_code',
        'tax_details',
        'start_date',
        'end_date',
        'created_at',
        'type',
    )
    xml_attribute_attributes = ('type', )
    _classes_for_nodename = {'tax_detail': TaxDetail}

    # This can be removed when the `original_adjustment_uuid` is moved to a link
    def __getattr__(self, name):
        if name == 'original_adjustment':
            try:
                uuid = super(Adjustment, self).__getattr__('original_adjustment_uuid')
            except (AttributeError):
                return super(Adjustment, self).__getattr__(name)

            return lambda: Adjustment.get(uuid)
        else:
            return super(Adjustment, self).__getattr__(name)


class Invoice(Resource):
    """A payable charge to an account for the customer's charges and subscriptions."""

    member_path = 'invoices/%s'
    collection_path = 'invoices'

    nodename = 'invoice'

    attributes = (
        'uuid',
        'state',
        'invoice_number',
        'invoice_number_prefix',
        'po_number',
        'vat_number',
        'subtotal_in_cents',
        'tax_in_cents',
        'tax_type',
        'tax_rate',
        'total_in_cents',
        'currency',
        'created_at',
        'line_items',
        'transactions',
        'terms_and_conditions',
        'customer_notes',
        'address',
        'closed_at',
        'collection_method',
        'net_terms',
    )

    blacklist_attributes = (
        'currency',
    )

    def invoice_number_with_prefix(self):
        return '%s%s' % (self.invoice_number_prefix, self.invoice_number)

    @classmethod
    def all_open(cls, **kwargs):
        """Return a `Page` of open invoices.

        This is a convenience method for `Invoice.all(state='open')`.

        """
        return cls.all(state='open', **kwargs)

    @classmethod
    def all_collected(cls, **kwargs):
        """Return a `Page` of collected invoices.

        This is a convenience method for `Invoice.all(state='collected')`.

        """
        return cls.all(state='collected', **kwargs)

    @classmethod
    def all_failed(cls, **kwargs):
        """Return a `Page` of failed invoices.

        This is a convenience method for `Invoice.all(state='failed')`.

        """
        return cls.all(state='failed', **kwargs)

    @classmethod
    def all_past_due(cls, **kwargs):
        """Return a `Page` of past-due invoices.

        This is a convenience method for `Invoice.all(state='past_due')`.

        """
        return cls.all(state='past_due', **kwargs)

    @classmethod
    def pdf(cls, uuid):
        """Return a PDF of the invoice identified by the UUID

        This is a raw string, which can be written to a file with:
        `
            with open('invoice.pdf', 'w') as invoice_file:
                invoice_file.write(recurly.Invoice.pdf(uuid))
        `

        """
        url = urljoin(config.get_base_uri(), cls.member_path % (uuid,))
        pdf_response = cls.http_request(url, headers={'Accept': 'application/pdf'})
        return pdf_response.read()

    def refund_amount(self, amount_in_cents, refund_apply_order = 'credit'):
        amount_element = self.refund_open_amount_xml(amount_in_cents, refund_apply_order)
        return self._create_refund_invoice(amount_element)

    def refund(self, adjustments, refund_apply_order = 'credit'):
        adjustments_element = self.refund_line_items_xml(adjustments, refund_apply_order)
        return self._create_refund_invoice(adjustments_element)

    def refund_open_amount_xml(self, amount_in_cents, refund_apply_order):
        elem = ElementTree.Element(self.nodename)
        elem.append(Resource.element_for_value('refund_apply_order', refund_apply_order))
        elem.append(Resource.element_for_value('amount_in_cents',
            amount_in_cents))
        return elem

    def refund_line_items_xml(self, line_items, refund_apply_order):
        elem = ElementTree.Element(self.nodename)
        elem.append(Resource.element_for_value('refund_apply_order', refund_apply_order))

        line_items_elem = ElementTree.Element('line_items')

        for item in line_items:
            adj_elem = ElementTree.Element('adjustment')
            adj_elem.append(Resource.element_for_value('uuid',
                item['adjustment'].uuid))
            adj_elem.append(Resource.element_for_value('quantity',
            item['quantity']))
            adj_elem.append(Resource.element_for_value('prorate', item['prorate']))
            line_items_elem.append(adj_elem)

        elem.append(line_items_elem)
        return elem

    def _create_refund_invoice(self, element):
        url = urljoin(self._url, '%s/refund' % (self.invoice_number, ))
        body = ElementTree.tostring(element, encoding='UTF-8')

        refund_invoice = Invoice()
        refund_invoice.post(url, body)

        return refund_invoice

    def redemption(self):
        try:
            return self.redemptions()[0]
        except AttributeError:
            raise AttributeError("redemption")


Adjustment.register_nodename()
Invoice.register_nodename()
