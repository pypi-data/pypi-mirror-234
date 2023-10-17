from deprecated import deprecated

from drb.core.path import ParsedPath
from drb.core.node import DrbNode
from drb.core.factory import DrbFactory
from drb.nodes.abstract_node import AbstractNode
from drb.exceptions.core import DrbNotImplementationException
from drb.exceptions.file import DrbFileNodeFactoryException
from urllib.parse import urlparse
from typing import Any, List

import io
import os
import platform
import pathlib
import re
import stat
import drb.topics.resolver as resolver


def is_hidden(path: str) -> bool:
    """
    Check if the associated file of the given path is hidden.
    :param path: file path to check
    :return: True if the file of the corresponding path is hidden
    :rtype: bool
    """
    # os_type = 'Linux' | 'Windows' | 'Java'
    os_type = platform.uname()[0]
    if os_type == 'Windows':
        return bool(os.stat(path).st_file_attributes &
                    stat.FILE_ATTRIBUTE_HIDDEN)
    return os.path.basename(path).startswith('.')


def _retrieve_file_mode(st_mode) -> str:
    if stat.S_ISREG(st_mode):
        return 'REGULAR'
    if stat.S_ISDIR(st_mode):
        return 'DIRECTORY'
    if stat.S_ISLNK(st_mode):
        return 'LINK'
    if stat.S_ISSOCK(st_mode):
        return 'SOCKET'
    if stat.S_ISFIFO(st_mode):
        return 'FIFO'
    if stat.S_ISBLK(st_mode):
        return 'BLOCK'
    if stat.S_ISCHR(st_mode):
        return 'CHAR'
    return 'UNKNOWN'


class DrbFileNode(AbstractNode):
    """
    Parameters:
        path (Union[str, ParsedPath]): The path of the file
                                       to read with this node.
        parent (DrbNode): The parent of this node (default: None)
    """

    def __init__(self, path, parent: DrbNode = None):
        super().__init__()
        if isinstance(path, ParsedPath):
            self._path = path
        else:
            if platform.uname()[0] == 'Windows':
                path = pathlib.Path(path).as_posix()
            self._path = ParsedPath(os.path.abspath(path))
        self.parent: DrbNode = parent
        self.__init_attr()
        self.add_impl(io.FileIO, self.__impl_stream)
        self.add_impl(io.BufferedReader, self.__impl_buffered_stream)
        self.name = self._path.filename
        self._children: List[DrbNode] = None

    @property
    def path(self) -> ParsedPath:
        return self._path

    def __init_attr(self):
        file_stat = os.stat(self.path.path)
        self.__imatmul__(('size', file_stat.st_size))
        self.__imatmul__(('mode', _retrieve_file_mode(file_stat.st_mode)))
        self.__imatmul__(('creation_time', file_stat.st_ctime))
        self.__imatmul__(('last_modification_time', file_stat.st_mtime))
        self.__imatmul__(('last_access_time', file_stat.st_atime))
        self.__imatmul__(('owner', file_stat.st_uid))
        self.__imatmul__(('group', file_stat.st_gid))
        self.__imatmul__(('link_number', file_stat.st_nlink))
        self.__imatmul__(('inode', file_stat.st_ino))
        self.__imatmul__(('hidden', is_hidden(self.path.path)))

    @property
    @resolver.resolve_children
    @deprecated(version='2.1.0', reason='Only bracket browse should be use')
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = []
            if os.path.isdir(self.path.path):
                sorted_child_names = sorted(os.listdir(self.path.path))
                for filename in sorted_child_names:
                    child = DrbFileNode(self.path / filename, parent=self)
                    self._children.append(child)
        return self._children

    def close(self) -> None:
        """
        Not use in this implementation.

        Returns:
            None
        """
        pass

    @classmethod
    def __impl_stream(cls, node: DrbNode) -> io.FileIO:
        return io.FileIO(node.path.path, 'r')

    @classmethod
    def __impl_buffered_stream(cls, node: DrbNode) -> io.BufferedReader:
        return io.BufferedReader(cls.__impl_stream(node))


class DrbFileFactory(DrbFactory):

    @staticmethod
    def _create_from_uri_of_node(node: DrbNode):
        uri = node.path.name
        parsed_uri = urlparse(uri)
        if (platform.uname()[0] == "Windows"):

            # not sure this code is executed
            # on windows plateform the urlparse split the drive letter
            # into parsed_uri.scheme.
            # parsed_uri has no drive letter
            if re.match(r"^/[a-zA-Z]:", parsed_uri.path):
                path = parsed_uri.path[:1].replace('%20', ' ')

            # PYDRB 547
            # test if it is a local file by testing if
            # its existence. This is the only way found to check whether
            # the uri is a local path or an url
            # if it is a loal path, simply keep the full uri
            if pathlib.Path(uri).exists():
                path = uri
            else:
                path = parsed_uri.path

        else:
            path = parsed_uri.path
        if os.path.exists(path):
            return DrbFileNode(path, node)
        raise DrbFileNodeFactoryException(f'File not found: {path}')

    def _create(self, node: DrbNode) -> DrbNode:
        return self._create_from_uri_of_node(node)
