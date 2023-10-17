from abc import ABC, abstractmethod

import uuid
from typing import List

from drb.topics.topic import DrbTopic


class DrbTopicDao(ABC):
    """
    Provides an interface to some type of database
    or other persistence mechanism.
    """
    @abstractmethod
    def create(self, topic: DrbTopic) -> DrbTopic:
        raise NotImplementedError

    @abstractmethod
    def read(self, identifier: uuid.UUID) -> DrbTopic:
        raise NotImplementedError

    @abstractmethod
    def update(self, topic: DrbTopic) -> DrbTopic:
        raise NotImplementedError

    @abstractmethod
    def delete(self, identifier: uuid.UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def find(self, search: str) -> List[DrbTopic]:
        raise NotImplementedError

    @abstractmethod
    def read_all(self) -> List[DrbTopic]:
        raise NotImplementedError
