from typing import Callable, Iterable, List, Optional, Tuple, Union


class ImplementationManager:
    def __init__(self):
        self.__impls = {}

    def add_impl(self, impl: type, identifier: Union[str, None],
                 function: Callable) -> None:
        """
        Adds or replaces support of a specific interface.
        Parameters:
            impl: interface implementation to add
            identifier: add-on identifier (default: ``None``)
            function: specific function allowing to generate the given
                      implementation
        """
        self.__impls[impl, identifier] = function

    def remove_impl(self, impl: type, identifier: str = None) -> None:
        """
        Remove a specific implementation.
        """
        if (impl, identifier) in self.__impls:
            del self.__impls[impl, identifier]

    def __find_impl(self, impl: type, identifier: Optional[str]) \
            -> List[Tuple[type, Optional[str]]]:
        if identifier is None:
            if (impl, None) in self.__impls.keys():
                return [(impl, None)]
            keys = set(self.__impls.keys())
        else:
            keys = set(
                filter(lambda x: x[1] == identifier, self.__impls.keys())
            )
        return list(filter(lambda x: issubclass(x[0], impl), keys))

    def has_impl(self, impl: type, identifier: str = None) -> bool:
        """
        Checks if a specific interface can be provided.

        Parameters:
            impl (type): the implementation type expected
            identifier (str): add-on interface identifier (default: ``None``)
        Returns:
            bool: True if an implementation of the interface can be provided
        and False otherwise.
        """
        return len(self.__find_impl(impl, identifier)) > 0

    def get_impl(self, impl: type, identifier: str = None) -> Callable:
        """
        This operation returns a reference to an object implementing a
        specific interface. The provided object is
        independent of this node and shall be released/closed by the caller
        when interface requires such finally operations.

        Parameters:
            impl (type): implementation type expected.
            identifier (str): implementation interface identifier, allows to
                              specify from which add-on retrieve the
                              implementation (default: ``None``)
        Return:
            Callable: the expected implementation.
        Raises:
            KeyError: if the given interface is not found
        """
        keys = self.__find_impl(impl, identifier)
        if len(keys) == 1:
            return self.__impls[keys[0]]
        raise KeyError

    def get_capabilities(self) -> List[Tuple[type, str]]:
        """
        Returns all possible interfaces the node can provide.

        Returns:
            Iterable[Tuple[type, str]]: A list of all possible interfaces
        """
        return list(self.__impls.keys())
