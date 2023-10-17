import os
import sys
import unittest
import uuid
from drb.core.signature import Signature
from drb.topics.topic import DrbTopic, TopicCategory
from drb.topics.dao import ManagerDao, DrbTopicDao
from drb.core.signature import parse_signature
from drb.exceptions.core import DrbException


class TestManagerDao(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = os.path.join(os.path.dirname(__file__),
                            'resources', 'packages')
        sys.path.append(path)

    def test_get_all_drb_topics(self):
        manager = ManagerDao()
        topics = manager.get_all_drb_topics()
        self.assertIsNotNone(topics)
        self.assertEqual(32, len(list(topics)))

    def test_get_drb_topic(self):
        manager = ManagerDao()
        identifier = uuid.UUID('3d797648-281a-11ec-9621-0242ac130002')
        label = 'Text'

        topic = manager.get_drb_topic(identifier)
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, DrbTopic)
        self.assertEqual(identifier, topic.id)
        self.assertEqual(label, topic.label)

    def test_is_subclass(self):
        manager = ManagerDao()
        foobar_id = uuid.UUID('75eddcbc-2752-11ec-9621-0242ac130002')
        safe_id = uuid.UUID('c44c2f36-2779-11ec-9621-0242ac130002')
        s1_id = uuid.UUID('84a54dea-2800-11ec-9621-0242ac130002')
        s1l0_id = uuid.UUID('4d28758a-2806-11ec-9621-0242ac130002')
        foobar = manager.get_drb_topic(foobar_id)
        safe = manager.get_drb_topic(safe_id)
        s1 = manager.get_drb_topic(s1_id)
        s1l0 = manager.get_drb_topic(s1l0_id)

        self.assertTrue(manager.is_subclass(foobar, foobar))
        self.assertTrue(manager.is_subclass(s1, safe))
        self.assertTrue(manager.is_subclass(s1l0, s1))
        self.assertTrue(manager.is_subclass(s1l0, safe))

        self.assertFalse(manager.is_subclass(foobar, safe))

    def test_get_parent(self):
        manager = ManagerDao()
        identifier = uuid.UUID('84a54dea-2800-11ec-9621-0242ac130002')

        parent_identifier = uuid.UUID('4cd8fe12-827c-11ec-a8a3-0242ac120002')
        parent_label = 'Sentinel SAFE Product'

        topic = manager.get_drb_topic(identifier)
        parents = manager.get_parents(topic)

        self.assertIsNotNone(parents)
        self.assertIsInstance(parents[0], DrbTopic)
        self.assertEqual(parent_identifier, parents[0].id)
        self.assertEqual(parent_label, parents[0].label)

    def test_get_children(self):
        manager = ManagerDao()
        identifier = uuid.UUID('4cd8fe12-827c-11ec-a8a3-0242ac120002')

        child_identifier = uuid.UUID('84a54dea-2800-11ec-9621-0242ac130002')
        child_label = 'Sentinel-1 Product'

        topic = manager.get_drb_topic(identifier)
        children = manager.get_children(topic)

        self.assertIsNotNone(children)
        self.assertIsInstance(children[0], DrbTopic)
        self.assertEqual(child_identifier, children[0].id)
        self.assertEqual(child_label, children[0].label)

    def test_save(self):
        data = {
            'id': uuid.UUID('93b508a0-6ee8-11ec-90d6-0242ac120003'),
            'subClassOf': [uuid.UUID('096ad7b2-e17b-4a4b-a6c3-c07ad5879203')],
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

        manager = ManagerDao()
        path_save = os.path.join(os.path.dirname(__file__),
                                 'resources', 'new_file.yml')

        dao = manager.add_dao(path_save)

        topic = manager.save(topic, dao)
        identifier = uuid.UUID('93b508a0-6ee8-11ec-90d6-0242ac120003')
        label = 'test'

        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, DrbTopic)
        self.assertEqual(identifier, topic.id)
        self.assertEqual(label, topic.label)

    def test_delete(self):
        path_delete = os.path.join(os.path.dirname(__file__),
                                   'resources', 'new_file.yml')

        manager = ManagerDao()
        manager.add_dao(path_delete)

        identifier = uuid.UUID('93b508a0-6ee8-11ec-90d6-0242ac120003')
        manager.delete(identifier)

        with self.assertRaises(DrbException):
            manager.get_drb_topic(identifier)

    def test_add_dao(self):
        manager = ManagerDao()

        path1 = os.path.join(os.path.dirname(__file__),
                             'resources', 'new_file.yml')
        path2 = os.path.join(os.path.dirname(__file__),
                             'resources', 'landsat.owl')
        path3 = os.path.join(os.path.dirname(__file__),
                             'resources', 'new_file.zip')

        dao1 = manager.add_dao(path1)
        self.assertIsNotNone(dao1)
        self.assertIsInstance(dao1, DrbTopicDao)

        dao2 = manager.add_dao(path2)
        self.assertIsNotNone(dao2)
        self.assertIsInstance(dao2, DrbTopicDao)

        with self.assertRaises(DrbException):
            manager.add_dao(path3)
