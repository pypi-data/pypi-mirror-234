from drb.core.node import DrbNode
from drb.nodes.logical_node import DrbLogicalNode
from drb.core.factory import DrbFactory
from drb.exceptions.core import DrbFactoryException
from .node import XmlBaseNode, XmlNode
from io import BufferedIOBase, StringIO
from typing import Union
import os


class XmlNodeFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        if isinstance(node, XmlNode):
            return node
        if node.has_impl(BufferedIOBase):
            return XmlBaseNode(node, node.get_impl(BufferedIOBase))
        raise DrbFactoryException(f'Invalid node: {type(node)}')

    def create(self, source: Union[DrbNode, str]) -> DrbNode:
        if isinstance(source, str):
            base_node = DrbLogicalNode("/")
            if os.path.exists(source):
                return XmlBaseNode(base_node, source)[0]
            return XmlBaseNode(base_node, StringIO(source))[0]
        elif isinstance(source, DrbNode):
            return self._create(source)
        raise DrbFactoryException(f'Invalid parameter type: {type(source)}')
