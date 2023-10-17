import unittest
import os
import uuid
import sys
import os
import drb.core.signature
from drb.topics.dao.rdf_dao import RDFDao
import drb.topics.resolver as resolver
from drb.topics.dao.manager_dao import ManagerDao
from drb.topics.dao.topic_dao import DrbTopicDao
from drb.topics.topic import DrbTopic


class TestRDFDao(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.path = os.path.join(os.path.dirname(__file__),
                                'resources', 'landsat-8-topic.ttl')
        cls.dao = RDFDao(cls.path)

    def test_read(self):
        identifier = uuid.UUID('f23a13eb-1ecd-3cf6-8bf8-fa32d2957de5')
        label = 'Landsat-8 Product: Level-1: GeoTIFF: Image band (10-11) 2017+'
        topic = self.dao.read(identifier)

        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, DrbTopic)
        self.assertEqual(identifier, topic.id)
        self.assertEqual(label, topic.label)

    def test_find(self):
        search = 'Landsat-8 Product: Level-1: GeoTIFF: Image'
        topics = self.dao.find(search)

        self.assertIsNotNone(topics)
        self.assertEqual(7, len(list(topics)))
        found_topic = None

        for topic in topics:
            self.assertIsInstance(topic, DrbTopic)
            if topic.label == 'Landsat-8 Product: Level-1: GeoTIFF:' \
                              ' Image band (10-11) 2017+':
                found_topic = topic
                continue

        self.assertIsNotNone(found_topic)

    def test_read_all(self):
        topics = self.dao.read_all()

        self.assertIsNotNone(topics)
        self.assertEqual(21, len(list(topics)))

    def test_create(self):
        search = 'Landsat-8 Level-1 Metadata Text File'
        topic = self.dao.find(search)

        with self.assertRaises(NotImplementedError):
            self.dao.create(topic)

    def test_update(self):
        search = 'Landsat-8'
        topics = self.dao.find(search)

        with self.assertRaises(NotImplementedError):
            self.dao.create(topics[0])

    def test_delete(self):
        identifier = uuid.UUID('cf502e4c-b410-312d-9b16-089c9f299a22')
        with self.assertRaises(NotImplementedError):
            self.dao.delete(identifier)
