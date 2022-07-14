from typing import Dict, List

from src.constants.html_tags import *
from src.constants.portal_sp import *
from src.parser.Parser import Parser
from src.model.PortalTransparenciaEnum import PortalTransparenciaEnum
from src.requester.sp_requester import SpRequester
from src.util import clean_text

from bs4 import BeautifulSoup
from bs4.element import Tag


class PortalSPParser(Parser):

    def parse_with_requester(self, requester: SpRequester) -> List[dict]:
        servidores: List[Dict] = list()
        while requester.has_next():
            page = requester.get_next()
            soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')
            result = self.parse(soup)
            servidores.extend(result)
        return servidores

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
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
                        servidor[NOME_CAMPOS_SP[index]] = clean_text(td.text)
                servidores.append(servidor)
        return servidores
