"""
This module defines a base class for models in the system.
The `_BaseModel` serves as an abstract base class that requires
derived classes to implement data deserialization.

Classes:

- _BaseModel: Abstract base class for defining data models with deserialization logic.
"""

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Mapping


@dataclass
class _BaseModel(metaclass=ABCMeta):
    """
    Defines a base abstract model with the requirement of implementing a
    deserialize method for data transformation.

    This class serves as a blueprint for creating models that represent
    domain-specific entities or data. It enforces the implementation of a
    `deserialize` method, ensuring all inherited classes adhere to the same
    interface for data deserialization. The deserialize method is intended
    to parse a mapping (like a dictionary) into an instance of the specific
    model.
    """

    @staticmethod
    @abstractmethod
    def deserialize(data: Mapping) -> "_BaseModel":
        """
        Deserializes the provided data into an instance of a class that
        inherits from `_BaseModel`. This is an abstract method that
        needs to be implemented in subclasses. The deserialization
        process is expected to transform a mapping structure into the
        corresponding model instance.

        :param data: The input data mapping to be deserialized to
            a `_BaseModel` instance.
        :type data: Mapping
        :return: A deserialized instance of `_BaseModel` created from
            the given data.
        :rtype: _BaseModel
        """
