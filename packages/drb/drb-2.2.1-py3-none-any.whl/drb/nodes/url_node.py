from __future__ import annotations
import io
import keyring
import requests
from requests.auth import AuthBase, HTTPBasicAuth
from typing import Any, Optional, List, Dict, Tuple, Union

from drb.core.node import DrbNode
from drb.core.path import ParsedPath, Path, parse_path
from drb.exceptions.core import DrbException


class UrlNode(DrbNode):
    """
    URL node is a simple implementation of DrbNode base on a given URL without
    any attribute or child. This node must be use only in this core library
    (drb) and not in any implementation. It's mainly uses to generate the root
    node generated from an URI.
    """
    def __init__(self, source: Union[str, Path, ParsedPath],
                 auth: AuthBase = None):
        """
        The construction of an UrlNode.

        Parameters:
            source (str, Path, ParsedPAth): the url to the service
            auth (AuthBase): the authentication(Optional)

        """
        super().__init__()
        self._path = parse_path(source)
        self._auth = auth
        self.add_impl(io.BytesIO, self._to_buffered_bytes, None)

    @property
    def name(self) -> str:
        return self._path.filename

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        raise DrbException('UrlNode has no attribute')

    @property
    def parent(self) -> Optional[DrbNode]:
        return None

    @property
    def path(self) -> ParsedPath:
        return self._path

    @property
    def children(self) -> List[DrbNode]:
        return []

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        return False

    def close(self) -> None:
        pass

    @classmethod
    def _to_buffered_bytes(cls, node: UrlNode):
        try:
            original_path = node.path.original_path
            if 'file' == node.path.scheme:
                path = original_path[7:]
                return open(path, 'rb')
            if '' == node.path.scheme:
                return open(original_path, 'rb')
            return requests.get(original_path,
                                auth=node._find_credential(original_path))
        except Exception as ex:
            raise DrbException(f'Unsupported URL') from ex

    def __len__(self):
        return 0

    def __getitem__(self, item):
        raise DrbException('UrlNode has no child')

    def __delitem__(self, key):
        raise DrbException('UrlNode has no child')

    def __setitem__(self, key, value):
        raise DrbException('UrlNode has no child')

    def __truediv__(self, child):
        raise DrbException('UrlNode has no child')

    def _find_credential(self, url: str):
        if self._auth is not None:
            return self._auth

        credential = keyring.get_credential(url, None)
        if credential is not None:
            return HTTPBasicAuth(credential.username, credential.password)

        return None
