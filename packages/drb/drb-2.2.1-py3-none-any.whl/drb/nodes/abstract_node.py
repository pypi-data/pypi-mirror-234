from __future__ import annotations

import abc
from typing import List, Union, Dict, Any, Tuple

from deprecated import deprecated

import drb.topics.resolver as resolver
from drb.core.node import DrbNode
from drb.core.predicate import Predicate
from drb.topics.resolver import DrbNodeList
from drb.exceptions.core import DrbException
from drb.utils.utils import get_name_namespace_index


class AbstractNode(DrbNode, abc.ABC):
    """
    This class regroup default implementation of DrbNode about the browsing
    using bracket and slash and also implementation of some utils functions.
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def __resolve_result(result: Union[DrbNode, List[DrbNode]]) \
            -> Union[DrbNode, List[DrbNode]]:
        """
        Resolves the given node(s)
        """
        if isinstance(result, DrbNode):
            try:
                return resolver.create(result)
            except DrbException:
                return result
        return DrbNodeList(result)

    def __len__(self):
        if not self.children:
            return 0
        return len(self.children)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.__resolve_result(self.children[item])
        if isinstance(item, slice):
            return self.__resolve_result(self.children[item])
        try:
            if isinstance(item, str):
                return self.__resolve_result(self._get_named_child(item))
            elif isinstance(item, tuple):
                key = get_name_namespace_index(item)
                return self.__resolve_result(
                    self._get_named_child(*key))
        except (DrbException, IndexError, TypeError, ValueError) as ex:
            raise KeyError(f'Invalid key {item}') from ex

        if isinstance(item, Predicate):
            children = [n for n in self.children if item.matches(n)]
            return DrbNodeList(children)
        raise TypeError(f"{type(item)} type not supported.")

    def __setitem__(self, key, value):
        if key is None:
            self.children.append(value)
        if isinstance(key, int):
            self.children[key] = value
        try:
            if isinstance(key, str):
                self.children[self._get_named_child_index(key)] = value
            elif isinstance(key, tuple):
                key = get_name_namespace_index(key)
                self.children[self._get_named_child_index(
                    *key)] = value
        except (DrbException, IndexError, TypeError) as ex:
            raise KeyError(f'Invalid key {key}') from ex

    def __delitem__(self, key):
        if isinstance(key, int):
            del self.children[key]
        try:
            if isinstance(key, str):
                del self.children[self._get_named_child_index(key)]
            elif isinstance(key, tuple):
                if len(key) == 2:
                    key = get_name_namespace_index(key)
                    del self.children[self._get_named_child_index(
                        *key)]
                    raise KeyError(f"Invalid key {key}.")
                else:
                    raise KeyError(f'Invalid key {key}')
        except (DrbException, IndexError, TypeError) as ex:
            raise KeyError(f'Invalid key {key}') from ex

    def _get_named_child_index(self, name: str, namespace_uri: str = None,
                               occurrence: int = 0) \
            -> int:
        """
        Retrieves one or more children via its given name and its namespace.

        Parameters:
            name (str): child name
            namespace_uri (str): child namespace URI (default: None)
            occurrence (int): child index or interval (default: 0)
        Returns:
            DrbNode | List[DrbNode] - requested child(ren)
        Raises:
            TypeError: if item is not an int or a slice
            IndexError: if item is out of range of found children
            DrbException: if no child following given criteria is found
        """
        occ = occurrence
        cpt = 0
        if self.namespace_aware or namespace_uri is not None:
            for x in self.children:
                if x.name == name and x.namespace_uri == namespace_uri:
                    if occ <= 0:
                        return cpt
                    occ -= 1
                cpt += 1
        else:
            for x in self.children:
                if x.name == name:
                    return cpt
                cpt += 1
        raise DrbException(f'No child found having name: {name} and'
                           f' namespace: {namespace_uri}')

    @property
    @deprecated(version='2.1.0',
                reason='Usage of the @ operator is recommended')
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self._attrs

    def _get_named_child(self, name: str, namespace_uri: str = None,
                         occurrence: Union[int, slice] = 0) -> \
            Union[DrbNode, List[DrbNode]]:
        """
        Retrieves one or more children via its given name and its namespace.

        Parameters:
            name (str): child name
            namespace_uri (str): child namespace URI (default: None)
            occurrence (int|slice): child index or interval (default: 0)
        Returns:
            DrbNode | List[DrbNode] - requested child(ren)
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
        return named_children[occurrence]

    def __eq__(self, other):
        if type(other) is type(self):
            return self.name == other.name and \
                   self.namespace_uri == other.namespace_uri and \
                   self.value == other.value
        else:
            return False

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if name is None and namespace is None:
            return len(self.children) > 0

        result = []
        if name is not None and namespace is not None:
            result = [x for x in self.children
                      if x.name == name and x.namespace_uri == namespace]
        if name is None:
            result = [x for x in self.children if x.namespace_uri == namespace]
        if namespace is None:
            result = [x for x in self.children if x.name == name]

        return len(result) > 0

    def __hash__(self):
        return super(DrbNode, self).__hash__()
