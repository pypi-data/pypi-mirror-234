from deprecated import deprecated
from drb.core.node import DrbNode
from drb.nodes.abstract_node import AbstractNode
from drb.exceptions.core import DrbNotImplementationException, DrbException
from typing import Any, List


class DrbXqueryItem(AbstractNode):

    def __init__(self, parent: DrbNode, name: str,
                 namespace_prefix: str, namespace_uri: str):
        super().__init__()
        self.name = name
        self.namespace_uri = namespace_uri
        self.parent = parent
        self._children: List[DrbNode] = []
        self.order_elt = []
        self.prefix = namespace_prefix

    @property
    @deprecated(
        version='2.1.0',
        reason='Please use bracket to access to node child(ren)'
    )
    def children(self) -> List[DrbNode]:
        return self._children

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')

    def get_named_child_list(self, name: str, namespace_uri: str = None) -> \
            List[DrbNode]:
        """
        Retrieves one or more children via its given name and its namespace.

        Parameters:
            name (str): child name
            namespace_uri (str): child namespace URI (default: None)
        Returns:
            List[DrbNode] - requested children
        Raises:
            TypeError: if item is not an int or a slice
            IndexError: if item is out of range of found children
            DrbException: if no child following given criteria is found
        """
        if self.namespace_aware or namespace_uri is not None:
            named_children = [x for x in self.children if x.name == name
                              and x.namespace_uri == namespace_uri]
        else:
            named_children = [x for x in self.children if x.name == name]
        if len(named_children) <= 0:
            raise DrbException(f'No child found having name: {name} and'
                               f' namespace: {namespace_uri}')
        return named_children

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.namespace_uri != other.namespace_uri:
            return False
        if self.value != other.value:
            return False

        return True

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __repr__(self):
        from drb.xquery.drb_xquery_res_to_string import XQueryResToString
        return XQueryResToString.drb_item_to_xml(self,
                                                 context=None,
                                                 dynamic_context=None,
                                                 namespace_declared=[])
