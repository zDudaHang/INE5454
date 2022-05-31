import os
from typing import Dict, List

from src.constants.paths import *
from src.constants.html_tags import *
from src.constants.portal_sp import *
from src.parser.Parser import Parser
from src.model.PortalTransparenciaEnum import PortalTransparenciaEnum
from src.util import print_when_verbose_enabled, clean_text

from bs4 import BeautifulSoup
from bs4.element import Tag


class PortalSPParser(Parser):
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
                    PORTAL_DICT_KEY: PortalTransparenciaEnum.SP}
                for index, td in enumerate(tds):
                    if isinstance(td, Tag):
                        servidor[NOME_CAMPOS[index]] = clean_text(td.text)
                servidores.append(servidor)
        print_when_verbose_enabled(servidores)
        return servidores
