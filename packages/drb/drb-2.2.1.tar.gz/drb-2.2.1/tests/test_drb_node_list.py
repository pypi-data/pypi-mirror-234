import unittest

from drb.topics.resolver import DrbNodeList
from drb.nodes.logical_node import DrbLogicalNode
from drb.exceptions.core import DrbFactoryException
from tests.utils import DrbTestNode


class TestDrbNodeList(unittest.TestCase):
    def test_int_item(self):
        children = DrbNodeList([DrbLogicalNode('mem://foo'),
                                DrbLogicalNode('mem://bar'),
                                DrbLogicalNode('foobar://foo'),
                                DrbLogicalNode('foobar://bar'),
                                DrbLogicalNode('s3://gael-systems/data')])
        self.assertEqual('Mem_foo', children[0].name)
        self.assertEqual('Mem_bar', children[1].name)
        self.assertEqual('Foobar_foo', children[2].name)
        self.assertEqual('Foobar_bar', children[3].name)
        self.assertEqual('data', children[4].name)
        self.assertIsInstance(children[-1], DrbLogicalNode)

    def test_slice_item(self):
        children = DrbNodeList([DrbLogicalNode('mem://foo'),
                                DrbLogicalNode('mem://bar'),
                                DrbLogicalNode('foobar://foo'),
                                DrbLogicalNode('foobar://foo')])
        result = children[1:3]
        self.assertEqual(2, len(result))
        self.assertEqual('Mem_bar', result[0].name)
        self.assertEqual('Foobar_foo', result[1].name)

    def test_unexpected_item(self):
        children = DrbNodeList([DrbLogicalNode('.')])
        with self.assertRaises(TypeError):
            print(children['.'])

    def test_not_supported_action(self):
        node = DrbTestNode('HelloWorld')
        node.append_child(DrbLogicalNode('mem:data1'))
        node.append_child(DrbLogicalNode('mem:data2'))
        node.append_child(DrbLogicalNode('mem:data3'))

        children = node.children
        with self.assertRaises(DrbFactoryException):
            children.append(DrbLogicalNode('test'))
        with self.assertRaises(DrbFactoryException):
            children.insert(0, DrbLogicalNode('test'))
        with self.assertRaises(DrbFactoryException):
            children = children + [DrbLogicalNode('test')]
        with self.assertRaises(DrbFactoryException):
            children = [DrbLogicalNode('test')] + children
        with self.assertRaises(DrbFactoryException):
            children += DrbLogicalNode('test')
        with self.assertRaises(DrbFactoryException):
            children.extend(range(2))
        with self.assertRaises(DrbFactoryException):
            children[0] = DrbLogicalNode('foobar://bar')
        with self.assertRaises(DrbFactoryException):
            children.clear()
        with self.assertRaises(DrbFactoryException):
            children.pop(0)
        with self.assertRaises(DrbFactoryException):
            children.remove(0)
        with self.assertRaises(DrbFactoryException):
            children.reverse()
        with self.assertRaises(DrbFactoryException):
            children.sort()
        with self.assertRaises(DrbFactoryException):
            children.count(DrbLogicalNode('test'))
        with self.assertRaises(DrbFactoryException):
            children.copy()
        with self.assertRaises(DrbFactoryException):
            children == children
        with self.assertRaises(DrbFactoryException):
            children != children

    def test_get_resolved_node(self):
        node = DrbTestNode('foobar')
        node.append_child(DrbLogicalNode('foobar://foo'))
        self.assertEqual('Foobar_foo', node.children[0].name)
