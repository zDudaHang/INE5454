from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import List


class Parser(ABC):
    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[dict]:
        pass
