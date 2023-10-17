import unittest
import uuid

from drb.topics.topic import DrbTopic, TopicCategory
from drb.nodes.logical_node import DrbLogicalNode
from drb.core.factory import FactoryLoader
from drb.core.signature import parse_signature
from tests.utils import DrbTestFactory


class TestDrbTopic(unittest.TestCase):
    def test_drb_topic(self):
        data = {
            'id': uuid.UUID('93b508a0-6ee8-11ec-90d6-0242ac120003'),
            'subClassOf': uuid.UUID('096ad7b2-e17b-4a4b-a6c3-c07ad5879203'),
            'label': 'test',
            'description': 'test topic description',
            'category': TopicCategory('FORMATTING'),
            'factory': 'test',
            'signatures': [
                parse_signature({'name': 'test_.+'}),
                parse_signature({'name': '.+_test'}),
            ]
        }

        topic = DrbTopic(**data)
        self.assertEqual(data['id'], topic.id)
        self.assertEqual(data['subClassOf'], topic.subClassOf)
        self.assertEqual(data['label'], topic.label)
        self.assertEqual(data['description'], topic.description)
        self.assertEqual(TopicCategory.FORMATTING, topic.category)

        FactoryLoader().get_factory(topic.factory)
        factory = FactoryLoader().get_factory(topic.factory)
        self.assertIsNotNone(factory)
        self.assertIsInstance(factory, DrbTestFactory)

        self.assertEqual(2, len(topic.signatures))
        self.assertTrue(topic.matches(DrbLogicalNode('test_foobar')))
        self.assertTrue(topic.matches(DrbLogicalNode('foobar_test')))
        self.assertFalse(topic.matches(DrbLogicalNode('foobar')))
