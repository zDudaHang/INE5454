import os
from typing import Dict, List

from src.constants.paths import *
from src.constants.html_tags import *
from src.constants.portal_sp import *
from src.parser.Parser import Parser
from src.model.PortalTransparenciaEnum import PortalTransparenciaEnum

from bs4 import BeautifulSoup
from bs4.element import Tag


class PortalSPParser(Parser):
    def parse(self) -> List[Dict]:
        servidores: List[Dict] = []
        path_to_sp_job1 = os.path.join(
            RESOURCES_DIR, SP_RESOURCES_DIR, SP_JOB_1)
        for page in range(1, len(os.listdir(path_to_sp_job1)) + 1):
            path_to_page = os.path.join(
                path_to_sp_job1, str(page) + FILE_EXTENSION)
            with open(path_to_page, 'r') as fp:
                soup = BeautifulSoup(fp, 'html.parser')
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
                                servidor[NOME_CAMPOS[index]] = td.text.strip()
                        servidores.append(servidor)
        return servidores
