import os
from typing import Dict, List
from abc import ABC, abstractmethod

from src.requester.requester import Requester
from src.util import print_when_debug_enabled, is_html_file
from bs4 import BeautifulSoup


class Parser(ABC):
    def __init__(self, resources_path: str):
        self.resources_path = resources_path

    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        pass

    @abstractmethod
    def parse_with_requester(self, requester: Requester) -> dict:
        pass

    def parse_resources(self) -> List[Dict]:
        return self.find_html_resources_and_parse(self.resources_path)

    def find_html_resources_and_parse(self, path: str) -> List[Dict]:
        todosServidores: List[Dict] = []
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file():
                    if is_html_file(entry.path):
                        with open(entry.path, 'r') as fp:
                            soup = BeautifulSoup(fp, 'html.parser')
                            servidores = self.parse(soup)
                            print_when_debug_enabled(
                                f"{entry.path}: {servidores.__len__()} registros")
                            todosServidores.extend(servidores)
                elif entry.is_dir():
                    servidores = self.find_html_resources_and_parse(entry.path)
                    todosServidores.extend(servidores)
        return todosServidores
