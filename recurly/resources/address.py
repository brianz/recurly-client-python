from .base import Resource


__all__ = ('Address', )


class Address(Resource):

    nodename = 'address'

    attributes = (
        'address1',
        'address2',
        'city',
        'state',
        'zip',
        'country',
        'phone',
    )
