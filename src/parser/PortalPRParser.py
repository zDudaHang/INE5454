from typing import Dict, List

from src.constants.paths import *
from src.constants.html_tags import *
from src.parser.Parser import Parser
from src.constants.common import *
from src.model.PortalTransparenciaEnum import PortalTransparenciaEnum

from bs4 import BeautifulSoup
from bs4.element import Tag

from src.util import print_when_verbose_enabled, clean_text

CLASSNAME_TR_HEADER = "ui-widget-header"
CLASSNAME_TR_CONTENT = "ui-widget-content"

ATTR_CLASS = 'class'

INDEX_COLUNA_NOME = 0


def is_tr_header(tr: Tag) -> bool:
    clazz = tr.attrs[ATTR_CLASS]
    return clazz.__contains__(CLASSNAME_TR_HEADER)


def is_tr_content(tr: Tag) -> bool:
    clazz = tr.attrs[ATTR_CLASS]
    return clazz.__contains__(CLASSNAME_TR_CONTENT)


class PortalPRParser(Parser):
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
                    text = span.get_text(separator=' ', strip=True)
                    if (text.__len__() != 0 and not text.__contains__('ui-button')):
                        colunas.append(clean_text(text))
        print_when_verbose_enabled(colunas)
        return colunas

    def encontrar_valores(self, colunas: List[str], soup: BeautifulSoup, servidores: List[Dict]) -> List[Dict]:
        tbody = soup.find(TBODY)
        trs = tbody.find_all(TR)
        nomeServidor = ''
        for tr in trs:
            if isinstance(tr, Tag):
                if is_tr_header(tr):
                    td = tr.find(TD)
                    if isinstance(td, Tag):
                        nomeServidor = td.get_text(separator=' ', strip=True)
                elif is_tr_content(tr):
                    servidor = {
                        PORTAL_DICT_KEY: PortalTransparenciaEnum.PR,
                        colunas[INDEX_COLUNA_NOME]: nomeServidor
                    }
                    tds = tr.find_all(TD)
                    for index_th, td in enumerate(tds, 1):
                        if isinstance(td, Tag):
                            servidor[colunas[index_th]] = clean_text(td.get_text(
                                separator=' ', strip=True))
                    servidores.append(servidor)
        print_when_verbose_enabled(servidores)
        return servidores
