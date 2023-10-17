from drb.exceptions.core import DrbSignatureNotFound
from .node import DrbNode
from typing import Callable, List
import abc
import importlib
import inspect
import logging
import drb.utils.plugins


_entry_point_name = 'drb.signature'
_signatures = None


class Signature(abc.ABC):
    """
    A signature describes a recognition mechanism for a specific type of DRB
    Item (ItemClass). This recognition mechanism is applied on a DRB Node.
    """

    @abc.abstractmethod
    def matches(self, node: DrbNode) -> bool:
        """
        Allowing to check if the given node match the signature.

        Parameters:
            node (DrbNode): item to check

        Returns:
            bool - ``True`` if the given node match, otherwise ``False``
        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError


class SignatureAggregator(Signature):
    """
    Allowing to check if a DRB Node match a signature set.
    Parameters:
        signatures List[Signature]: signature list to match
    """

    def __init__(self, signatures: List[Signature]):
        self._signatures = signatures

    def matches(self, node: DrbNode) -> bool:
        if len(self._signatures) == 0:
            return False
        for signature in self._signatures:
            if not signature.matches(node):
                return False
        return True

    def to_dict(self) -> dict:
        data = {}
        for signature in self._signatures:
            for k, v in signature.to_dict().items():
                data[k] = v
        return data


def _filter_signature_by_name(name: str):
    """
    Returns specific lambda checking if the given object is a class, and it
    names as the given name.
    """
    return lambda obj: inspect.isclass(obj) and obj.__name__ == name


def _load_signatures():
    """
    Loads signatures defined in the Python environment via the entry point
    mechanism.
    """
    for entry_point in drb.utils.plugins.get_entry_points(_entry_point_name):
        if entry_point.name in _signatures:
            logging.warning(
                f'Signature({entry_point.name},{entry_point.value}) skipped '
                f'caused by signature name ({entry_point.name}) already used')
            continue

        module_path, class_name = entry_point.value.split(':')
        try:
            module = importlib.import_module(module_path)

            members = inspect.getmembers(module,
                                         _filter_signature_by_name(class_name))
            if len(members) != 1:
                raise DrbSignatureNotFound(f'Signature not found at: '
                                           f'{entry_point.value}')

            _, obj = members[0]
            if not issubclass(obj, Signature):
                raise TypeError(f'{entry_point.value} is not a Signature')

            _signatures[entry_point.name] = obj
        except ModuleNotFoundError:
            logging.error(f'module {module_path} not found')
        except Exception as ex:
            logging.error(f'an error occurred during loading signature '
                          f'"{entry_point.name}": {ex}')


def get(name: str) -> Callable:
    if name in _signatures:
        return _signatures[name]
    raise KeyError(f'Signature not found: {name}')


def parse_signature(data: dict) -> Signature:
    signatures = []
    for key in data.keys():
        signature = get(key)(data[key])
        if signature is not None:
            signatures.append(signature)
    return SignatureAggregator(signatures)


if _signatures is None:
    _signatures = {}
    _load_signatures()
