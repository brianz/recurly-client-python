from .account import Account
from .address import Address
from .billing import BillingInfo
from .coupon import Coupon
from .coupon import Redemption
from .invoice import Adjustment
from .invoice import Invoice
from .note import Note
from .plan import AddOn
from .plan import SubscriptionAddOn
from .plan import Plan
from .subscription import Subscription
from .tax import TaxDetail
from .transaction import TransactionBillingInfo
from .transaction import TransactionAccount
from .transaction import TransactionDetails
from .transaction import TransactionError
from .transaction import Transaction


def objects_for_push_notification(notification):
    """Decode a push notification with the given body XML.

    Returns a dictionary containing the constituent objects of the push
    notification. The kind of push notification is given in the ``"type"``
    member of the returned dictionary.

    """
    from .base import Resource
    from ..utils import ElementTree
    notification_el = ElementTree.fromstring(notification)
    objects = {'type': notification_el.tag}
    for child_el in notification_el:
        tag = child_el.tag
        res = Resource.value_for_element(child_el)
        objects[tag] = res
    return objects
