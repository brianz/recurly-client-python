from .base import Resource

from ..utils import ElementTree


def objects_for_push_notification(notification):
    """Decode a push notification with the given body XML.

    Returns a dictionary containing the constituent objects of the push
    notification. The kind of push notification is given in the ``"type"``
    member of the returned dictionary.

    """
    notification_el = ElementTree.fromstring(notification)
    objects = {'type': notification_el.tag}
    for child_el in notification_el:
        tag = child_el.tag
        res = Resource.value_for_element(child_el)
        objects[tag] = res
    return objects
