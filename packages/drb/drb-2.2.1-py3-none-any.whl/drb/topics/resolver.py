import os
import os.path
import logging
import pathlib
import sys
import re

from urllib.parse import urlparse
from typing import List, Optional, Tuple, Union

from drb.core.node import DrbNode
from drb.core.factory import DrbFactory, FactoryLoader
from drb.topics.topic import DrbTopic, TopicCategory
from drb.exceptions.core import DrbFactoryException, DrbException
from drb.nodes.url_node import UrlNode
from drb.topics.dao import ManagerDao
from drb.addons.addon import AddonManager


logger = logging.getLogger('DrbResolver')


def _is_remote_url(parsed_path):
    """
    Checks if the given parsed URL is a remote URL
    """
    return parsed_path.scheme != '' and parsed_path.scheme != 'file'


def forced_factory(topic: DrbTopic, node: DrbNode) -> Optional[DrbNode]:
    if topic.forced and topic.factory is not None:
        try:
            new_node = FactoryLoader().get_factory(
                topic.factory).create(node)
        except Exception as e:
            return node
        return new_node
    return node


class _DrbFactoryResolver(DrbFactory):
    """ The factory resolver

    The factory resolver aims to parametrize the selection of the factory
    able to resolves the nodes according to its physical input.
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(_DrbFactoryResolver, cls).__new__(cls)

        return cls.__instance

    def _create(self, node: DrbNode) -> DrbNode:
        topic, n = self.resolve(node)
        return n

    def __retrieve_protocol(self, node: DrbNode) -> Optional[DrbTopic]:
        """
        Retrieves the protocol topic associated to the given node.

        Parameters:
            node (DrbNode): node which need to be resolved
        Returns:
            DrbNode: a protocol topic associated to the given node or
                     ``None`` if no protocol item class is found.
        """
        for protocol in ManagerDao().get_drb_topics_by_category(
                TopicCategory.PROTOCOL):
            node = forced_factory(protocol, node)
            if protocol.matches(node):
                return protocol
        return None

    def __retrieve_container(self, node: DrbNode) -> Tuple[DrbTopic, DrbNode]:
        """
        Retrieves the container signature associated to the given node.

        Parameters:
            node (DrbNode): node which need to be resolved
        Returns:
            DrbTopic, DrbNode: A topic matching the given node and the
                                associated node
        """
        highest_containers = [x for x in
                              ManagerDao().get_drb_topics_by_category(
                                  TopicCategory.CONTAINER)
                              if x.subClassOf is None]

        for s in highest_containers:
            node = forced_factory(s, node)
            if s.matches(node):
                return self.__finest_drb_topic(node, s)
        return None, node

    def __finest_drb_topic(self, node: DrbNode, finest: DrbTopic) \
            -> Tuple[DrbTopic, DrbNode]:
        """
        Retrieves the finest topic associated to the given node.

        Parameters:
            node (DrbNode): node which need to be resolved
            finest (DrbTopic): current finest topic matching the given
                                node
        Returns:
            DrbTopic: the finest topic matching the given node
        """
        topics = [x for x in ManagerDao().get_all_drb_topics()
                  if x.subClassOf is not None if x.subClassOf[0] == finest.id]
        for topic in topics:
            node = forced_factory(topic, node)
            if topic.matches(node):
                n = node
                if topic.factory is not None:
                    n = FactoryLoader().get_factory(
                        topic.factory).create(node)
                return self.__finest_drb_topic(n, topic)
        return finest, node

    def __retrieve_formatting(self, node) -> Optional[DrbTopic]:
        """
        Retrieves the formatting topic associated to the given node.

        Parameters:
            node (DrbNode): node which need to be resolved
        Returns:
            DrbTopic: A formatting topic matching the given node,
                       otherwise ``None``
        """
        for topic in ManagerDao().get_drb_topics_by_category(
                TopicCategory.FORMATTING):
            node = forced_factory(topic, node)
            if topic.matches(node):
                return topic
        return None

    def __create_from_url(self, url: str, curl: str = None,
                          path: List[str] = None) -> DrbNode:
        """
        Parses the given url to retrieve the targeted resource to open as node
        This method allows to target an inner resource (e.g. an XML file in a
        zipped data from an HTTP URL)

        Parameters:
            url (str): targeted resource URL
            curl (str): current URL (internal processing)
            path (list): remaining path of the given URL (internal processing)
        Returns:
            DrbNode: A DrbNode representing the requested URL resource.
        Raises:
            DrbFactoryException: if an error appear
        """

        # Full Windows path like c:/foo are not parsed correctly with urlparse,
        # so we make it into an uri that can be parsed
        if (sys.platform == "win32"
                and re.match(r"^[a-zA-Z]:", url)):
            url = pathlib.Path(url).as_uri().replace('%20', ' ')
        pp = urlparse(url)

        if curl is None and path is None:
            try:
                return self.create(UrlNode(url))
            except (DrbFactoryException, DrbException,
                    IndexError, KeyError, TypeError):
                pass

            if _is_remote_url(pp):
                curl = f'{pp.scheme}://{pp.netloc}'

            # Uri of Windows path parsed with urlparse returns a path like
            # /c:/foo/bar which is incorrect, so we take out the first '/'
            if (sys.platform == "win32"
                    and re.match(r"^/[a-zA-Z]:", pp.path)):
                path = list(pathlib.Path(pp.path[1:]).parts)
            else:
                path = list(pathlib.Path(pp.path).parts)
            if curl is None:
                seg = path.pop(0)
                curl = seg if os.path.isabs(pp.path) else f'{os.sep}{seg}'

        # try to create node from curl
        try:
            node = self.create(UrlNode(curl))
            for child in path:
                if child != '':
                    node = node[child]
            return node
        except (DrbFactoryException, DrbException,
                IndexError, KeyError, TypeError):
            if curl == url or len(path) == 0:
                raise DrbFactoryException(f'Cannot resolve URL: {url}')
            if _is_remote_url(pp):
                seg = path.pop(0)
                # skip empty string (e.g. /path/to//data)
                if seg == '':
                    seg = path.pop(0)
                curl += f'/{seg}'
            else:
                curl = os.path.join(curl, path.pop(0))
            return self.__create_from_url(url, curl, path)

    def _resolve_overridden(self, source: DrbNode) -> \
            Optional[Tuple[DrbTopic, Optional[DrbNode]]]:
        for ic in ManagerDao().get_overridden_drb_topics():
            source = forced_factory(ic, source)
            if ic.matches(source):
                return self.__finest_drb_topic(source, ic)
        return None

    def _basic_resolve(self, source: DrbNode) -> \
            Tuple[DrbTopic, Optional[DrbNode]]:
        if isinstance(source, str):
            node = UrlNode(source)
        else:
            node = source
        protocol = None
        if node.parent is None:

            protocol = self.__retrieve_protocol(node)
            if protocol is None:
                raise DrbFactoryException(f'Cannot resolve: {source}')
            node = FactoryLoader().get_factory(
                protocol.factory).create(node)

        container, node = self.__retrieve_container(node)
        if container is not None and container.factory is not None:
            node = FactoryLoader().get_factory(
                container.factory).create(node)

        formatting = self.__retrieve_formatting(node)
        if formatting is not None:
            if formatting.factory is not None:
                node = FactoryLoader().get_factory(formatting.factory).create(
                    node)
            t, n = self.__finest_drb_topic(node, formatting)
        elif container is not None:
            t, n = container, node
        elif protocol is not None:
            t, n = protocol, node
        else:
            raise DrbFactoryException(f'Cannot resolve: {source}')

        addons = filter(lambda x: x.can_apply(t),
                        AddonManager().get_all_addons())
        for addon in addons:
            node.add_impl(addon.return_type(), addon.apply, addon.identifier())
        return t, n

    def resolve(self, source: Union[str, DrbNode]) \
            -> Tuple[DrbTopic, Optional[DrbNode]]:
        """
        Retrieves the topic related to the given source.

        Parameters:
            source: source to be resolved
        Returns:
            tuple: A tuple containing a DrbTopic corresponding to the given
                   source and the last DrbNode allowing to resolve the given
                   source (maybe to ``None``)
        Raises:
            DrbFactoryException: if the given source cannot be resolved.
        """
        if isinstance(source, str):
            node = UrlNode(source)
        else:
            node = source

        result = self._resolve_overridden(node)
        if result is not None:
            topic, node = result
            if topic.factory is not None:
                node = FactoryLoader().get_factory(topic.factory).create(node)
            return topic, node
        return self._basic_resolve(node)

    def create(self, source: Union[DrbNode, str]) -> DrbNode:
        if isinstance(source, str):
            return self.__create_from_url(source)
        if isinstance(source, DrbNode):
            return self._basic_resolve(source)[1]
        raise DrbFactoryException(f'Invalid source type: {type(source)}')


class DrbNodeList(list):
    def __init__(self, children: List[DrbNode]):
        super(DrbNodeList, self).__init__()
        self._list: List[DrbNode] = children

    @staticmethod
    def __resolve_node(node: DrbNode):
        try:
            return create(node)
        except DrbFactoryException:
            return node

    def __getitem__(self, item):
        result = self._list[item]
        if isinstance(result, DrbNode):
            return self.__resolve_node(result)
        else:
            return [self.__resolve_node(node) for node in result]

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return DrbNodeListIterator(self._list.__iter__())

    def append(self, obj) -> None:
        raise DrbFactoryException

    def clear(self) -> None:
        raise DrbFactoryException

    def copy(self) -> List:
        raise DrbFactoryException

    def count(self, value) -> int:
        raise DrbFactoryException

    def insert(self, index: int, obj) -> None:
        raise DrbFactoryException

    def extend(self, iterable) -> None:
        raise DrbFactoryException

    def index(self, value, start: int = ..., __stop: int = ...) -> int:
        raise DrbFactoryException

    def pop(self, index: int = ...):
        raise DrbFactoryException

    def remove(self, value) -> None:
        raise DrbFactoryException

    def reverse(self) -> None:
        raise DrbFactoryException

    def sort(self, *, key: None = ..., reverse: bool = ...) -> None:
        raise DrbFactoryException

    def __eq__(self, other):
        raise DrbFactoryException

    def __ne__(self, other):
        raise DrbFactoryException

    def __add__(self, other):
        raise DrbFactoryException

    def __iadd__(self, other):
        raise DrbFactoryException

    def __radd__(self, other):
        raise DrbFactoryException

    def __setitem__(self, key, value):
        raise DrbFactoryException


class DrbNodeListIterator:
    def __init__(self, iterator):
        self.base_itr = iterator

    def __iter__(self):
        return self

    def __next__(self):
        node = next(self.base_itr)
        try:
            return create(node)
        except DrbFactoryException:
            return node


def resolve_children(func):
    def inner(ref):
        if isinstance(ref, DrbNode) and func.__name__ == 'children':
            return DrbNodeList(func(ref))
        raise TypeError('@resolve_children decorator must be only apply on '
                        'children methods of a DrbNode')
    return inner


def resolve(source: Union[str, DrbNode]) -> Tuple[DrbTopic, DrbNode]:
    return _DrbFactoryResolver().resolve(source)


def create(source: Union[str, DrbNode]) -> DrbNode:
    return _DrbFactoryResolver().create(source)
