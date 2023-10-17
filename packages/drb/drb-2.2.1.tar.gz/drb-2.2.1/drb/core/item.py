from __future__ import annotations

import abc
from typing import Any, Optional, Callable

from drb.core import EventManager


class DrbItem(abc.ABC):
    """
    Item interface. This interface represents common properties of structured
    data. Supported item kinds are nodes, attributes.

    The item content if a tuple of (name, value, namespace) information, where
    name is mandatory and value and namespace are optional. It might be
    extended by the sub implementations.
    """
    __event_type_item = {
        'name-changed',
        'namespace-changed',
        'value-changed',
    }

    def __init__(self):
        self.__events = EventManager()
        self.__name = None
        self.__namespace_uri = None
        self.__value = None
        for event_name in self.__event_type_item:
            self._event_manager.append_event_type(event_name)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        old = self.name
        if old != name:
            self.__name = name
            self._event_manager.notify('name-changed', self, old, name)

    @property
    def namespace_uri(self) -> Optional[str]:
        return self.__namespace_uri

    @namespace_uri.setter
    def namespace_uri(self, namespace_uri: str) -> None:
        old = self.namespace_uri
        if old != namespace_uri:
            self.__namespace_uri = namespace_uri
            self._event_manager.notify('namespace-changed', self, old,
                                       namespace_uri)

    @property
    def value(self) -> Optional[Any]:
        return self.__value

    @value.setter
    def value(self, value: Any) -> None:
        old = self.value
        if old != value:
            self.__value = value
            self._event_manager.notify('value-changed', self, old, value)

    @property
    def _event_manager(self) -> EventManager:
        """
        Retrieves the EventManager associated to this node.

        Returns:
             EventManager: the event manager attached to this node

        """
        return self.__events

    def register(self, event_type: str, callback: Callable):
        """
        Registers a new callback on a specific event type.

        Parameters:
            event_type (str): target event type
            callback (Callable): the callback to register
        """
        self.__events.register(event_type, callback)

    def unregister(self, event_type: str, callback: Callable):
        """
        Unregisters a new callback on a specific event type.

        Parameters:
            event_type (str): target event type
            callback (Callable): the callback to unregister
        """
        self.__events.unregister(event_type, callback)
