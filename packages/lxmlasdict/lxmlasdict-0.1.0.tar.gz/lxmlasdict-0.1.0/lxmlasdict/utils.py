from lxml import etree
from lxml.etree import _Element as Element
from lxmlasdict.base import LXMLTreeAsDictReadOnly


def from_string(xml: str) -> LXMLTreeAsDictReadOnly:
    xml = xml.encode('utf-8')
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(xml, parser)

    return LXMLTreeAsDictReadOnly(root)


def from_file(path: str) -> LXMLTreeAsDictReadOnly:
    file = open(path, 'r')
    xml = file.read()
    file.close()
    
    return from_string(xml)


def to_dict(obj: LXMLTreeAsDictReadOnly) -> dict:
    return obj.__dict__()
