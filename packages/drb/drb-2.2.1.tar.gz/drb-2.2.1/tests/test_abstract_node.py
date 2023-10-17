import io
import unittest
import os

from drb.core import DrbNode, Predicate
from drb.exceptions.core import DrbException
from drb.nodes.logical_node import DrbLogicalNode


class MyPredicate(Predicate):
    def matches(self, node: DrbNode) -> bool:
        return 'a' == node.namespace_uri


class TestDrbNode(unittest.TestCase):
    node = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.node = DrbLogicalNode(os.getcwd())
        cls.node.append_child(DrbLogicalNode('data1.zip'))
        cls.node.append_child(DrbLogicalNode('data1.zip', namespace_uri='a'))
        child = DrbLogicalNode('data2.txt')
        child @= ('occurrence', 1)
        cls.node.append_child(child)
        child = DrbLogicalNode('data2.txt')
        child @= ('occurrence', 2)
        cls.node.append_child(child)
        cls.node.append_child(DrbLogicalNode('data2.txt', namespace_uri='b'))

    def test_getitem_int(self):
        node = self.node[1]
        self.assertEqual('data1.zip', node.name)
        self.assertEqual('a', node.namespace_uri)
        self.assertEqual("<class 'drb.drivers.zip.ZipNode'>",
                         str(node.__class__))

        with self.assertRaises(IndexError):
            node = self.node[42]
        self.assertEqual(self.node[-1], self.node[len(self.node)-1])

    def test_del_attr(self):
        node = DrbLogicalNode('test')
        node @= ('one', 1)
        node @= ('two', 2)
        node @= ('three', 3)

        self.assertEqual(len(node._attrs), 3)
        node @= ('one', None)
        self.assertEqual(len(node._attrs), 2)
        node @= ('two', None)
        self.assertEqual(len(node._attrs), 1)
        node @= ('three', None)
        self.assertEqual(len(node._attrs), 0)

    def test_getitem_slice(self):
        nodes = self.node[1:3]
        self.assertIsInstance(nodes, list)
        self.assertEqual(2, len(nodes))
        self.assertEqual('data1.zip', nodes[0].name)
        self.assertEqual('a', nodes[0].namespace_uri)
        self.assertEqual('data2.txt', nodes[1].name)
        self.assertEqual(1, nodes[1].get_attribute('occurrence'))
        self.assertEqual(1, nodes[1] @ 'occurrence')

        nodes = self.node[:]
        self.assertIsInstance(nodes, list)
        self.assertEqual(5, len(nodes))

    def test_getitem_str(self):
        data = self.node['data2.txt']
        self.assertEqual(1, data.get_attribute('occurrence'))
        self.assertEqual(1, data @ 'occurrence')
        self.assertEqual("<class 'drb.drivers.text.TextNode'>",
                         str(data.__class__))

        with self.assertRaises(KeyError):
            data = self.node['foobar']

    def test_getitem_tuple(self):
        data = self.node['data2.txt', 'b']
        # self.assertIsInstance(data, DrbNode)
        # self.assertEqual('data2.txt', data.name)
        # self.assertEqual('b', data.namespace_uri)
        # self.assertEqual("<class 'drb.drivers.text.TextNode'>",
        #                  str(data.__class__))
        #
        # data = self.node['data2.txt', 1]
        # self.assertIsInstance(data, DrbNode)
        # self.assertEqual(2, data.get_attribute('occurrence'))
        # self.assertEqual(2, data @ 'occurrence')
        # self.assertEqual("<class 'drb.drivers.text.TextNode'>",
        #                  str(data.__class__))
        #
        # data = self.node['data1.zip', 'a', 0]
        # self.assertIsInstance(data, DrbNode)
        # self.assertEqual('data1.zip', data.name)
        # self.assertEqual('a', data.namespace_uri)
        # self.assertEqual("<class 'drb.drivers.zip.ZipNode'>",
        #                  str(data.__class__))
        #
        # data = self.node['data1.zip', None, 0]
        # self.assertIsInstance(data, DrbNode)
        # self.assertIsNone(data.namespace_uri)
        # self.assertEqual("<class 'drb.drivers.zip.ZipNode'>",
        #                  str(data.__class__))
        #
        # data = self.node['data1.zip', 1]
        # self.assertIsNotNone(data)
        # self.assertEqual('data1.zip', data.name)
        # self.assertEqual('a', data.namespace_uri)
        #
        # data = self.node['data2.txt', :2]
        # self.assertIsNotNone(data)
        # self.assertIsInstance(data, list)
        # self.assertEqual(2, len(data))
        # self.assertEqual('data2.txt', data[0].name)
        # self.assertEqual(1, data[0] @ 'occurrence')
        # self.assertEqual('data2.txt', data[1].name)
        # self.assertEqual(2, data[1] @ 'occurrence')

        with self.assertRaises(KeyError):
            data = self.node['data2.txt', ]
        with self.assertRaises(KeyError):
            data = self.node['data1.zip', 42]
        with self.assertRaises(KeyError):
            data = self.node['foobar', 3]

    def test_getitem_predicate(self):
        data = self.node[MyPredicate()]
        self.assertIsInstance(data, list)
        self.assertEqual(1, len(data))
        self.assertEqual("a", data[0].namespace_uri)
        self.assertEqual("<class 'drb.drivers.zip.ZipNode'>",
                         str(data[0].__class__))

    def test_impl(self):
        self.assertFalse(self.node.has_impl(str))
        self.assertFalse(self.node.has_impl(io.BytesIO))
        self.assertFalse(self.node.has_impl(io.BufferedReader))
        self.assertFalse(self.node.has_impl(io.BufferedIOBase))
        self.assertEqual([], self.node.impl_capabilities())
        with self.assertRaises(DrbException):
            self.node.get_impl(io.BytesIO)
        with self.assertRaises(DrbException):
            self.node.get_impl(int)

    def test_setitem(self):
        node = self.node['data2.txt', 1]
        self.assertEqual(len(node), 0)

        node[None] = DrbLogicalNode('Test_0')

        self.assertEqual(len(node), 1)
        self.assertEqual(node[0].name, 'Test_0')

        node['Test_0'] = DrbLogicalNode('Test_1')
        self.assertEqual(node[0].name, 'Test_1')

        with self.assertRaises(KeyError):
            node['Toto'] = DrbLogicalNode('Toto')

    def test_eq_path(self):
        self.assertEqual(DrbLogicalNode('/toto'), DrbLogicalNode('/toto'))
        self.assertNotEqual(DrbLogicalNode('/Toto'), DrbLogicalNode('/Tata'))

    def test_delitem(self):
        node = self.node['data2.txt', 1]
        node[None] = DrbLogicalNode('Test_0')

        self.assertEqual(len(node), 1)
        self.assertEqual(node[0].name, 'Test_0')

        del node['Test_0']
        with self.assertRaises(IndexError):
            node[0].name
        with self.assertRaises(KeyError):
            del node['Test_0']
        self.assertEqual(len(node), 0)

    def test_namespace_11(self):
        # Case 1.1: node with ns / user access with ns / aware = True
        root = DrbLogicalNode("root")
        ns = 'http://www.gael.fr/drb/item'
        ns_node = DrbLogicalNode('xml', namespace_uri=ns)

        root.append_child(ns_node)
        root.namespace_aware = True

        self.assertIsNotNone(root['xml', ns])
        with self.assertRaises(KeyError):
            self.assertIsNone(root['xml', ns + 'bad_ns'])

    def test_namespace_12(self):
        # Case 1.2: node with ns / user access with ns / aware = False
        root = DrbLogicalNode("root")
        ns = 'http://www.gael.fr/drb/item'
        ns_node = DrbLogicalNode('xml', namespace_uri=ns)

        root.append_child(ns_node)
        ns_node.namespace_aware = False

        self.assertIsNotNone(root['xml', ns])
        with self.assertRaises(KeyError):
            node = root['xml', ns + 'bad_ns']

    def test_namespace_21(self):
        # Case 2.1: node without ns / user access with ns / aware = True
        root = DrbLogicalNode("root")
        ns = 'http://www.gael.fr/drb/item'
        ns_node = DrbLogicalNode('xml')

        root.append_child(ns_node)
        root.namespace_aware = True

        with self.assertRaises(KeyError):
            node = root['xml', ns]

    def test_namespace_22(self):
        # Case 2.2: node without ns / user access with ns / aware = False
        root = DrbLogicalNode("root")
        ns = 'http://www.gael.fr/drb/item'
        ns_node = DrbLogicalNode('xml')

        root.append_child(ns_node)
        ns_node.namespace_aware = False

        with self.assertRaises(KeyError):
            node = root['xml', ns]

    def test_namespace_31(self):
        # Case 3.1: node with ns / user access without ns / aware = True
        root = DrbLogicalNode("root")
        ns = 'http://www.gael.fr/drb/item'
        ns_node = DrbLogicalNode('xml', namespace_uri=ns)

        root.append_child(ns_node)
        root.namespace_aware = True

        with self.assertRaises(KeyError):
            node = root['xml']

    def test_namespace_32(self):
        # Case 3.2: node with ns / user access without ns / aware = False
        root = DrbLogicalNode("root")
        ns = 'http://www.gael.fr/drb/item'
        ns_node = DrbLogicalNode('xml', namespace_uri=ns)

        root.append_child(ns_node)
        ns_node.namespace_aware = False

        self.assertIsNotNone(root['xml'])

    def test_namespace_41(self):
        # Case 4.1: node without ns / user access without ns / aware = True
        root = DrbLogicalNode("root")
        ns_node = DrbLogicalNode('xml')

        root.append_child(ns_node)
        root.namespace_aware = True

        self.assertIsNotNone(root['xml'])

    def test_namespace_42(self):
        # Case 4.1: node without ns / user access without ns / aware = False
        root = DrbLogicalNode("root")
        ns_node = DrbLogicalNode('xml')

        root.append_child(ns_node)
        ns_node.namespace_aware = False

        self.assertIsNotNone(root['xml'])

    def test_namespace_aware_transitivity(self):
        root = DrbLogicalNode('root')
        self.assertFalse(root.namespace_aware)

        a_child = DrbLogicalNode('a')
        a_child.append_child(DrbLogicalNode('aa'))
        a_child.append_child(DrbLogicalNode('ab', namespace_uri='a'))
        b_child = DrbLogicalNode('b')
        b_child.append_child(DrbLogicalNode('ba'))
        b_child.append_child(DrbLogicalNode('bb', namespace_uri='b'))
        root.append_child(a_child)
        root.append_child(b_child)

        # Default namespace_aware value (False)
        self.assertFalse(root['a'].namespace_aware)
        self.assertFalse(root['a']['aa'].namespace_aware)
        node = root['a']['ab']
        self.assertIsNotNone(node)
        self.assertFalse(node.namespace_aware)
        self.assertEqual('a', node.namespace_uri)
        self.assertFalse(root['a']['ab'].namespace_aware)
        self.assertFalse(root['b'].namespace_aware)
        self.assertFalse(root['b']['ba'].namespace_aware)
        node = root['b']['bb']
        self.assertIsNotNone(node)
        self.assertFalse(node.namespace_aware)
        self.assertEqual('b', node.namespace_uri)

        # set namespace_aware to True only on root node
        root.namespace_aware = True
        self.assertTrue(root['a'].namespace_aware)
        self.assertTrue(root['a']['aa'].namespace_aware)
        with self.assertRaises(KeyError):
            node = root['a']['ab']
        self.assertTrue(root['b'].namespace_aware)
        self.assertTrue(root['b']['ba'].namespace_aware)
        with self.assertRaises(KeyError):
            node = root['b']['bb']

        # Override namespace_aware property
        root.namespace_aware = False
        b_child.namespace_aware = True
        self.assertFalse(root['a'].namespace_aware)
        self.assertFalse(root['a']['aa'].namespace_aware)
        self.assertFalse(root['a']['ab'].namespace_aware)
        self.assertTrue(root['b'].namespace_aware)
        self.assertTrue(root['b']['ba'].namespace_aware)
        with self.assertRaises(KeyError):
            node = root['b']['bb']

    def test_has_child(self):
        self.assertTrue(self.node.has_child())

        self.assertTrue(self.node.has_child('data1.zip'))
        self.assertTrue(self.node.has_child('data2.txt'))
        self.assertFalse(self.node.has_child('data3.dat'))

        self.assertTrue(self.node.has_child(namespace='a'))
        self.assertTrue(self.node.has_child(namespace='b'))
        self.assertFalse(self.node.has_child(namespace='c'))

        self.assertTrue(self.node.has_child('data1.zip', 'a'))
        self.assertTrue(self.node.has_child('data2.txt', 'b'))
        self.assertFalse(self.node.has_child('data2.txt', 'c'))
        self.assertFalse(self.node.has_child('data2.txt', 'a'))
