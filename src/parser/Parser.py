from typing import Dict, List
from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def parse(self) -> List[Dict]:
        pass
