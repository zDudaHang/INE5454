import os
from typing import Dict, List

from src.constants.html_tags import *
from src.constants.portal_se import *
from src.parser.Parser import Parser
from src.model.PortalTransparenciaEnum import PortalTransparenciaEnum
from src.requester.se_requester import SeRequester
from src.util import print_when_verbose_enabled, clean_text

from bs4 import BeautifulSoup
from bs4.element import Tag


class PortalSEParser(Parser):
    def parse_with_requester(self, requester: SeRequester) -> dict:
        servidores: List[Dict] = list()
        while requester.has_next():
            page = requester.get_next()
            soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')
            servidores.extend(self.parse(soup))
        return servidores

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        servidores: List[Dict] = []
        table = soup.find(TABLE)
        tbody = table.find(TBODY, attrs={'id': 'frmPrincipal:Tabela_data'})
        trs = tbody.find_all(TR)
        for tr in trs:
            if isinstance(tr, Tag):
                tds = tr.find_all(TD)
                servidor = {
                    PORTAL_DICT_KEY: PortalTransparenciaEnum.SC}
                for index, td in enumerate(tds):
                    if index > 6:
                        continue
                    if isinstance(td, Tag):
                        servidor[NOME_CAMPOS_SE[index]] = clean_text(td.text)
                servidores.append(servidor)
        print_when_verbose_enabled(servidores)
        return servidores
