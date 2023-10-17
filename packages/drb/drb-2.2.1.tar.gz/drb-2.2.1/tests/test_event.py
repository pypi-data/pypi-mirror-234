from drb.core import EventManager
from .utils import Counter
import random
import unittest


class TestEventManager(unittest.TestCase):
    def test_add_event_type(self):
        event_type = 'test'
        counter = Counter()
        events = EventManager()

        with self.assertRaises(KeyError):
            events.register(event_type, counter.increase_counter)

        events.append_event_type(event_type)
        events.register(event_type, counter.increase_counter)

    def test_register(self):
        events = EventManager()
        counter = Counter()

        events.append_event_type('foo')
        events.register('foo', counter.increase_counter)
        times = random.randint(1, 10)
        for _ in range(times):
            events.notify('foo')
        self.assertEqual(times, counter.count)

        with self.assertRaises(ValueError):
            events.register('foo', 42)

    def test_unregister(self):
        event_type = 'foo'
        events = EventManager()
        counter = Counter()

        events.append_event_type(event_type)
        events.register(event_type, counter.increase_counter)
        events.notify(event_type)
        events.notify(event_type)
        events.unregister(event_type, counter.increase_counter)
        events.notify(event_type)
        events.notify(event_type)
        self.assertEqual(2, counter.count)

        # should not raise any exception
        events.unregister('bar', counter.increase_counter)
