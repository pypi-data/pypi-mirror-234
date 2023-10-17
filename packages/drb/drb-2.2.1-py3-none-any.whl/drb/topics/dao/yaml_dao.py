import os

import yaml
import logging
import uuid
import jsonschema
from pathlib import Path
from typing import List

from .topic_dao import DrbTopicDao
from drb.core.factory import FactoryLoader
from drb.core.signature import parse_signature
from drb.topics.topic import DrbTopic, TopicCategory
from drb.exceptions.core import DrbException


logger = logging.getLogger('DrbTopic')


class YamlDao(DrbTopicDao):
    """
    Manages different operations on YAML files.
    """
    __schema_path = os.path.join(
        os.path.dirname(__file__), 'topic_schema.yml')
    __schema = None

    @classmethod
    def validate(cls, path: str):
        """
        Checks validity of a topic description file.
        Parameters:
            path (str): path of topic description file
        Raises:
            FileNotFoundError - if path does not exist
            ValidationError - if the description file is not valid
        """
        if cls.__schema is None:
            with open(cls.__schema_path) as file:
                cls.__schema = yaml.safe_load(file)

        with open(path) as file:
            for it in yaml.safe_load_all(file):
                jsonschema.validate(it, cls.__schema)

    def __init__(self, path: str):
        # if not existing, generate a new file.
        Path(path).touch(exist_ok=True)
        self.validate(path)

        self.__file = path

    @staticmethod
    def __write_topic_to_yaml_file(topic: DrbTopic) -> dict:
        """
        Converts a topic into a dictionary used for writing YAML file.
        Parameters:
            topic (YamlTopic): topic to convert
        Returns:
            dict: dictionary containing topic information
        """
        data = {'id': str(topic.id), 'label': topic.label,
                'category': topic.category.value}

        if topic.subClassOf is not None:
            data['subClassOf'] = str(topic.subClassOf[0])
        if topic.description is not None:
            data['description'] = topic.description

        if topic.factory is not None:
            data['factory'] = topic.factory

        if topic.signatures is not None:
            signs = topic.signatures
            data['signatures'] = [s.to_dict() for s in signs]

        return data

    @staticmethod
    def __generate_topic_from_yaml_file(ic_data: dict) -> DrbTopic:
        """
        Generates a DrbTopic using a dictionary from YAML file.
        Parameters:
            ic_data (dict): dictionary from YAML file
        Returns:
            DrbTopic: the corresponding topic
        """
        data = {'id': uuid.UUID(ic_data['id']), 'label': ic_data['label'],
                'category': TopicCategory(ic_data['category']),
                'description': ic_data.get('description', None),
                'uri': ic_data.get('uri', None),
                'factory': ic_data.get('factory', None),
                'forced': ic_data.get('forced', False)}

        signatures = ic_data.get('signatures', None)
        if signatures is not None:
            data['signatures'] = [parse_signature(s) for s in signatures]
        else:
            data['signatures'] = []

        if 'subClassOf' in ic_data:
            value = ic_data['subClassOf']

            if isinstance(value, dict):
                data['subClassOf'] = [uuid.UUID(value['id'])]
                data['override'] = value.get('override', False)

            else:
                # value is an UUID string
                data['subClassOf'] = [uuid.UUID(value)]

        topic = DrbTopic(**data)
        return topic

    def create(self, topic: DrbTopic) -> DrbTopic:
        """
        Creates or extends a YAML file containing a topic.
        Parameters:
            topic (DrbTopic): topic to create in YAML file
        Returns:
            DrbTopic: created topic in YAML file
        """

        topics = []
        docs = []

        with open(self.__file, 'r') as file:
            data = yaml.safe_load_all(file)
            for topic_data in data:

                if uuid.UUID(topic_data['id']) != topic.id:

                    ic = self.__generate_topic_from_yaml_file(topic_data)
                    topics.append(ic)

            topics.append(topic)
            top = topic

        for topic in topics:

            doc = self.__write_topic_to_yaml_file(topic)
            docs.append(doc)

        with open(self.__file, 'w') as file:
            yaml.safe_dump_all(docs, file,
                               default_flow_style=False, sort_keys=False)

        return top

    def read(self, identifier: uuid.UUID) -> DrbTopic:
        """
        Reads a topic from a YAML file.
        Parameters:
            identifier (UUID): id of topic to read from file
        Returns:
            DrbTopic: the topic corresponding to the given identifier
        """
        with open(self.__file, 'r') as file:
            data = yaml.safe_load_all(file)
            for topic_data in data:

                if uuid.UUID(topic_data['id']) == identifier:
                    topic = self.__generate_topic_from_yaml_file(
                            topic_data)

        try:
            return topic
        except UnboundLocalError:
            raise DrbException

    def update(self, topic: DrbTopic) -> DrbTopic:
        """
        Updates a topic in a YAML file.
        Parameters:
            topic (DrbTopic): topic to update
        Returns:
            DrbTopic: topic is up-to-date
        """

        topics = []
        docs = []

        with open(self.__file, 'r') as file:
            data = yaml.safe_load_all(file)

            for topic_data in data:
                if uuid.UUID(topic_data['id']) == topic.id:
                    topics.append(topic)
                    top = topic

                else:
                    ic = self.__generate_topic_from_yaml_file(topic_data)
                    topics.append(ic)

            for topic in topics:
                doc = self.__write_topic_to_yaml_file(topic)
                docs.append(doc)

        with open(self.__file, 'w') as file:
            yaml.dump_all(docs, file,
                          default_flow_style=False,
                          sort_keys=False)

        try:
            return top
        except UnboundLocalError:
            raise DrbException

    def delete(self, identifier: uuid.UUID):
        """
        Deletes a topic from a YAML file.
        Parameters:
            identifier (UUID): id of topic to delete

        """
        with open(self.__file, 'r') as file:
            data = yaml.safe_load_all(file)
            topics = []
            docs = []

            for topic_data in data:

                if uuid.UUID(topic_data['id']) == identifier:
                    continue

                elif 'subClassOf' in topic_data:
                    try:
                        if uuid.UUID(
                                topic_data
                                ['subClassOf']) == identifier:
                            continue
                    except AttributeError:
                        if uuid.UUID(
                                topic_data
                                ['subClassOf']['id']) == identifier:
                            continue

                try:
                    ic = self.__generate_topic_from_yaml_file(topic_data)
                    topics.append(ic)

                except (KeyError, DrbException):
                    docs.append(topic_data)
                    continue

            for topic in topics:
                topic_data = self.__write_topic_to_yaml_file(topic)
                docs.append(topic_data)

        with open(self.__file, 'w') as file:
            yaml.safe_dump_all(docs, file,
                               default_flow_style=False, sort_keys=False)

    def find(self, search: str) -> List[DrbTopic]:
        """
        Finds a topic in a YAML file.
        Parameters:
        search (str): id of topic to read from file
        Returns:
        List[DrbTopic]: the topic corresponding to the given label
        """
        topics = []
        with open(self.__file, 'r') as file:
            data = yaml.safe_load_all(file)
            for topic_data in data:

                if search in topic_data['label']:
                    topic = self.__generate_topic_from_yaml_file(
                            topic_data)
                    topics.append(topic)

        return topics

    def read_all(self) -> List[DrbTopic]:
        """
        Loads all topics defined in a Cortex YAML file.
        """

        topics = []

        with open(self.__file) as file:
            data = yaml.safe_load_all(file)
            for topic_data in data:

                topic = self.__generate_topic_from_yaml_file(topic_data)
                topics.append(topic)

        return topics
