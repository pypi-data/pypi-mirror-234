import abc
from dataclasses import dataclass

@dataclass
class BaseMapping(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def empty():
        pass

    @abc.abstractclassmethod
    def to_dict(self) -> dict:
        pass

    @abc.abstractmethod
    def ready_to_generate(self) -> bool:
        pass

    @abc.abstractmethod
    def generate_values(self) -> list[dict]:
        pass