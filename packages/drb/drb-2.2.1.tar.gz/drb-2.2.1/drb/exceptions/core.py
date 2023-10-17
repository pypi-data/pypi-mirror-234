class DrbException(Exception):
    pass


class DrbFactoryException(DrbException):
    pass


class DrbNotImplementationException(DrbException):
    pass


class DrbPathException(DrbException):
    pass


class DrbSignatureNotFound(DrbException):
    pass


class DaoException(DrbException):
    pass
