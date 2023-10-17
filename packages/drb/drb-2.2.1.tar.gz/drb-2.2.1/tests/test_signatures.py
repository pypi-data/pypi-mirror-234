from drb.core import DrbNode, Signature
from drb.nodes.logical_node import DrbLogicalNode
from drb.signatures.core import (
    NameSignature,
    NamespaceSignature,
    PathSignature,
    SignatureAggregator,
    AttributesSignature,
    ChildrenSignature,
    PythonSignature,
)
import unittest
import drb.core.signature as signatures


class BoolSignature(Signature):

    def __init__(self, boolean: bool):
        self._match = boolean

    def matches(self, node: DrbNode) -> bool:
        return self._match

    def to_dict(self) -> dict:
        return {self.get_name(): self._match}

    @staticmethod
    def get_name():
        return 'bool'


class TestSignatures(unittest.TestCase):
    def test_name_signature(self):
        node = DrbLogicalNode('foobar')

        signature = NameSignature('foobar')
        self.assertTrue(signature.matches(node))

        signature = NameSignature('^fo+bar')
        self.assertTrue(signature.matches(node))

        signature = NameSignature('other')
        self.assertFalse(signature.matches(node))

        signature = NameSignature('f[0-9]+bar$')
        self.assertFalse(signature.matches(node))

    def test_namespace_signature(self):
        ns = 'https://gael-systems.com'
        node = DrbLogicalNode('test', namespace_uri=ns)

        signature = NamespaceSignature(ns)
        self.assertTrue(signature.matches(node))

        node.namespace_uri = 'https://fake.namespace.com'
        self.assertFalse(signature.matches(node))

    def test_path_signature(self):
        node = DrbLogicalNode('https://gael-systems.com/drb/test-data.dat')

        signature = PathSignature('^(file)?://.+')
        self.assertFalse(signature.matches(node))

        signature = PathSignature('^http(s)?://.+')
        self.assertTrue(signature.matches(node))

    def test_attributes_signature(self):
        node = DrbLogicalNode('test')
        node.add_attribute('odata-version', '4.0')
        node.add_attribute('drb', True, 'test')

        data = [{'name': 'odata-version'}]
        signature = AttributesSignature(data)
        self.assertTrue(signature.matches(node))

        data = [{'name': 'odata-version', 'value': '4.0'}]
        signature = AttributesSignature(data)
        self.assertTrue(signature.matches(node))

        data = [{'name': 'odata-version', 'value': 4.0}]
        signature = AttributesSignature(data)
        self.assertFalse(signature.matches(node))

        data = [{'name': 'odata-version', 'namespace': 'test'}]
        signature = AttributesSignature(data)
        self.assertFalse(signature.matches(node))

        data = [{'name': 'drb', 'namespace': 'test'}]
        signature = AttributesSignature(data)
        self.assertTrue(signature.matches(node))

        data = [{'name': 'drb', 'namespace': 'test', 'value': True}]
        signature = AttributesSignature(data)
        self.assertTrue(signature.matches(node))

        data = [{'name': 'drb', 'namespace': 'test', 'value': 'True'}]
        signature = AttributesSignature(data)
        self.assertFalse(signature.matches(node))

    def test_children_signature(self):
        node = DrbLogicalNode('tests')
        child = DrbLogicalNode('subtest_1', namespace_uri='root')
        node.append_child(child)
        child = DrbLogicalNode('subtest_2')
        node.append_child(child)
        child = DrbLogicalNode('subtest_2', namespace_uri='sub')
        node.append_child(child)

        data = [{'name': 'subtest_[0-9]+'}]
        signature = ChildrenSignature(data)
        self.assertTrue(signature.matches(node))

        data = [{'name': 'subtest_[0-9]+', 'namespace': 'root'}]
        signature = ChildrenSignature(data)
        self.assertTrue(signature.matches(node))

        data = [{'name': 'subtest_[0-9]+', 'namespaceAware': True}]
        signature = ChildrenSignature(data)
        self.assertTrue(signature.matches(node))

        data = [{'name': 'subtest_2', 'namespace': 'test'}]
        signature = ChildrenSignature(data)
        self.assertFalse(signature.matches(node))

        data = [{'name': 'subtest_1', 'namespaceAware': True}]
        signature = ChildrenSignature(data)
        self.assertFalse(signature.matches(node))

    def test_python_signature(self):
        node = DrbLogicalNode('foobar')
        node.add_attribute('Content-Type',
                           'application/json;odata.metadata=minimal')
        node.value = 25
        node.append_child(DrbLogicalNode('child1'))
        node.append_child(DrbLogicalNode('child2'))

        # node match the signature
        code = """
value = node.get_attribute('Content-Type')
return 'application/json' in value
        """
        signature = PythonSignature(code)
        self.assertTrue(signature.matches(node))

        code = '''from math import sqrt
return sqrt(node.value) == 5
        '''
        signature = PythonSignature(code)
        self.assertTrue(signature.matches(node))

        # node unmatched the signature
        code = 'return len(node) == 3'
        signature = PythonSignature(code)
        self.assertFalse(signature.matches(node))

        # the signature does not return a boolean
        code = 'return sqrt(9)'
        signature = PythonSignature(code)
        self.assertFalse(signature.matches(node))

        # raise an exception
        code = 'raise ValueError("Invalid value")'
        signature = PythonSignature(code)
        self.assertFalse(signature.matches(node))

    def test_signature_aggregator(self):
        sig_list = []
        node = DrbLogicalNode('.')
        signature = SignatureAggregator(sig_list)
        self.assertFalse(signature.matches(node))

        sig_list.append(BoolSignature(True))
        signature = SignatureAggregator(sig_list)
        self.assertTrue(signature.matches(node))

        sig_list.append(BoolSignature(False))
        signature = SignatureAggregator(sig_list)
        self.assertFalse(signature.matches(node))

    def test_parse_signature(self):
        node = DrbLogicalNode('data.dat')
        node.add_attribute('test', True)

        data = {'name': r'.+\.dat', 'attributes': [{'name': 'test'}]}
        signature = signatures.parse_signature(data)
        self.assertIsNotNone(signature)
        self.assertIsInstance(signature, SignatureAggregator)
        self.assertTrue(signature.matches(node))

    def test_get_signature(self):
        signature = signatures.get('name')
        self.assertEqual(NameSignature, signature)

        signature = signatures.get('python')
        self.assertEqual(PythonSignature, signature)

        # test to retrieve an unknown signature
        with self.assertRaises(KeyError):
            signatures.get('unknown')
