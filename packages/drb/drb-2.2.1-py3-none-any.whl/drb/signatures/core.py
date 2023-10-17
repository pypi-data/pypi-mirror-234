from drb.core import DrbNode
from drb.core.predicate import Predicate
from drb.utils.drb_python_script import exec_with_return
from drb.exceptions.core import DrbException
from drb.core.signature import Signature, SignatureAggregator
import re
import logging


class NameSignature(Signature):
    """
    Allowing to check if a DRB Node name match a specific regex.
    Parameters:
        regex (str): regex pattern to match
    """

    def __init__(self, regex: str):
        self.__regex = regex

    def matches(self, node: DrbNode) -> bool:
        return re.match(self.__regex, node.name) is not None

    def to_dict(self) -> dict:
        return {self.get_name(): self.__regex}

    @staticmethod
    def get_name():
        return 'name'


class NamespaceSignature(Signature):
    """
    Allowing to check if a DRB Node namespace_uri match a specific regex.
    Parameters:
        regex (str): regex pattern to match
    """

    def __init__(self, regex: str):
        self.__regex = regex

    def matches(self, node: DrbNode) -> bool:
        return re.match(self.__regex, node.namespace_uri) is not None

    def to_dict(self) -> dict:
        return {self.get_name(): self.__regex}

    @staticmethod
    def get_name():
        return 'namespace'


class PathSignature(Signature):
    """
    Allowing to check if a DRB Node path match a specific regex.
    Parameters:
        regex (str): regex pattern to match
    """

    def __init__(self, regex: str):
        self.__regex = regex

    def matches(self, node: DrbNode) -> bool:
        return re.match(self.__regex, node.path.name) is not None

    def to_dict(self) -> dict:
        return {self.get_name(): self.__regex}

    @staticmethod
    def get_name():
        return 'path'


class _AttributeSignature(Signature):
    """
    Allowing to check if a DRB Node having a specific attribute and also to
    check its value.
    Parameters:
        name (str): attribute name
    Keyword Arguments:
        namespace (str): attribute namespace
        value (Any): attribute value
    """

    def __init__(self, name: str, **kwargs):
        self.__name = name
        self.__namespace = kwargs.get('namespace', None)
        self.__check_value = 'value' in kwargs.keys()
        self.__value = kwargs.get('value', None)

    def matches(self, node: DrbNode) -> bool:
        try:
            value = node.get_attribute(self.__name, self.__namespace)
            if self.__check_value:
                return self.__value == value
            return True
        except DrbException:
            return False

    def to_dict(self) -> dict:
        data = {'name': self.__name}
        if self.__namespace is not None:
            data['namespace'] = self.__namespace
        if self.__value is not None:
            data['value'] = self.__value
        return data

    @staticmethod
    def get_name():
        return 'attribute'


class AttributesSignature(SignatureAggregator):
    """
    Allowing to check one or several attribute of a node.
    """

    def __init__(self, attributes: list):
        signatures = []
        for data in attributes:
            signatures.append(_AttributeSignature(**data))
        super().__init__(signatures)

    def to_dict(self) -> dict:
        return {self.get_name(): [sig.to_dict() for sig in self._signatures]}

    @staticmethod
    def get_name():
        return 'attributes'


class _ChildSignature(Signature):
    """
    Allowing to check if a DRB Node having a child matching specific criteria.

    Parameters:
        name (str): child name pattern

    Keyword Arguments:
        namespace (str): child node namespace (default: None)
        namespaceAware (bool): namespace_aware node flag (default: ``False``)
    """

    class _ChildPredicate(Predicate):
        def __init__(self, name: str, ns: str = None, aware: bool = False):
            self.__name = name
            self.__ns = ns
            self.__ns_aware = aware

        def matches(self, node) -> bool:
            match = re.match(self.__name, node.name)
            if match is None:
                return False
            if self.__ns is not None:
                return True if node.namespace_uri == self.__ns else False
            if self.__ns_aware:
                return self.__ns == node.namespace_uri
            return True

    def __init__(self, name: str, **kwargs):
        self.__name = name
        self.__ns = kwargs.get('namespace', None)
        self.__aware = kwargs.get('namespaceAware', False)
        self.__predicate = _ChildSignature._ChildPredicate(
            self.__name, self.__ns, self.__aware)

    def matches(self, node: DrbNode) -> bool:
        try:
            n = node[self.__predicate]
            return len(n) > 0
        except DrbException:
            return False

    def to_dict(self) -> dict:
        data = {'name': self.__name}
        if self.__ns is not None:
            data['namespace'] = self.__ns
        if self.__aware:
            data['namespaceAware'] = self.__aware
        return data

    @staticmethod
    def get_name():
        return 'child'


class ChildrenSignature(SignatureAggregator):
    """
    Allowing to check if specific children of a DRB Node match their associated
    criteria.

    Parameters:
        children (list): data list, each data must allow generation of a
                         ChildSignature
    """

    def __init__(self, children: list):
        signatures = []
        for data in children:
            signatures.append(_ChildSignature(**data))
        super().__init__(signatures)

    def to_dict(self) -> dict:
        return {self.get_name(): [sig.to_dict() for sig in self._signatures]}

    @staticmethod
    def get_name():
        return 'children'


class PythonSignature(Signature):
    """
    Allowing to check if a DRB Node match a custom signature.

    Parameters:
        script (str): custom Python (3.8+) script signature, this script must
                    return a boolean, otherwise ``False`` will be always
                    returned
    """

    _logger = logging.getLogger('PythonSignature')
    _ident = '  '

    def __init__(self, script: str):
        self.__code = self._ident + script.replace('\n', f'\n{self._ident}')
        self._script = f'def match():\n{self.__code}\nmatch()'

    def matches(self, node: DrbNode) -> bool:
        try:
            result = exec_with_return(self._script, node)
            if isinstance(result, bool):
                return result
            return False
        except Exception as ex:
            self._logger.debug('An error occurred during a Python signature'
                               f' check: {ex}')
            return False

    def to_dict(self) -> dict:
        return {self.get_name(): self.__code}

    @staticmethod
    def get_name():
        return 'python'
