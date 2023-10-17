from __future__ import annotations
import io
import xml.etree.ElementTree

from deprecated import deprecated

from drb.core.node import DrbNode
from drb.nodes.abstract_node import AbstractNode
from drb.core.path import ParsedPath
from drb.exceptions.core import DrbNotImplementationException, DrbException
from typing import Any, Union, List, Tuple, IO
from xml.etree.ElementTree import parse, Element, dump
from io import BufferedIOBase, RawIOBase, IOBase
import re


def extract_namespace_name(value: str) -> Tuple[str, str]:
    """
    Extracts namespace and name from a tag of a Element

    Parameters:
        value: XML element tag

    Returns:
          tuple: a tuple containing the extracted namespace and name
    """
    ns, name = re.match(r'({.*})?(.*)', value).groups()
    if ns is not None:
        ns = ns[1:-1]
    return ns, name


class XmlNode(AbstractNode):

    def __init__(self, element: Element, parent: DrbNode = None, **kwargs):
        super().__init__()
        namespace_uri, name = extract_namespace_name(element.tag)
        self.name = name
        self.namespace_uri = namespace_uri
        if self.namespace_uri is None:
            self.namespace_uri = element.get('xmlns', None)
        if self.namespace_uri is None and parent is not None:
            self.namespace_uri = parent.namespace_uri

        self.parent: DrbNode = parent
        self._children = None
        self._elem: Element = element
        self._occurrence = kwargs.get('occurrence', 1)
        if not self.has_child():
            self.value = self._elem.text
        self.__init_attr()
        self.add_impl(io.BytesIO, self.__to_bytes_stream)
        self.add_impl(str, self.__to_str)

    def __init_attr(self):
        for k, v in self._elem.attrib.items():
            ns, name = extract_namespace_name(k)
            if name != 'xmlns' or ns is not None:
                self.__imatmul__((name, ns, v))

    @property
    @deprecated(version='2.1.0', reason='Usage of the bracket is recommended')
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = []
            occurrences = {}
            for elem in self._elem:
                namespace, name = extract_namespace_name(elem.tag)
                occurrence = occurrences.get(name, 0) + 1
                occurrences[name] = occurrence
                self._children.append(
                    XmlNode(elem, self, occurrence=occurrence))
        return self._children

    def _get_named_child(self, name: str, namespace_uri: str = None,
                         occurrence: Union[int, slice] = 0) -> \
            Union[DrbNode, List[DrbNode]]:
        tag = f'ns:{name}'
        named_children = self._elem.findall(tag, {'ns': '*'})

        if len(named_children) == 0:
            raise DrbException(f'No child found having name: {name} and'
                               f' namespace: {namespace_uri}')

        children = [XmlNode(named_children[i], self, occurrence=i+1)
                    for i in range(len(named_children))]
        if self.namespace_aware or namespace_uri is not None:
            children = list(
                filter(lambda n: n.namespace_uri == namespace_uri, children))
        return children[occurrence]

    def close(self) -> None:
        pass

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if name is None and namespace is None:
            return len(self.children) > 0

        tag = f'ns:{name}'

        if namespace is None:
            if not self.namespace_aware:
                ns = {'ns': "*"}
            else:
                tag = name
                ns = {}
        else:
            ns = {'ns': namespace}

        found = self._elem.find(tag, ns)

        if found is not None:
            return True
        else:
            return False

    @classmethod
    def __to_str(cls, node: XmlNode):
        return xml.etree.ElementTree.tostring(node._elem).decode()

    @classmethod
    def __to_bytes_stream(cls, node: XmlNode):
        return io.BytesIO(xml.etree.ElementTree.tostring(node._elem))

    def __hash__(self):
        return hash(self.path.name) + hash(self._occurrence)


class XmlBaseNode(AbstractNode):
    """
    This class represents a single node of a tree of data.
    When the data came from another implementation.

    Parameters:
        node (DrbNode): the base node of this node.
        source(Union[BufferedIOBase, RawIOBase, IO]): The xml data.
    """
    def __init__(self, node: DrbNode, source: Union[BufferedIOBase, IO]):
        super().__init__()
        self.__base_node = node
        self.name = node.name
        self.namespace_uri = node.namespace_uri
        self.value = node.value
        self.parent = node.parent
        self.__source = source
        self.__xml_node = XmlNode(parse(source).getroot(), node)
        if isinstance(source, IOBase):
            self.__source.close()
        for n, ns in node.attribute_names():
            self.__imatmul__((n, ns, node @ (n, ns)))

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    @property
    def path(self) -> ParsedPath:
        return self.__base_node.path

    def impl_capabilities(self) -> List[Tuple[type, str]]:
        return self.__base_node.impl_capabilities()

    @property
    @deprecated(version='2.1.0', reason='Usage of the bracket is recommended')
    def children(self) -> List[DrbNode]:
        return [self.__xml_node]

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if name is None and namespace is None:
            return True

        if namespace is not None or self.namespace_aware:
            if self.__xml_node.namespace_uri != namespace:
                return False

        if self.__xml_node.name == name:
            return True

        return False

    @deprecated(version='2.1.0',
                reason='Usage of the @ operator is recommended')
    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        return self.__base_node.get_attribute(name, namespace_uri)

    def has_impl(self, impl: type, identifier: str = None) -> bool:
        return self.__base_node.has_impl(impl, identifier)

    def get_impl(self, impl: type, identifier: str = None, **kwargs) -> Any:
        return self.__base_node.get_impl(impl, identifier, **kwargs)

    def _get_named_child(self, name: str, namespace_uri: str = None,
                         occurrence: Union[int, slice] = 0) -> \
            Union[DrbNode, List[DrbNode]]:
        if self.__xml_node.name == name and \
                ((not self.namespace_aware and namespace_uri is None)
                 or self.__xml_node.namespace_uri == namespace_uri):
            return [self.__xml_node][occurrence]
        raise DrbException(f'No child found having name: {name} and'
                           f' namespace: {namespace_uri}')

    def close(self) -> None:
        self.__base_node.close()
