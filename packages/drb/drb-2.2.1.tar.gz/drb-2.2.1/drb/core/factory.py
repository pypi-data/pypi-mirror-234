from __future__ import annotations

import importlib
import inspect
import logging
import drb.utils.plugins
from abc import ABC, abstractmethod
from typing import Optional, Union

from .node import DrbNode
from drb.exceptions.core import DrbException
from drb.nodes.url_node import UrlNode


class DrbFactory(ABC):
    """
    The Factory class defines the abstract class to be implemented in order to
    build drb nodes according to their physical form.
    The factory shall be aware of the implementations available to build nodes
    and build a relation between the physical data and its virtual node
    representation.
    """

    @abstractmethod
    def _create(self, node: DrbNode) -> DrbNode:
        """
        Build a DrbNode thanks to this factory implementation.

        Parameters:
            The DrbNode of the physical data.
        Return:
            a drb node representing the passed node
        Raises:
            DrbFactoryException: if the factory cannot build the node
        """
        raise NotImplementedError("Call impl method")

    def create(self, source: Union[DrbNode, str]) -> DrbNode:
        """
        Build a DrbNode thanks to this factory implementation.

        Parameters:
            source, the URI or the DrbNode of the physical data.
        Return:
            a drb node representing the passed source
        Raises:
            DrbFactoryException: if the given source is not valid
        """
        if isinstance(source, DrbNode):
            return self._create(source)
        else:
            return self._create(UrlNode(source))


class FactoryLoader:
    """
    Manages loading and retrieving of factories defined in the Python context.
    """
    __instance = None
    __factories = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(FactoryLoader, cls).__new__(cls)
            cls.__factories = cls.__load_factories()
        return cls.__instance

    @classmethod
    def __is_class(cls, class_name: str):
        return lambda obj: inspect.isclass(obj) and class_name == obj.__name__

    @classmethod
    def __load_factories(cls) -> dict:
        entry_point_group = 'drb.driver'
        factories = {}
        for ep in drb.utils.plugins.get_entry_points(entry_point_group):
            factory_name = ep.name

            if factory_name in factories:
                continue

            # m -> factory module, c -> factory class
            m, c = ep.value.split(':')
            try:
                m = importlib.import_module(m)
                for _, obj in inspect.getmembers(m, cls.__is_class(c)):
                    if obj != DrbFactory and issubclass(obj, DrbFactory):
                        factories[ep.name] = obj()
                    else:
                        logging.getLogger().warning(
                            f'Failed to load factory "{ep.name}":'
                            f'Invalid factory: {ep.value}'
                        )
            except ModuleNotFoundError:
                logging.getLogger().warning(
                    f'Failed to load factory "{ep.name}": Module {m} not found'
                )
        return factories

    def get_factories(self) -> dict:
        return self.__factories.copy()

    def get_factory(self, name: str) -> Optional[DrbFactory]:
        """
        Retrieves a factory by its name identifier.
        Parameters:
            name: factory name identifier
        Returns:
             DrbFactory - the requested factory, otherwise ``None``
        """
        return self.__factories.get(name, None)

    def check_factories(self) -> None:
        for name, factory in self.__factories.items():
            if factory is None:
                raise DrbException(f'factory {name} defined but not found')
