from typing import Iterator
from lxml.etree import _Element as Element, QName


class LXMLTreeAsDictReadOnly:

    __slots__ = (
        '_root',
        '_iter',
        '_siblings',
    )

    def __init__(self, root: Element, iter: Iterator[Element] = None):
      self._root = root
      self._iter = iter
      self._siblings = None

    def __getitem__(self, key: str) -> 'LXMLTreeAsDictReadOnly':
        if key == '#text':
            if self._root is None:
                return None

            return self._root.text

        elif key[0] == '@':
            if self._root is None:
                return None

            return self._root.attrib.get(key[1:])

        if self._root is None:
            return self

        iter = self._find_nodes(key)
        return LXMLTreeAsDictReadOnly(next(iter, None), iter)

    def _find_nodes(self, key: str) -> Iterator[Element]:
        ns, tag = key.split(':') if ':' in key else ('', key)

        if ns:
            for node in self._root:
                uri = node.nsmap.get(ns, '')

                if node.tag == f'{{{uri}}}{tag}':
                    yield node
        else:
            for node in self._root:
                if node.tag == tag:
                    yield node

    def __iter__(self) -> Iterator['LXMLTreeAsDictReadOnly']:
        if isinstance(self._siblings, list):
            for node in self._siblings:
                yield LXMLTreeAsDictReadOnly(node)
            return

        if self._root is not None:
            self._siblings = [self._root]
            yield LXMLTreeAsDictReadOnly(self._root)

        if self._iter is not None:
            for node in self._iter:
                self._siblings.append(node)
                yield LXMLTreeAsDictReadOnly(node)

    def __len__(self) -> int:
        if self._root is None:
            return 0

        self._siblings = [self._root]

        if self._iter is not None:
            for node in self._iter:
                self._siblings.append(node)

        return len(self._siblings)

    def __dict__(self) -> dict:
        if self._root is None:
            return dict()

        key, value = self._export_root(self._root)
        return {key: value}

    def _export_root(self, root: Element) -> dict:
        data = {}

        for node in root:
            self._export_node(data, node)

        for key in root.attrib:
            data[f'@{key}'] = root.attrib[key]

        text = (root.text or '').strip() or None

        if data:
            if text:
                data['#text'] = text
        else:
            data = text

        tag = QName(root).localname
        tag = f'{root.prefix}:{tag}' if root.prefix else tag
        return tag, data

    def _export_node(self, data: dict, node: Element) -> None:
        sub_tag, sub_data = self._export_root(node)

        if sub_tag in data:
            if isinstance(data[sub_tag], list):
                data[sub_tag].append(sub_data)
            else:
                data[sub_tag] = [data[sub_tag], sub_data]
        else:
            data[sub_tag] = sub_data

    def __bool__(self) -> bool:
        return self._root is not None

    def __eq__(self, other) -> bool:
        if isinstance(other, LXMLTreeAsDictReadOnly):
            return self._root == other._root

        return self._root == other

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'LXMLTreeAsDictReadOnly(root={self._root})'
