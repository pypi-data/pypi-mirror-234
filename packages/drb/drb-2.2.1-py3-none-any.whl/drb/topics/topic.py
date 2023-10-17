from __future__ import annotations
from dataclasses import dataclass, field

import enum
import uuid
from typing import List

from drb.core.node import DrbNode
from drb.core.signature import Signature


class TopicCategory(enum.Enum):
    SECURITY = 'SECURITY'
    PROTOCOL = 'PROTOCOL'
    CONTAINER = 'CONTAINER'
    FORMATTING = 'FORMATTING'


@dataclass
class DrbTopic:
    """
    Class for defining a type of node, this type is described in each
     DRB topic or implementation.
    """

    id: uuid.UUID
    label: str
    category: TopicCategory = field(default=None, repr=False)
    subClassOf: List[uuid.UUID] = field(default=None, repr=False)
    uri: str = field(default=None, repr=False)
    factory: str = field(default=None, repr=False)
    description: str = field(default=None, repr=False)
    forced: bool = field(default=False, repr=False)
    signatures: List[Signature] = field(default=None, repr=False)
    override: bool = field(default=False, repr=False)

    def matches(self, node: DrbNode) -> bool:
        """
        Checks if the given node match one of its signatures.

        Parameters:
            node(DrbNode): node supportability to check
        Returns:
            bool: ``True`` if the given node is supported by the item class
        """
        for signature in self.signatures:
            if signature.matches(node):
                return True
        return False

    def __eq__(self, other):
        """
        Defines the equality comparison for the DrbTopic class.

        Parameters:
            other (DrbTopic): The other object to compare with.
        Returns:
            bool: True if both objects are equal, False otherwise.
        """
        if not isinstance(other, DrbTopic):
            return False
        return self.id == other.id
