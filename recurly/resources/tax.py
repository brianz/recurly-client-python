from .base import Resource


class TaxDetail(Resource):

    """A charge's tax breakdown"""

    nodename = 'taxdetail'
    inherits_currency = True

    attributes = (
        'name',
        'type',
        'tax_rate',
        'tax_in_cents',
    )

TaxDetail.register_nodename()
