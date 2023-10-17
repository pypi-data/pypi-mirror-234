import unittest
from drb.core import DrbNode
from drb.core.factory import DrbFactory, FactoryLoader
from tests.utils import DrbTestNode


class DefaultFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        return DrbTestNode(f"DefaultNode_{node.name}")


class TestDrbFactory(unittest.TestCase):
    def test_drb_factory_check_uri(self):
        uris = [
            ("file://my/path/to/my_file/", "DefaultNode_"),
            ("/my/path/to/my_file/", "DefaultNode_"),
            ("file://my/path/to/my_file", "DefaultNode_my_file"),
            ("/my/path/to/my_file", "DefaultNode_my_file"),
            ("http://avp.wikia.com/wiki/ht_file", "DefaultNode_ht_file"),
            ("AAA", "DefaultNode_AAA"),
            ("ftp://ftp.fe.fr/ms/fp.cs.org/7.2.15/ft_file",
             "DefaultNode_ft_file")]

        factory = DefaultFactory()
        for uri, expected_name in uris:
            self.assertEqual(factory.create(uri).name, expected_name,
                             f'Uri not supported: {uri}')


class TestFactoryLoader(unittest.TestCase):
    def test_get_factories(self):
        loader = FactoryLoader()
        expected_factories = [
            'file',
            'xml',
            'foobar',
            'data',
            'resource',
            'url',
            'mem',
            'safe',
            's1l0rf',
            'txt',
            'zip',
        ]
        factories = loader.get_factories()
        self.assertEqual(13, len(factories))
        expected = all(
            map(
                lambda x: isinstance(x, DrbFactory),
                map(lambda f: loader.get_factory(f), expected_factories)
            )
        )
        self.assertTrue(expected)

    def test_get_factory(self):
        loader = FactoryLoader()

        factory = loader.get_factory('xml')
        self.assertEqual("<class 'drb.drivers.xml.factory.XmlNodeFactory'>",
                         str(factory.__class__))

        factory = loader.get_factory('unknown')
        self.assertIsNone(factory)
