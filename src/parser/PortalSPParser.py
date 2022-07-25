from typing import Dict, List

from src.constants.html_tags import *
from src.constants.portal_sp import *
from src.parser.Parser import Parser
from src.model.PortalTransparenciaEnum import PortalTransparenciaEnum
from src.requester.sp_requester import SpRequester

from bs4 import BeautifulSoup
from bs4.element import Tag

# Exemplo de uso
# sp_requester = SpRequester(orgao=71)
# parser = PortalSPParser('')
# results = parser.parse_with_requester(sp_requester)
# for result in results:
#   print(result)


class PortalSPParser(Parser):
    ATTRS_TO_GET = [NOME, CARGO, ORGAO, REMUNERACAO]

    def parse_with_requester(self, requester: SpRequester, max_pages_to_parse: int = 20) -> list[dict]:
        servidores: list[dict] = list()
        pages_parsed = 0
        while requester.has_next():
            if pages_parsed > max_pages_to_parse:
                break
            page = requester.get_next()
            soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')
            result = self.parse(soup)
            servidores.extend(result)
            pages_parsed = pages_parsed + 1
        return servidores

    def parse(self, soup: BeautifulSoup) -> list[dict]:
        servidores: List[Dict] = []
        result = soup.find(TABLE, attrs={'rules': 'all'})
        trs = result.find_all(TR, attrs=None)
        for tr in trs:
            if isinstance(tr, Tag):
                tds = tr.find_all(TD)
                if len(tds) < 1:
                    continue
                servidor = {
                    PORTAL_DICT_KEY: PortalTransparenciaEnum.SP.value}
                for index, td in enumerate(tds):
                    if isinstance(td, Tag):
                        # pega apenas atributos em comum com outros portais
                        if NOME_CAMPOS_SP[index] in self.ATTRS_TO_GET:
                            servidor[NOME_CAMPOS_SP[index]] = td.text
                servidores.append(servidor)
        return servidores
