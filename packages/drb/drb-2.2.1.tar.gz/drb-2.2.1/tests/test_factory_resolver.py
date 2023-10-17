import io
import os
import unittest
from uuid import UUID

import drb.topics.resolver as resolver
from drb.nodes.logical_node import DrbLogicalNode
from drb.nodes.url_node import UrlNode
from drb.exceptions.core import DrbFactoryException


class TestDrbFactoryResolver(unittest.TestCase):
    mock_package_path: str = None
    signature_uuid: dict = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.signature_uuid = {
            'file': UUID('99e6ce18-276f-11ec-9621-0242ac130002'),
            'foobar': UUID('75eddcbc-2752-11ec-9621-0242ac130002'),
            'mem': UUID('09d14890-283b-11ec-9621-0242ac130002'),
            'zip': UUID('53794b50-2778-11ec-9621-0242ac130002'),
            'safe': UUID('c44c2f36-2779-11ec-9621-0242ac130002'),
            'sentinel_safe': UUID('4cd8fe12-827c-11ec-a8a3-0242ac120002'),
            'sentinel-1': UUID('84a54dea-2800-11ec-9621-0242ac130002'),
            'sentinel-1-level0': UUID('4d28758a-2806-11ec-9621-0242ac130002'),
            'sentinel-2-forced': UUID('a98046ec-95be-11ed-a1eb-0242ac120002'),
            'forced-failed': UUID('bff1d8a0-963b-11ed-a1eb-0242ac120002'),
            'xml': UUID('40123218-2b5e-11ec-8d3d-0242ac130003'),
            'txt': UUID('3d797648-281a-11ec-9621-0242ac130002')
        }

    def test_resolve_foobar(self):
        node = DrbLogicalNode('foobar:my-data')
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['foobar'], signature.id)

    def test_resolve_mem(self):
        node = DrbLogicalNode('mem:my-data')
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['mem'], signature.id)

    def test_resolve_file(self):
        path = os.getcwd()
        node = DrbLogicalNode(f'file://{path}')
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['file'], signature.id)

        node = DrbLogicalNode(path)
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['file'], signature.id)

        path = os.listdir(os.getcwd())[0]
        node = DrbLogicalNode(path)
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['file'], signature.id)

    def test_resolve_txt(self):
        source = os.path.join(os.path.dirname(__file__),
                              'resources/drivers/file/text.txt')
        signature, base_node = resolver.resolve(source)
        self.assertEqual(self.signature_uuid['txt'], signature.id)
        self.assertEqual("<class 'drb.drivers.text.TextNode'>",
                         str(type(base_node)))

        source = DrbLogicalNode(source)
        signature, base_node = resolver.resolve(source)
        self.assertEqual(self.signature_uuid['txt'], signature.id)
        self.assertEqual("<class 'drb.drivers.text.TextNode'>",
                         str(type(base_node)))

    def test_resolve_xml(self):
        node = DrbLogicalNode(os.path.join(os.path.dirname(__file__),
                                           'resources/drivers/xml/test.xml'))
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['xml'], signature.id)

    def test_resolve_safe_product(self):
        path = os.path.join(os.path.dirname(__file__),
                            'resources/drivers/file/TEST.SAFE')

        node = DrbLogicalNode(path)
        node.append_child(DrbLogicalNode('manifest.safe'))
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['sentinel_safe'], signature.id)

        node = DrbLogicalNode(path)
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['file'], signature.id)

    def test_resolve_sentinel_product(self):
        name = 'S1A_IW_SLC__1SDV_20211008T045534_20211008T045601_040023' \
               '_04BCCC_58BF.SAFE'
        node = DrbLogicalNode(name)
        node.append_child(DrbLogicalNode('manifest.safe'))
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['sentinel-1'], signature.id)

        name = 'S1A_IW_RAW__0SDV_20211008T045532_20211008T045604_040023' \
               '_04BCCC_56E7.SAFE'
        node = DrbLogicalNode(name)
        node.append_child(DrbLogicalNode('manifest.safe'))
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['sentinel-1-level0'],
                         signature.id)

    def test_cannot_resolve(self):
        node = DrbLogicalNode('foo:my-data')
        with self.assertRaises(DrbFactoryException):
            resolver.resolve(node)

    def test_create(self):
        uri = UrlNode('foobar:///path/to/my-data')
        node = resolver.create(uri)
        self.assertEqual("Foobar_my-data", node.name)

        uri = UrlNode('mem:/my/path/to/my_file')
        node = resolver.create(uri)
        self.assertEqual("Mem_my_file", node.name)

    def test_url_resolution(self):
        url = 'mockurl://path/to/resource.rs/sub/path/foobar.data'
        node = resolver.create(url)
        self.assertIsNotNone(node)
        self.assertEqual("<class 'drb.drivers.data.MockDataNode'>",
                         str(type(node)))
        self.assertEqual('foobar', node.name)

        url = 'fake://path/to/resource.rs/sub/path/foobar.fake'
        with self.assertRaises(DrbFactoryException):
            resolver.create(url)

    def test_override_resolution(self):
        node = DrbLogicalNode('TEST.SAFE')
        node.append_child(DrbLogicalNode('manifest.xml'))
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['sentinel_safe'], signature.id)

        node = DrbLogicalNode('TEST.SAFE')
        node.append_child(DrbLogicalNode('xfdumanifest.xml'))
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['sentinel_safe'], signature.id)

    def test_derivative_topic_with_factory(self):
        data = 'S1A_RF_RAW__0SDH_20140513T012339_20140513T012340_000572_' \
               '000747_31E3.SAFE'
        node = DrbLogicalNode(data)
        node.append_child(DrbLogicalNode('manifest.safe'))
        topic, node = resolver.resolve(node)
        self.assertEqual('Sentinel-1 Level 0 RF Product', topic.label)
        self.assertEqual(
            "<class 'drb.drivers.sentinel1.Sentinel1L0RFProduct'>",
            str(type(node)))

    def test_resolve_force_topic(self):
        source = os.path.join(os.path.dirname(__file__),
                              'resources/drivers/file/S2_failed.force')
        node = DrbLogicalNode(source)
        signature, base_node = resolver.resolve(node)
        self.assertEqual(self.signature_uuid['sentinel-2-forced'],
                         signature.id)

    def test_resolve_addon_impls(self):
        import pathlib
        name = pathlib.Path('.').absolute().name
        base_node = DrbLogicalNode('.')
        _, node = resolver.resolve(base_node)

        expected = {
            (io.FileIO, None),
            (io.BufferedReader, None),
            (str, 'hello'),
        }
        self.assertEqual(expected, set(node.impl_capabilities()))
        self.assertEqual(f'Hello {name}', node.get_impl(str))
