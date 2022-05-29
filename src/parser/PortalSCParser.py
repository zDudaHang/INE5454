import os
from typing import Dict, List

from src.constants.paths import *
from src.constants.html_tags import *
from src.parser.Parser import Parser

from bs4 import BeautifulSoup
from bs4.element import Tag


class PortalSCParser(Parser):
    def parse(self):
        servidores: List[Dict] = []
        path_to_job1 = os.path.join(RESOURCES_DIR, SC_RESOURCES_DIR, SC_JOB_1)
        for page in range(1, len(os.listdir(path_to_job1)) + 1):
            path_to_page = os.path.join(
                path_to_job1, str(page) + FILE_EXTENSION)
            with open(path_to_page, 'r') as fp:
                soup = BeautifulSoup(fp, 'html.parser')
                colunas = encontrar_colunas(soup)
                servidores = encontrar_valores(colunas, soup, servidores)
        print(servidores)

    def validate(self):
        pass


def encontrar_colunas(soup: BeautifulSoup) -> List[str]:
    colunas: List[str] = []
    thead = soup.find(THEAD)
    if (isinstance(thead, Tag)):
        ths = thead.find_all(TH)
        for th in ths:
            if (isinstance(th, Tag)):
                span = th.find(SPAN)
            if (isinstance(span, Tag)):
                colunas.append(span.text.strip())
    return colunas


def encontrar_valores(colunas: List[str], soup: BeautifulSoup, servidores: List[Dict]) -> List[Dict]:
    tbody = soup.find(TBODY)
    trs = tbody.find_all(TR)
    for tr in trs:
        if (isinstance(tr, Tag)):
            tds = tr.find_all(TD)
            servidor = {}
            for index_th, td in enumerate(tds):
                if (isinstance(td, Tag)):
                    span = td.find(SPAN)
                    if (isinstance(span, Tag)):
                        servidor[colunas[index_th]] = span.text
            servidores.append(servidor)
    return servidores
