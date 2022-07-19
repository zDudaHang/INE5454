from typing import Dict, List

from src.constants.html_tags import *
from src.constants.portal_se import *
from src.parser.Parser import Parser
from src.model.PortalTransparenciaEnum import PortalTransparenciaEnum
from src.requester.se_requester import SeRequester

from bs4 import BeautifulSoup
from bs4.element import Tag

# Exemplo de uso
# se_requester = SeRequester()
# parser = PortalSEParser('')
# results = parser.parse_with_requester(se_requester)
# for result in results:
#   print(result)


class PortalSEParser(Parser):
    ATTRS_TO_GET = [NOME, CARGO, ORGAO, REMUNERACAO_MES]

    def parse_with_requester(self, requester: SeRequester) -> list[dict]:
        servidores: List[Dict] = list()
        while requester.has_next():
            page = requester.get_next()
            soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')
            result = self.parse(soup)
            servidores.extend(result)
        return servidores

    def parse(self, soup: BeautifulSoup) -> list[dict]:
        servidores: List[Dict] = []
        table = soup.find(TABLE)
        tbody = table.find(TBODY, attrs={'id': 'frmPrincipal:Tabela_data'})
        trs = tbody.find_all(TR)
        for tr in trs:
            if isinstance(tr, Tag):
                tds = tr.find_all(TD)
                servidor = {
                    PORTAL_DICT_KEY: PortalTransparenciaEnum.SE.value}
                for index, td in enumerate(tds):
                    if index > 6:
                        continue
                    if isinstance(td, Tag):
                        # pega apenas atributos em comum com outrosportais
                        if NOME_CAMPOS_SE[index] in self.ATTRS_TO_GET:
                            servidor[NOME_CAMPOS_SE[index]] = td.text
                servidores.append(servidor)
        return servidores
