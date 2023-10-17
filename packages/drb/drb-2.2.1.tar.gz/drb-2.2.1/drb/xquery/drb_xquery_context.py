from .execptions import ErrorXQUERY, DynamicException, StaticException
from drb.core.node import DrbNode
from enum import Enum
from typing import Optional, Any


class NavigationStep(Enum):
    CHILD = 1
    DESCENDANT_OR_SELF = 2
    DESCENDANT = 3


class AxeNode:
    def __init__(self, navigation_step=NavigationStep.CHILD):
        self.namespace = None
        self.name = None
        self.is_attribute = False
        self.is_node = True
        self.is_wildcard = False
        self.is_parent = False
        self.navigation_step = navigation_step
        self.namespace_resolved = False

    def set_namespace_full(self, namespace_full, prefix_ns):
        if len(namespace_full) > 0:
            self.namespace = namespace_full
            self.namespace_resolved = True
        else:
            self.namespace = prefix_ns
            self.namespace_resolved = False


class NamespaceMap:

    predefined_namespace = {
        'xmlns': "http://www.w3.org/2000/xmlns/",
        'xml': "http://www.w3.org/XML/1998/namespace",
        'fn': "http://www.w3.org/2005/xpath-functions",
        'xs': "http://www.w3.org/2001/XMLSchema",
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xdt': "http://www.w3.org/2003/11/xpath-datatypes",
        'local': "http://www.w3.org/2005/xquery-local-functions",
        'drb': "http://www.gael.fr/drb",
        'math': "http://exslt.org/math"
    }

    def __init__(self):
        self.namespace_map = {}
        self.namespace_prefix_map = {}

    @staticmethod
    def check_is_predefined_namespace(prefix: str, namespace_full: str):
        if prefix in NamespaceMap.predefined_namespace.keys():
            raise StaticException(
                ErrorXQUERY.XQST0070, "Prefix namespace "
                                      + prefix + " is predefined and cant be "
                                                 "re declared.")
        if namespace_full in NamespaceMap.predefined_namespace.values():
            raise StaticException(
                ErrorXQUERY.XQST0070, "Namespace "
                                      + namespace_full +
                                      " is predefined and cant be "
                                      "re declared.")

        return False

    def check_duplicate_namespace(self, prefix: str, namespace_full: str):
        if prefix in self.namespace_map.keys():
            raise StaticException(
                ErrorXQUERY.XQST0033, "Prefix namespace "
                                      + prefix + " already declared.")

        return False

    def add_namespace(self, prefix: str, namespace_full: str):
        self.check_duplicate_namespace(prefix, namespace_full)
        self.namespace_map[prefix] = namespace_full
        self.namespace_prefix_map[namespace_full] = prefix

    def get_namespace_full_name(self, prefix: str):
        if prefix in NamespaceMap.predefined_namespace.keys():
            return NamespaceMap.predefined_namespace[prefix]
        if prefix in self.namespace_map.keys():
            return self.namespace_map[prefix]
        return ''

    def get_namespace_prefix_name(self, fullname: str):
        if fullname in NamespaceMap.predefined_namespace.values():
            # TODO Optimise
            for key, full_key in NamespaceMap.predefined_namespace.items():
                if full_key == fullname:
                    return key

        if fullname in self.namespace_prefix_map.keys():
            return self.namespace_prefix_map[fullname]
        return ''

    def clone(self, other):
        self.namespace_map = other.namespace_map.copy()
        self.namespace_prefix_map = other.namespace_prefix_map.copy()


