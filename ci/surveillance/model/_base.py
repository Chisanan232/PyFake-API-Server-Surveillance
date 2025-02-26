from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Mapping


@dataclass
class _BaseModel(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def deserialize(data: Mapping) -> "_BaseModel":
        pass
