from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class Parser(ABC):
    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> list[dict]:
        pass
