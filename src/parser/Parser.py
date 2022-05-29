
from typing import List
from abc import ABC, abstractmethod
from src.model.Servidor import Servidor


class Parser(ABC):
    @abstractmethod
    def parse(self) -> List[Servidor]:
        pass

    @abstractmethod
    def validate(self) -> bool:
        pass
