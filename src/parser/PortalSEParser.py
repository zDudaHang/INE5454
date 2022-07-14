from typing import Dict, List

from src.constants.html_tags import *
from src.constants.portal_se import *
from src.parser.Parser import Parser
from src.model.PortalTransparenciaEnum import PortalTransparenciaEnum
from src.requester.se_requester import SeRequester
from src.util import clean_text

from bs4 import BeautifulSoup
from bs4.element import Tag

# Exemplo de uso
# se_requester = SeRequester()
# parser = PortalSEParser('')
# results = parser.parse_with_requester(se_requester)
# for result in results:
#   print(result)


class PortalSEParser(Parser):

    def parse_with_requester(self, requester: SeRequester) -> dict:
        servidores: List[Dict] = list()
        while requester.has_next():
            page, first_page = requester.get_next()
            soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')
            result = self.parse(soup) if first_page else self.parse_last_page(soup)
            servidores.extend(result)
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
        return servidores

    def parse_last_page(self, soup: BeautifulSoup) -> List[Dict]:
        servidores: List[Dict] = []
        table = soup.find(TABLE)
        trs = table.find_all(TR)
        for tr in trs:
            if isinstance(tr, Tag):
                tds = tr.find_all(TD)
                servidor = {
                    PORTAL_DICT_KEY: PortalTransparenciaEnum.SE.value}
                for index, td in enumerate(tds):
                    if index > 6:
                        continue
                    if isinstance(td, Tag):
                        servidor[NOME_CAMPOS_SE[index]] = clean_text(td.text)
                servidores.append(servidor)
        return servidores
