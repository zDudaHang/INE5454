from typing import Dict, List

from src.constants.paths import *
from src.constants.html_tags import *
from src.parser.Parser import Parser
from src.constants.common import *
from src.model.PortalTransparenciaEnum import PortalTransparenciaEnum

from bs4 import BeautifulSoup
from bs4.element import Tag

from src.util import print_when_verbose_enabled


class PortalSCParser(Parser):
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        servidores: List[Dict] = []
        colunas = self.encontrar_colunas(soup)
        servidores = self.encontrar_valores(colunas, soup, servidores)
        return servidores

    def encontrar_colunas(self, soup: BeautifulSoup) -> List[str]:
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

    def encontrar_valores(self, colunas: List[str], soup: BeautifulSoup, servidores: List[Dict]) -> List[Dict]:
        tbody = soup.find(TBODY)
        trs = tbody.find_all(TR)
        for tr in trs:
            if (isinstance(tr, Tag)):
                tds = tr.find_all(TD)
                servidor = {
                    PORTAL_DICT_KEY: PortalTransparenciaEnum.SC}
                for index_th, td in enumerate(tds):
                    if (isinstance(td, Tag)):
                        span = td.find(SPAN)
                        if (isinstance(span, Tag)):
                            servidor[colunas[index_th]] = span.text
                servidores.append(servidor)
        print_when_verbose_enabled(servidores)
        return servidores
