import unittest
import os
import uuid
import drb.core.signature
from drb.topics.topic import DrbTopic
from drb.topics.dao.xml_dao import XmlDao
from drb.exceptions.core import DrbException


class TestXmlDao(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = os.path.join(os.path.dirname(__file__),
                            'resources', 'landsat.owl')
        cls.dao = XmlDao(path)

    def test_read(self):
        identifier = uuid.UUID('dc26dbe5-d09e-3d53-a555-802844716688')
        label = 'Landsat-8 Level-1 GeoTIFF Image'
        topic = self.dao.read(identifier)

        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, DrbTopic)
        self.assertEqual(identifier, topic.id)
        self.assertEqual(label, topic.label)

    def test_find(self):
        search = 'Landsat-8 Level-1 GeoTIFF Folder Collection'
        topics = self.dao.find(search)

        self.assertIsNotNone(topics)
        self.assertEqual(3, len(list(topics)))
        found_topic = None

        for topic in topics:
            self.assertIsInstance(topic, DrbTopic)
            if topic.label == 'Landsat-8 Level-1 GeoTIFF Folder' \
                              ' Collection 1 Product (L1T)':
                found_topic = topic
                continue

        self.assertIsNotNone(found_topic)

    def test_read_all(self):
        topics = self.dao.read_all()

        self.assertIsNotNone(topics)
        self.assertEqual(16, len(list(topics)))

    def test_create(self):
        search = 'Landsat-8 Level-1 Metadata Text File'
        topics = self.dao.find(search)

        with self.assertRaises(NotImplementedError):
            self.dao.create(topics[0])

    def test_update(self):
        search = 'Landsat-8 Level-1 Ground Control Points File'
        topics = self.dao.find(search)

        with self.assertRaises(NotImplementedError):
            self.dao.create(topics[0])

    def test_delete(self):
        identifier = uuid.UUID('cf502e4c-b410-312d-9b16-089c9f299a22')
        with self.assertRaises(NotImplementedError):
            self.dao.delete(identifier)
