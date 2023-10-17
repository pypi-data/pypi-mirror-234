import abc
from typing import Any, Dict, List
from drb.core.node import DrbNode
from drb.topics.topic import DrbTopic
from drb.utils.plugins import get_entry_points


class Addon:
    @classmethod
    @abc.abstractmethod
    def identifier(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def return_type(cls) -> type:
        raise NotImplementedError

    @abc.abstractmethod
    def apply(self, node: DrbNode, **kwargs) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def can_apply(self, source: DrbTopic) -> bool:
        raise NotImplementedError


class AddonManager:
    __instance = None
    __addons = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(AddonManager, cls).__new__(cls)
            cls.__addons = cls.__load_addons()
        return cls.__instance

    @staticmethod
    def __load_addons() -> Dict[str, Addon]:
        addons = {}
        entry_point_group = 'drb.addon'
        for ep in get_entry_points(entry_point_group):
            addon_class = ep.load()
            if issubclass(addon_class, Addon):
                addons[addon_class.identifier()] = addon_class()
        return addons

    def get_all_addons(self) -> List[Addon]:
        return list(self.__addons.values())

    def get_addon(self, identifier: str) -> Addon:
        return self.__addons[identifier]
