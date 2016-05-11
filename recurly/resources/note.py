from .base import Resource


class Note(Resource):
    """A customer account's notes."""
    nodename = 'note'
    collection_path = 'notes'

    attributes = (
        'message',
        'created_at',
    )

    @classmethod
    def from_element(cls, elem):
        new_note = Note()
        for child_el in elem:
            if not child_el.tag:
                continue
            setattr(new_note, child_el.tag, child_el.text)
        return new_note


Note.register_nodename()
