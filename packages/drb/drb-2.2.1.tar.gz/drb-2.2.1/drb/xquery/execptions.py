from enum import Enum

from drb.exceptions.core import DrbException


class ErrorXQUERY(Enum):
    XPDY0002 = "Dynamic context is absent"
    XPST0017 = "No matching function call"
    XPTY0004 = "Type error"
    XPTY0020 = "Context item is not a node"
    FOAP0001 = "Wrong number of arguments."
    FOAR0001 = "Division by zero."
    FOCH0004 = "Collation does not support collation units."
    FORG0006 = "Invalid argument type."
    XPST0008 = "Unreferenced element, variable, attribute name or namespace"
    FODC0002 = "Error retrieving resource."
    FODC0005 = "Invalid argument to fn:doc or fn:doc-available."
    FOTY0012 = "Argument to fn:data() contains a node that does not have" \
               " a typed value."
    FORG0001 = "Invalid value for cast / constructor."
    FORX0001 = "Invalid regular expression flags."
    FORX0002 = "Invalid regular expression."
    FORX0003 = "Regular expression matches zero - length string."
    FORX0004 = "Invalid replacement string."
    XPST0051 = "Undefined type"
    XQST0134 = "The namespace axis is not supported."
    XPST0003 = "Syntax error."
    XQST0033 = "Duplicated namespace declaration"
    XQST0070 = "Undeclarable namespace"


class DynamicException(DrbException):
    def __init__(self, error: ErrorXQUERY, message):
        super().__init__(repr(error) + message)


class StaticException(DrbException):
    def __init__(self, error: ErrorXQUERY, message):
        super().__init__(repr(error) + message)
