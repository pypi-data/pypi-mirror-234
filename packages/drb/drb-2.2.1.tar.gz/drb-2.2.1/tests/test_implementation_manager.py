import unittest
from drb.core.impls import ImplementationManager
from drb.core.node import DrbNode


def function_1(node: DrbNode, **kwargs):
    pass


def function_2(node: DrbNode, **kwargs):
    pass


def function_3(node: DrbNode, **kwargs):
    pass


class TestImplManager(unittest.TestCase):
    def test_add_impl(self):
        mng = ImplementationManager()
        self.assertEqual([], mng.get_capabilities())
        mng.add_impl(str, None, lambda x: x)
        self.assertEqual([(str, None)], mng.get_capabilities())

    def test_remove_impl(self):
        mng = ImplementationManager()
        mng.add_impl(str, None, function_1)
        mng.add_impl(str, 'test', function_2)
        mng.add_impl(dict, 'test', function_3)

        expected = {(str, None), (str, 'test'), (dict, 'test')}
        self.assertEqual(expected, set(mng.get_capabilities()))

        mng.remove_impl(str)
        expected.remove((str, None))
        self.assertEqual(expected, set(mng.get_capabilities()))

        mng.remove_impl(dict)

    def test_has_impl(self):
        mng = ImplementationManager()
        mng.add_impl(str, None, lambda x: x)
        mng.add_impl(str, 'test', lambda x: x)
        mng.add_impl(list, 'test', lambda x: x)

        self.assertTrue(mng.has_impl(str))
        self.assertTrue(mng.has_impl(str, 'test'))
        self.assertTrue(mng.has_impl(list, 'test'))
        self.assertTrue(mng.has_impl(list))
        self.assertFalse(mng.has_impl(list, 'other'))
        self.assertFalse(mng.has_impl(dict))

    def test_get_impl(self):
        mng = ImplementationManager()
        mng.add_impl(str, None, function_1)
        mng.add_impl(str, 'test', function_2)
        mng.add_impl(list, 'test', function_3)

        self.assertEqual(function_1, mng.get_impl(str))
        self.assertEqual(function_2, mng.get_impl(str, 'test'))
        self.assertEqual(function_3, mng.get_impl(list, 'test'))
        self.assertEqual(function_3, mng.get_impl(list))

        with self.assertRaises(KeyError):
            mng.get_impl(str, 'foobar')
        with self.assertRaises(KeyError):
            mng.get_impl(dict)

    def test_get_capabilities(self):
        mng = ImplementationManager()
        self.assertEqual([], mng.get_capabilities())

        mng.add_impl(str, None, lambda x: x)
        mng.add_impl(str, 'test', lambda x: x)
        mng.add_impl(list, 'test', lambda x: x)

        expected = {(str, None), (str, 'test'), (list, 'test')}
        self.assertEqual(expected, set(mng.get_capabilities()))
