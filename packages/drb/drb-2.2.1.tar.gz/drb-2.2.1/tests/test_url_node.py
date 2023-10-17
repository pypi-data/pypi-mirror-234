import io
import string
import unittest
import tempfile
import random
import pathlib

from drb.core.path import ParsedPath
from drb.nodes.url_node import UrlNode
from drb.exceptions.core import DrbException
from tests.utils import DrbTestPredicate
from requests.auth import HTTPBasicAuth


class TestUrlNode(unittest.TestCase):
    data = None
    path = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = ''.join(
            random.choice(string.ascii_letters) for _ in range(100))
        fd, cls.path = tempfile.mkstemp()
        with open(cls.path, 'w') as file:
            file.write(cls.data)

    @classmethod
    def tearDownClass(cls) -> None:
        # os.remove(cls.path)
        if pathlib.Path(cls.path).is_dir():
            pathlib.Path(cls.path).rmdir()

    def test_namespace_uri(self):
        node = UrlNode(self.path)
        self.assertIsNone(node.namespace_uri)

    def test_name(self):
        node = UrlNode(f'file://{self.path}')
        self.assertEqual(pathlib.Path(self.path).stem, node.name)

    def test_value(self):
        node = UrlNode(self.path)
        self.assertIsNone(node.value)

    def test_path(self):
        # fix PYDRB 327 : for comparison purpose,
        # convert the path using pathlib so that the path separtors
        # (slashes) are correct for the current operating system
        # (i.e windows)
        converted_path = pathlib.Path(self.path).as_posix()

        node = UrlNode(self.path)
        self.assertEqual(converted_path, node.path.path)
        node = UrlNode(f'file://{self.path}')
        self.assertEqual(converted_path, node.path.path)

    def test_parent(self):
        node = UrlNode(self.path)
        self.assertIsNone(node.parent)

    def test_attributes(self):
        node = UrlNode(self.path)
        self.assertEqual({}, node.attributes)

    def test_get_attribute(self):
        node = UrlNode(self.path)
        with self.assertRaises(DrbException):
            node.get_attribute('test')

    def test_children(self):
        node = UrlNode(self.path)
        self.assertEqual([], node.children)

    def test_has_child(self):
        node = UrlNode(self.path)
        self.assertFalse(node.has_child())

    def test_has_impl(self):
        node = UrlNode(self.path)
        self.assertTrue(node.has_impl(io.BytesIO))
        self.assertFalse(node.has_impl(str))

    def test_has_impl_buffered(self):
        node = UrlNode(self.path)
        self.assertTrue(node.has_impl(io.BufferedIOBase))
        self.assertFalse(node.has_impl(str))

    def test_get_impl(self):
        node = UrlNode(self.path)
        with node.get_impl(io.BytesIO) as stream:
            self.assertEqual(self.data.encode(), stream.read())

        with self.assertRaises(DrbException):
            node.get_impl(str)

    def test_get_impl_credential(self):
        node = UrlNode(self.path, auth=HTTPBasicAuth("name", "pass"))
        with node.get_impl(io.BytesIO) as stream:
            self.assertEqual(self.data.encode(), stream.read())

        with self.assertRaises(DrbException):
            node.get_impl(str)

    def test_getitem(self):
        node = UrlNode(self.path)
        n = None
        with self.assertRaises(DrbException):
            n = node[0]
        with self.assertRaises(DrbException):
            n = node['foo']
        with self.assertRaises(DrbException):
            n = node['foo', 'bar']
        with self.assertRaises(DrbException):
            n = node['foo', 1]
        with self.assertRaises(DrbException):
            n = node['foo', 'bar', 1]
        with self.assertRaises(DrbException):
            n = node[DrbTestPredicate()]

    def test_len(self):
        node = UrlNode(self.path)
        self.assertEqual(0, len(node))

    def test_close(self):
        node = UrlNode(self.path)
        node.close()

    def test_hash(self):
        path = ParsedPath(self.path)
        node = UrlNode(path)
        self.assertEqual(hash(path.name), hash(node))
