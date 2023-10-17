import os
import logging
import uuid
from pathlib import Path
from typing import List
from deprecated import deprecated

from drb.drivers.xml import XmlNodeFactory, XmlNode

from .topic_dao import DrbTopicDao
from drb.core.signature import parse_signature
from drb.topics.topic import DrbTopic, TopicCategory
from drb.exceptions.core import DrbException


logger = logging.getLogger('DrbTopic')

ns = {'owl': 'http://www.w3.org/2002/07/owl#',
      'drb': 'http://www.gael.fr/drb#',
      'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
      'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}


@deprecated(version='2.1.4',
            reason='Usage of the RDFDao is recommended')
class XmlDao(DrbTopicDao):

    def __init__(self, path: str):
        # if not existing, generate a new file.
        Path(path).touch(exist_ok=True)

        self.__file = path
        self.__nodes = self.__search_xml_node()

    def __search_xml_node(self) -> List[XmlNode]:
        """
        Search for all topics in XML file.
        Returns:
            List[XmlNode]: list containing nodes of XML topics
        """

        path = os.path.join(self.__file)
        n = XmlNodeFactory().create(path)
        nodes = n['Class', ns['owl'], :]

        return nodes

    def __generate_topic_from_xml_node(self, node: XmlNode) -> DrbTopic:
        """
        Converts a node into a dictionary used for generating XmlTopic(s).
        Parameters:
            node (XmlNode): node to convert
        Returns:
            DrbTopic: the corresponding topic
        """
        data = {}
        uri_parent = None
        uri = list(node.attributes.values())[0]

        data['uri'] = uri
        data['id'] = self.generate_id(uri)
        data['category'] = TopicCategory('CONTAINER')

        signatures = []
        parents = []

        for child in node.children:
            if child.name == 'subClassOf':

                try:
                    uri_parent = list(child.attributes.values())[0]

                except (IndexError, DrbException):
                    for grandchild in child.children:
                        uri_parent = list(grandchild.attributes.values())[0]

                parent = self.generate_id(uri_parent)
                parents.append(parent)
                data['subClassOf'] = parents

            if child.name == 'label':
                data['label'] = child.value

            if child.name == 'implementationIdentifier':
                data['factory'] = {'name': child.value}

            if child.name == 'comment':
                data['description'] = child.value

            if child.name == 'signature':

                for grandchild in child.children:

                    signature = {}
                    if grandchild.name == 'nameMatch':
                        signature['name'] = grandchild.value
                        signatures.append(signature)

                    elif grandchild.name == 'parentClassName':
                        signature['parent'] = grandchild.value
                        signatures.append(signature)

                data['signatures'] = [parse_signature(s) for s in signatures]
        topic = DrbTopic(**data)

        return topic

    @staticmethod
    def generate_id(uri: str) -> uuid.UUID:
        """
        Generates an unique UUID from topic's unique URI.
        Parameters:
            uri (str): topic's unique URI
        Returns:
            UUID: topic's unique
        """
        return uuid.uuid3(uuid.NAMESPACE_DNS, uri)

    def read(self, identifier: uuid.UUID) -> DrbTopic:
        """
        Reads a topic from XML file.
        Parameters:
            identifier (UUID): id of topic to read from file
        Returns:
            DrbTopic: the topic corresponding to the given identifier
                """

        for node in self.__nodes:
            uri = list(node.attributes.values())[0]
            id_from_uri = self.generate_id(uri)

            if id_from_uri == identifier:
                topic = self.__generate_topic_from_xml_node(node)
                return topic
            else:
                continue

        raise DrbException

    def find(self, search: str) -> List[DrbTopic]:
        """
        Finds a topic from an XML file.
        Parameters:
            search (str): label of topic to read from file
        Returns:
            List[DrbTopic]: the topic corresponding to the given label
        """
        topics = []
        for node in self.__nodes:
            for child in node.children:

                if child.name == 'label':
                    if search in child.value:
                        topic = self.__generate_topic_from_xml_node(node)
                        topics.append(topic)

        return topics

    def read_all(self) -> List[DrbTopic]:
        """
        Loads all topics defined in XML files.
        """

        topics = []

        for node in self.__nodes:

            try:
                topic = self.__generate_topic_from_xml_node(node)
                topics.append(topic)

            except TypeError:
                continue

        return topics

    def create(self, topic: DrbTopic) -> DrbTopic:
        raise NotImplementedError

    def update(self, topic: DrbTopic) -> DrbTopic:
        raise NotImplementedError

    def delete(self, identifier: uuid.UUID) -> None:
        raise NotImplementedError
