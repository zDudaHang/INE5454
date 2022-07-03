from typing import Dict, List
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class Parser(ABC):
    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        pass
