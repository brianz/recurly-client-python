from xml.etree import ElementTree


def xml(text):
    doc = ElementTree.fromstring(text)
    for el in doc.iter():
        if el.text and el.text.isspace():
            el.text = ''
        if el.tail and el.tail.isspace():
            el.tail = ''
    return ElementTree.tostring(doc, encoding='UTF-8')