class StaticContext:
    def __init__(self):
        self.list_func = {}
        self.in_scope_variables = {}
        self.namespace_map = {}
        self.namespace_prefix_map = {}
        self.namespace_func = {}
        self.namespace_default_func = ''
        self.namespace_default_elt = ''

        self.name_space_map = NamespaceMap()

        self.namespace_builtin_func = {}

        self.imported_module = {}
        self.is_in_predicate = False
        self.list_children_open = []

    def clone(self, other):
        if isinstance(other, StaticContext):
            self.namespace_map = other.namespace_map.copy()
            self.namespace_prefix_map = other.namespace_prefix_map.copy()
            self.namespace_func = other.namespace_func.copy()
            self.namespace_builtin_func = other.namespace_func.copy()

            self.name_space_map.clone(other.name_space_map)
            self.imported_module = other.imported_module.copy()

    def get_key_var(self, key):
        from drb.xquery.drb_xquery_utils import DrbQueryFuncUtil
        namespace_prefix, name_var = DrbQueryFuncUtil.split_namespace_name(key)
        namespace_full = None
        if namespace_prefix is not None:
            namespace_full = self.get_namespace_full_name(namespace_prefix)

        if namespace_full is not None and len(namespace_full) > 0:
            return namespace_full, name_var

        else:
            return None, name_var

    def add_var(self, key: str, var):
        key = self.get_key_var(key)

        self.in_scope_variables[key] = var

    def get_var(self, key: str):
        key_tuple = self.get_key_var(key)

        if key_tuple not in self.in_scope_variables.keys():
            raise DynamicException(ErrorXQUERY.XPST0008, "Variable : " +
                                   str(key) + " unknown.")
        return self.in_scope_variables[key_tuple]

    def add_namespace(self, prefix: str, namespace_full: str):
        NamespaceMap.check_is_predefined_namespace(prefix, namespace_full)
        return self.name_space_map.add_namespace(prefix, namespace_full)

    def get_namespace_full_name(self, prefix: str):
        return self.name_space_map.get_namespace_full_name(prefix)

    def get_namespace_prefix_name(self, fullname: str):
        return self.name_space_map.get_namespace_prefix_name(fullname)

    def set_func_list_namespace(self, prefix: str, func_list: dict):
        self.namespace_func[prefix] = func_list

    def get_func_list_namespace(self, prefix: str):
        if prefix in self.namespace_func.keys():
            return self.namespace_func[prefix]
        return None

    def get_func_namespace(self, prefix: str, func_name: str):
        if prefix in self.namespace_func.keys():
            if func_name in self.namespace_func[prefix].keys():
                return self.namespace_func[prefix][func_name]
        return None

    # def add_func_namespace(self, prefix: str, func_name: str, func):
    #     if prefix in self.namespace_func.keys():
    #         self.namespace_func[prefix][func_name] = func
    #     else:
    #         self.namespace_func[prefix] = {}
    #         self.namespace_func[prefix][func_name] = func

    def add_func_build_in(self, func_name: str, func_exp,
                          specific_context=None):
        ns, func_name = self.get_key_var(func_name)
        from drb.xquery.drb_xquery_variable import XqueryBuildIn
        self.namespace_builtin_func[ns, func_name] = XqueryBuildIn(
            func_name,
            func_exp,
            namespace=ns,
            specific_context=specific_context
        )

    def get_func_build_in(self, func_name: str):
        ns, func_name = self.get_key_var(func_name)
        if (ns, func_name) in self.namespace_builtin_func.keys():
            return self.namespace_builtin_func[ns, func_name]
        return None


class DynamicContext:

    def __init__(self, node, position=0, value=None, parent=None,
                 attribute=False,
                 size_context=1,
                 namespace=None,
                 dynamic_context_prev=None):
        self.node = node
        self._value = value
        self._name = None

        if not isinstance(self.node, DrbNode) and value is None:
            self._value = self.node
        self._namespace = namespace
        self._parent = parent
        self.position = position
        self.size_context = size_context
        self.attribute = attribute
        self.name_space_map = NamespaceMap()

        if dynamic_context_prev is None:
            self.namespace_default_elt = ''
        else:
            self.namespace_default_elt = \
                dynamic_context_prev.namespace_default_elt
            self.name_space_map.clone(dynamic_context_prev.name_space_map)

    @property
    def name(self) -> str:
        if self._name is None:
            if isinstance(self.node, DrbNode):
                self._name = self.node.name
            elif isinstance(self.node, tuple):
                if len(self.node) == 2:
                    self._name, self._namespace = self.node
            else:
                self._name = self.node
        return self._name

    @property
    def value(self) -> Optional[Any]:
        if isinstance(self.node, DrbNode):
            return self.node.value
        return self._value

    @property
    def namespace_uri(self) -> Optional[str]:
        if isinstance(self.node, DrbNode):
            self._namespace = self.node.namespace_uri
        elif self._namespace is None and self._name is None:
            if isinstance(self.node, tuple):
                if len(self.node) == 2:
                    self._name, self._namespace = self.node
        return self._namespace

    def is_node(self):
        return isinstance(self.node, DrbNode)

    def is_attribute(self):
        return self.attribute

    @property
    def parent(self) -> Optional[DrbNode]:
        if isinstance(self.node, DrbNode):
            return self.node.parent
        return self._parent

    def add_namespace(self, static_context: StaticContext,
                      prefix: str, namespace_full: str):
        if prefix == 'xml' and \
                NamespaceMap.predefined_namespace[prefix] == namespace_full:
            return
        NamespaceMap.check_is_predefined_namespace(prefix, namespace_full)

        static_context.name_space_map.check_duplicate_namespace(prefix,
                                                                namespace_full)
        return self.name_space_map.add_namespace(prefix, namespace_full)

    def get_namespace_full_name(self, prefix: str):
        return self.name_space_map.get_namespace_full_name(prefix)

    def get_namespace_prefix_name(self, fullname: str):
        return self.name_space_map.get_namespace_prefix_name(fullname)

    def __eq__(self, other):
        if self.is_node():
            return self.node == other.node

        return self.name == other.value and self.value == other.value
