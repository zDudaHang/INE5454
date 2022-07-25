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
    COLUNAS = ['NOME', 'CARGO', 'ORGAO', 'REMUNERACAO']

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        servidores: List[Dict] = []
        # colunas = self.encontrar_colunas(soup)
        servidores = self.encontrar_valores(self.COLUNAS, soup, servidores)
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
        print_when_verbose_enabled(f'Colunas={colunas}')
        return colunas

    def encontrar_valores(self, colunas: List[str], soup: BeautifulSoup, servidores: List[Dict]) -> List[Dict]:
        tbody = soup.find(TBODY)
        if tbody != None:
            trs = tbody.find_all(TR)
            for tr in trs:
                if (isinstance(tr, Tag)):
                    tds = tr.find_all(TD)
                    servidor = {
                        PORTAL_DICT_KEY: PortalTransparenciaEnum.SC.value}
                    # elimina info sobre situação
                    tds.pop(1)
                    for index_th, td in enumerate(tds):
                        if (isinstance(td, Tag)):
                            span = td.find(SPAN)
                            if (isinstance(span, Tag)):
                                text = span.text
                                if text.find('R$') != -1:
                                    text = text.replace('R$', '')
                                    text = text.strip()
                                servidor[colunas[index_th]] = text
                    servidores.append(servidor)
            print_when_verbose_enabled(f'servidores encontrados={servidores}')
        return servidores
