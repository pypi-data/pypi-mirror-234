import unittest
import os
import uuid
from typing import List
from drb.topics.dao.yaml_dao import YamlDao
from drb.topics.topic import DrbTopic, TopicCategory
from drb.core.signature import parse_signature
from drb.exceptions.core import DrbException


class TestYamlDao(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = os.path.join(os.path.dirname(__file__),
                            'resources', 'S3.yml')
        cls.dao = YamlDao(path)

    def test_read(self):
        identifier = uuid.UUID('300c6ea1-6a99-4e5c-b31d-6894504756de')
        label = 'Sentinel-3 SYNERGIE Level-2 V10 Product'
        topic = self.dao.read(identifier)

        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, DrbTopic)
        self.assertEqual(identifier, topic.id)
        self.assertEqual(label, topic.label)

    def test_find(self):
        search = 'Sentinel-3 SYNERGIE Level-2 V'
        topics = self.dao.find(search)

        self.assertIsNotNone(topics)
        self.assertEqual(5, len(list(topics)))
        found_topic = None

        for topic in topics:
            self.assertIsInstance(topic, DrbTopic)
            if topic.label == 'Sentinel-3 SYNERGIE Level-2 V10 Product':
                found_topic = topic
                continue

        self.assertIsNotNone(found_topic)

    def test_read_all(self):

        topics = self.dao.read_all()

        self.assertIsNotNone(topics)
        self.assertIsInstance(topics, List)
        self.assertEqual(8, len(list(topics)))

    def test_create(self):
        data = {
            'id': uuid.UUID('93b508a0-6ee8-11ec-90d6-0242ac120008'),
            'subClassOf': [uuid.UUID('096ad7b2-e17b-4a4b-a6c3-c07ad5879408')],
            'label': 'test_create',
            'description': 'create topic description',
            'category': TopicCategory('CONTAINER'),
            'factory': 'test',
            'signatures': [
                parse_signature({'name': 'test_.+'}),
                parse_signature({'name': '.+_test'}),
            ]
        }

        topic = DrbTopic(**data)

        path_create = os.path.join(os.path.dirname(__file__),
                                   'resources', 'new_file.yml')

        dao = YamlDao(path_create)

        topic = dao.create(topic)
        identifier = uuid.UUID('93b508a0-6ee8-11ec-90d6-0242ac120008')
        label = 'test_create'

        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, DrbTopic)
        self.assertEqual(identifier, topic.id)
        self.assertEqual(label, topic.label)

    def test_update(self):
        path_update = os.path.join(os.path.dirname(__file__),
                                   'resources', 'new_file.yml')

        dao = YamlDao(path_update)

        identifier = uuid.UUID('93b508a0-6ee8-11ec-90d6-0242ac120008')
        label = 'test_update'

        topic = dao.read(identifier)
        topic.label = label

        topic = dao.update(topic)

        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, DrbTopic)
        self.assertEqual(identifier, topic.id)
        self.assertEqual(label, topic.label)
